import logging
from kink import di
from datetime import datetime
from bs4 import BeautifulSoup
from models.core.web_driver import WebDriver
from models.core.di import main_injection
from models.core.exceptions import DryRunException
from models.db.opening import Opening
from utils.functions import post_to_slack, file_transact, db_transact
from utils.extractors import retrieve_tag_href, retrieve_tag_text, retrieve_date
from utils.slack_blocks import block_completed, block_error, block_info

# Initialize Logging
logging.getLogger().setLevel(logging.INFO)

# Define empty list of openings
OPENINGS: list[Opening] = []
OPENINGS_IDS: list[str] = []
VISITED_URLS: list[str] = []


# Other Functions
def main_scraping_process(web_driver: WebDriver, filters: dict):
    # Define global vars
    global OPENINGS, OPENINGS_IDS

    # Log event
    logging.info("Starting scraping process. Retrieving openings...")

    # Load the main container and opening elements
    container, opening_elements = web_driver.load_elements(
        wrapper_filter=filters["wrapper"],
        openings_filter=filters["openings"],
    )

    # Iterate through each opening elements
    for opening in opening_elements:
        # outer = opening.get_attribute("outerHTML")
        # print(f"Outer {outer}")

        # Retrieve opening details
        soup = BeautifulSoup(opening.get_attribute("outerHTML"), "html.parser")
        title = retrieve_tag_text(soup, filters["name"])
        posted_date = retrieve_date(soup, filters["posted_date"])
        closing_date = retrieve_date(soup, filters["closing_date"])
        recruiter = retrieve_tag_text(soup, filters["recruiter"])
        salary_range = retrieve_tag_text(soup, filters["salary_range"])
        location = retrieve_tag_text(soup, filters["location"])
        link = retrieve_tag_href(soup, filters["link"])

        # If closing date is obtained and
        # closing date is before today,
        # no need to keep the opening.
        if closing_date and closing_date < datetime.now():
            # Log event
            logging.info(
                f"Closing date for title {title} is before today. Skipping it..."
            )

            # Skip to next
            continue

        # Verify if link is already present
        if link not in OPENINGS_IDS:
            # Append the opening id to the list
            OPENINGS_IDS.append(link)

            # Append opening to the list
            OPENINGS.append(
                Opening(
                    id=link
                    if link.startswith(di["DOMAIN"])
                    else f"{di['SOURCE_URL']}{link}",
                    title=title,
                    posted_date=posted_date.strftime("%Y-%m-%d")
                    if posted_date
                    else "N/A",
                    closing_date=closing_date.strftime("%Y-%m-%d")
                    if closing_date
                    else "N/A",
                    recruiter=recruiter,
                    location=location,
                    salary_range=salary_range,
                    updated_at=datetime.now().strftime("%Y-%m-%d"),
                    opening_source=di["SOURCE"],
                )
            )

    # Return the soup for the main container
    return BeautifulSoup(container.get_attribute("outerHTML"), "html.parser")


@main_injection
def main(event, context):
    # Define global vars
    global OPENINGS, OPENINGS_IDS, VISITED_URLS

    # Clear vars before starting
    OPENINGS.clear()
    OPENINGS_IDS.clear()
    VISITED_URLS.clear()

    # Post message to slack
    _, thread_ts = post_to_slack(
        blocks=block_info(
            message=f"mo-bizin-travay trigerred from source `{di['SOURCE']}` with url `{di['SOURCE_URL']}`"
        )
    )

    try:
        # Get the dry run flag
        dry_run = "dry_run" in event

        # Retrieve event parameters
        delay = event["delay"] if "delay" in event else di["DELAY"]
        filters = event["filters"]

        # Create the web driver
        web_driver = WebDriver(di["STARTUP_URL"], delay, dry_run)

        # Extract openings and retrieve the container soup
        container_soup = main_scraping_process(web_driver=web_driver, filters=filters)

        # Find the next button pagination
        next_button_url = retrieve_tag_href(
            soup=container_soup, filter=filters["pagination_button"]
        )

        # Verify if there is pagination
        while next_button_url is not None:
            # If partial url, add prefix
            if di["DOMAIN"] not in next_button_url:
                next_button_url = f"{di['SOURCE_URL']}{next_button_url}"

            # If the new url has already been visited
            # break the loop as the pagination has
            # started all over again
            if next_button_url in VISITED_URLS:
                # Log event
                logging.warn(
                    "Pagination has looped back to the first page. Breaking the loop."
                )

                # Break loop
                break

            # Add URL to the visited URL
            VISITED_URLS.append(next_button_url)

            # Log event
            logging.info(f"Pagination found on url {next_button_url}")

            # Close any previous drivers
            if web_driver:
                web_driver.quit()

            # Recreate a new driver
            web_driver = WebDriver(next_button_url, delay, dry_run)

            # Extract openings and retrieve the container soup
            container_soup = main_scraping_process(
                web_driver=web_driver, filters=filters
            )

            # Find the next button pagination
            next_button_url = retrieve_tag_href(
                soup=container_soup, filter=filters["pagination_button"]
            )

        if len(OPENINGS) > 0:
            # Log event
            logging.info(
                f"{len(OPENINGS)} openings obtained from source {di['SOURCE']}"
            )

            # Post to slack
            post_to_slack(
                blocks=block_info(
                    message=f"`{len(OPENINGS)}` openings obtained from source `{di['SOURCE']}`"
                ),
                thread_ts=thread_ts,
            )

            # Verify if this is a dry run
            if dry_run:
                # Log event
                logging.info("Dry run detected. No data will be saved.")

                # Post to slack
                post_to_slack(
                    blocks=block_info(message="Script is running in `dry run` mode"),
                    thread_ts=thread_ts,
                )

                # Log event
                # logging.info(
                #     f"{len(OPENINGS)} The following titles were obtained: {[str(o.title) for o in OPENINGS]}"
                # )

                # Export openings to json file
                file_transact(openings=OPENINGS)

                # ! Raise exception
                raise Exception("Dry run completed. No data was saved.")

            # Save openings to DB
            db_transact(openings=OPENINGS)

        # If web driver not empty, quit
        if web_driver:
            web_driver.quit()

        # Log event
        logging.info("Script completed successfully.")

        # Post to slack
        post_to_slack(blocks=block_completed(), thread_ts=thread_ts)

    except DryRunException as dre:
        # Log error
        logging.error(f"Dry Run initiated: {dre}")

        # Post to slack
        post_to_slack(
            blocks=block_error(error_message="Dry run completed."),
            thread_ts=thread_ts,
        )

    except Exception as e:
        # Log error
        logging.error(f"Error occurred: {str(e)}")

        # Post to slack
        post_to_slack(blocks=block_error(error_message=str(e)), thread_ts=thread_ts)
