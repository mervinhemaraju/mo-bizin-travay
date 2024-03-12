import logging
from kink import di
from datetime import datetime
from bs4 import BeautifulSoup
from models.core.web_driver import WebDriver
from models.core.di import main_injection
from models.db.opening import Opening
from utils.extractors import retrieve_tag_href, retrieve_tag_text, retrieve_date
from models.db.opening_dao import ItemDao

# Initialize Logging
logging.getLogger().setLevel(logging.INFO)

# Define empty list of openings
OPENINGS = []


# Other Functions
def main_scraping_process(web_driver: WebDriver):
    # Define global vars
    global OPENINGS

    # Log event
    logging.info("Web driver has been intialized. Retrieving openings...")

    # Load the main container and opening elements
    container, opening_elements = web_driver.load_elements(
        wrapper_filter=di["WRAPPER_FILTER"], openings_filter=di["OPENINGS_FILTER"]
    )

    # Iterate through each opening elements
    for opening in opening_elements:
        # outer = opening.get_attribute("outerHTML")
        # print(f"Outer {opening.get_attribute('outerHTML')}")

        # Retrieve opening details
        soup = BeautifulSoup(opening.get_attribute("outerHTML"), "html.parser")
        opening_title = retrieve_tag_text(soup, di["FILTERS_NAME"])
        opening_posted_date = retrieve_date(soup, di["FILTER_POSTED_DATE"])
        link = retrieve_tag_href(soup, di["FILTER_LINK"])

        # Append opening to the list
        OPENINGS.append(
            Opening(
                id=link,
                title=opening_title,
                posted_date=opening_posted_date,
                recruiter=di["RECRUITER"],
                updated_at=datetime.now().strftime("%Y-%m-%d"),
            )
        )

    # Return the soup for the main container
    return BeautifulSoup(container.get_attribute("outerHTML"), "html.parser")


@main_injection
def main(event, context):
    # Define global vars
    global OPENINGS

    # Clear vars before starting
    OPENINGS.clear()

    # Get the dry run flag
    dry_run = "dry_run" in event

    # Create the web driver
    web_driver = WebDriver(di["CAREERS_URL"], di["DELAY"], dry_run)

    # Extract openings and retrieve the container soup
    container_soup = main_scraping_process(web_driver=web_driver)

    # Find the next button pagination
    next_button = container_soup.select(di["FILTER_PAGINATION_BUTTON"])

    # Verify if there is pagination
    while len(next_button) > 0:
        # Get the next url
        new_url = next_button[0]["href"]

        # If partial url, add prefix
        if di["MAIN_URL"] not in new_url:
            new_url = f"{di['MAIN_URL']}{new_url}"

        # Log event
        logging.info(f"Pagination found on url {new_url}")

        # Close any previous drivers
        if web_driver:
            web_driver.quit()

        # Recreate a new driver
        web_driver = WebDriver(new_url, di["DELAY"], dry_run)

        # Extract openings and retrieve the container soup
        container_soup = main_scraping_process(web_driver=web_driver)

        # Find the next button pagination
        next_button = container_soup.select(di["FILTER_PAGINATION_BUTTON"])

    if len(OPENINGS) > 0:
        # Log event
        logging.info(
            f"{len(OPENINGS)} openings obtained from recruiter {di['RECRUITER']}"
        )

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
        logging.info("Retrieving previous opening...")

        # Retrieve the previous openings
        previous_openings = item_dao.get_items_by_recruiter(recruiter=di["RECRUITER"])

        # Log event
        logging.info(
            f"{len(previous_openings)} previous openings obtained from recruiter {di['RECRUITER']}"
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
