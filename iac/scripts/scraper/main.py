import logging
from kink import di
from datetime import datetime
from bs4 import BeautifulSoup
from models.core.web_driver import WebDriver
from models.core.di import main_injection
from models.db.opening import Opening
from models.db.opening_dao import ItemDao
from utils.functions import post_to_slack
from utils.extractors import retrieve_tag_href, retrieve_tag_text, retrieve_date

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
    logging.info("Web driver has been intialized. Retrieving openings...")

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
            # Append opening to the list
            OPENINGS.append(
                Opening(
                    id=link,
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
                    source=di["SOURCE"],
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

    # Get the dry run flag
    dry_run = "dry_run" in event

    # Retrieve event parameters
    delay = event["delay"] if "delay" in event else di["DELAY"]
    filters = event["filters"]

    # Create the web driver
    web_driver = WebDriver(di["SOURCE_URL"], delay, dry_run)

    # Extract openings and retrieve the container soup
    container_soup = main_scraping_process(web_driver=web_driver, filters=filters)

    # Find the next button pagination
    next_button = (
        container_soup.select(filters["pagination_button"])
        if filters["pagination_button"]
        else []
    )

    # Verify if there is pagination
    while len(next_button) > 0:
        # Get the next url
        new_url = next_button[0]["href"]

        # If partial url, add prefix
        if di["SOURCE_URL"] not in new_url:
            new_url = f"{di['SOURCE_URL']}{new_url}"

        # If the new url has already been visited
        # break the loop as the pagination has
        # started all over again
        if new_url in VISITED_URLS:
            # Log event
            logging.warn(
                "Pagination has looped back to the first page. Breaking the loop."
            )

            # Break loop
            break

        # Add URL to the visited URL
        VISITED_URLS.append(new_url)

        # Log event
        logging.info(f"Pagination found on url {new_url}")

        # Close any previous drivers
        if web_driver:
            web_driver.quit()

        # Recreate a new driver
        web_driver = WebDriver(new_url, delay, dry_run)

        # Extract openings and retrieve the container soup
        container_soup = main_scraping_process(web_driver=web_driver, filters=filters)

        # Find the next button pagination
        next_button = container_soup.select(filters["pagination_button"])

    if len(OPENINGS) > 0:
        # Log event
        logging.info(f"{len(OPENINGS)} openings obtained from source {di['SOURCE']}")

        # Verify if this is a dry run
        if dry_run:
            # Log event
            logging.info("Dry run detected. No data will be saved.")

            # Log event
            logging.info(
                f"{len(OPENINGS)} Openings obtained: {[str(o) for o in OPENINGS]}"
            )

            # ! Raise exception
            raise Exception("Dry run completed. No data was saved.")

        # Create a new ItemDao object
        item_dao = ItemDao()

        # Log event
        logging.info("Retrieving previous openings...")

        # Retrieve the previous openings
        previous_openings = item_dao.get_items_by_source(source=di["SOURCE"])

        # Log event
        logging.info(
            f"{len(previous_openings)} previous openings obtained from recruiter {di['SOURCE']}"
        )

        # Clear the previous openings from that recruiter
        item_dao.delete_all(openings=previous_openings)

        # Log event
        logging.info("Previous openings deleted")

        # Save the new openings
        item_dao.save_all(openings=OPENINGS)

        # Log event
        logging.info("New openings saved successfully")

    # If web driver not empty, quit
    if web_driver:
        web_driver.quit()

    # Log event
    logging.info("Script completed successfully.")
