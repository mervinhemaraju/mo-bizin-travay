import logging
from kink import di
from datetime import datetime
from bs4 import BeautifulSoup
from models.core.di import main_injection
from models.core.web_driver import WebDriver
from models.db.opening import Opening
from utils.extractors import retrieve_tag_href, retrieve_tag_text
from models.db.opening_dao import ItemDao

# Initialize Logging
logging.getLogger().setLevel(logging.INFO)


@main_injection
def main(event, context):
    # Create a web driver instance
    web_driver = WebDriver(di["URL"], di["DELAY"])

    # Log event
    logging.info("Web driver has been intialized. Retrieving openings...")

    # Load the opening elements
    opening_elements = web_driver.load_elements(di["PRINCIPAL_FILTER"])

    # Extract the HTML of all openings elements, parse them with BS4 and save to JSON
    openings = []

    # Log event
    logging.info("Filtering the openings")

    for opening in opening_elements:
        # outer = position.get_attribute("outerHTML")
        soup = BeautifulSoup(opening.get_attribute("outerHTML"), "html.parser")
        opening_title = retrieve_tag_text(soup, di["FILTERS_NAME"])
        opening_posted_date = retrieve_tag_text(soup, di["FILTER_POSTED_DATE"])
        link = retrieve_tag_href(soup, di["FILTER_LINK"])

        openings.append(
            Opening(
                id=link,
                title=opening_title,
                posted_date=opening_posted_date,
                recruiter=di["RECRUITER"],
                updated_at=datetime.now().strftime("%Y-%m-%d"),
            )
        )

    if len(openings) > 0:
        # Log event
        logging.info(
            f"{len(openings)} openings obtained from recruiter {di['RECRUITER']}"
        )

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
        item_dao.save_all(openings=openings)

        # Log event
        logging.info("New openings saved successfully")

    # Close the WebDriver
    web_driver.quit()

    # Log event
    logging.info("Script completed successfully.")
