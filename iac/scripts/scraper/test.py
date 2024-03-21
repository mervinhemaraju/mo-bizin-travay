import logging
from kink import di
from datetime import datetime
from bs4 import BeautifulSoup
from models.core.web_driver import WebDriver

# from models.core.di import main_injection
from models.db.opening import Opening
from utils.extractors import retrieve_tag_href, retrieve_tag_text, retrieve_date
from models.db.opening_dao import ItemDao

# Initialize Logging
logging.getLogger().setLevel(logging.INFO)

# Define empty list of openings
OPENINGS: list[Opening] = []
OPENINGS_IDS: list[str] = []
VISITED_URLS: list[str] = []


# Other Functions
# def main_scraping_process(web_driver: WebDriver):
#     # Define global vars
#     global OPENINGS

#     # Log event
#     logging.info("Web driver has been intialized. Retrieving openings...")

#     # Load the main container and opening elements
#     container, opening_elements = web_driver.load_elements(
#         wrapper_filter=di["WRAPPER_FILTER"], openings_filter=di["OPENINGS_FILTER"]
#     )

#     # Iterate through each opening elements
#     for opening in opening_elements:
#         # outer = opening.get_attribute("outerHTML")
#         # print(f"Outer {opening.get_attribute('outerHTML')}")

#         # Retrieve opening details
#         soup = BeautifulSoup(opening.get_attribute("outerHTML"), "html.parser")
#         opening_title = retrieve_tag_text(soup, di["FILTERS_NAME"])
#         opening_posted_date = retrieve_date(soup, di["FILTER_POSTED_DATE"])
#         link = retrieve_tag_href(soup, di["FILTER_LINK"])

#         # Append opening to the list
#         OPENINGS.append(
#             Opening(
#                 id=link,
#                 title=opening_title,
#                 posted_date=opening_posted_date,
#                 recruiter=di["RECRUITER"],
#                 updated_at=datetime.now().strftime("%Y-%m-%d"),
#             )
#         )

#     # Return the soup for the main container
#     return BeautifulSoup(container.get_attribute("outerHTML"), "html.parser")


def main(event, context):
    # Define global vars
    global OPENINGS, OPENINGS_IDS, VISITED_URLS

    # Clear vars before starting
    OPENINGS.clear()
    OPENINGS_IDS.clear()
    VISITED_URLS.clear()

    url = "https://www.myjob.mu/ShowResults.aspx?Keywords=&Location=&Category=&Recruiter=Company&Page=3"
    filters = {
        "wrapper": "div.two-thirds",
        "openings": "div.module.job-result",
        "name": "div.module-content div.job-result-logo-title div.job-result-title h2 a",
        "posted_date": "div.module-content div.job-result-overview ul.job-overview li.updated-time",
        "closing_date": "div.module-content div.job-result-overview ul.job-overview li.closed-time",
        "recruiter": "div.module-content div.job-result-logo-title div.job-result-title h3 a",
        "salary_range": "div.module-content div.job-result-overview ul.job-overview li.salary",
        "location": "div.module-content div.job-result-overview ul.job-overview li.location",
        "link": "div.module-content div.job-result-logo-title div.job-result-title h2 a",
        "pagination_button": "ul#pagination li:last-child a",
    }

    # Create the web driver
    web_driver = WebDriver(url, 15, True)

    # Load the main container and opening elements
    container, opening_elements = web_driver.load_elements(
        wrapper_filter=filters["wrapper"],
        openings_filter=filters["openings"],
    )

    # Iterate through each opening elements
    for opening in opening_elements:
        soup = BeautifulSoup(opening.get_attribute("outerHTML"), "html.parser")
        title = retrieve_tag_text(soup, filters["name"])

        # Append opening to the list
        OPENINGS.append(
            Opening(
                id="Test",
                title=title,
                posted_date="N/A",
                closing_date="N/A",
                recruiter="Test",
                location="Test",
                salary_range="Test",
                updated_at="Test",
                opening_source="Test",
            )
        )

    for opening in OPENINGS:
        print(opening.title)


main({}, {})
