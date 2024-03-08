from kink import di
from datetime import datetime
from bs4 import BeautifulSoup
from models.web_driver import WebDriver
from models.opening import Opening
from di import main_injection
from utils.extractors import retrieve_tag_href, retrieve_tag_text


@main_injection
def main(event, context):
    # Create a web driver instance
    web_driver = WebDriver(di["URL"], di["DELAY"])

    # Load the opening elements
    opening_elements = web_driver.load_elements(di["PRINCIPAL_FILTER"])

    # Extract the HTML of all openings elements, parse them with BS4 and save to JSON
    openings = []

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

    with Opening.batch_write() as batch:
        for opening in openings:
            batch.save(opening)

    # Close the WebDriver
    web_driver.quit()
