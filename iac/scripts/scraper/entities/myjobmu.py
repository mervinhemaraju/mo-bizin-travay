import logging
from kink import di
from bs4 import BeautifulSoup
from models.core.web_driver import WebDriver
from datetime import datetime
from utils.extractors import retrieve_tag_href, retrieve_tag_text, retrieve_date


def main_scraping_process(web_driver: WebDriver, filters: dict):
    # Define empty openings list
    openings = []

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
        if link not in di["opening_ids"]:
            # Append the opening id to the list
            di["opening_ids"].append(link)

            # Create an opening document
            document = {
                "title": title,
                "posted_date": posted_date.strftime("%Y-%m-%d")
                if posted_date
                else datetime.now().strftime("%Y-%m-%d"),
                "closing_date": closing_date.strftime("%Y-%m-%d")
                if closing_date
                else None,
                "recruiter": recruiter if recruiter else "MYJOBMU",
                "location": location if location else "Not Specified.",
                "salary_range": salary_range if salary_range else "Not disclosed.",
                "updated_at": datetime.now().strftime("%Y-%m-%d"),
                "opening_source": di["SOURCE"],
                "link": link,
            }

            # Append to openings list
            openings.append(document)

    # Return the soup for the main container
    return BeautifulSoup(container.get_attribute("outerHTML"), "html.parser"), openings


def scrape(delay, dry_run):
    # ! Define the filters
    filters = {
        "wrapper": "div#page",
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
    web_driver = WebDriver(di["SOURCE_URL"], delay, dry_run)

    # Define empty openings list
    openings = []

    # Extract openings and retrieve the container soup
    container_soup, scraped_openings = main_scraping_process(
        web_driver=web_driver, filters=filters
    )

    # Append scraped openings to list
    openings += scraped_openings

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
        if next_button_url in di["visited_urls"]:
            # Log event
            logging.warn(
                "Pagination has looped back to the first page. Breaking the loop."
            )

            # Break loop
            break

        # Add URL to the visited URL
        di["visited_urls"].append(next_button_url)

        # Log event
        logging.info(f"Pagination found on url {next_button_url}")

        # Close any previous drivers
        if web_driver:
            web_driver.quit()

        # Recreate a new driver
        web_driver = WebDriver(next_button_url, delay, dry_run)

        # Extract openings and retrieve the container soup
        container_soup, scraped_openings = main_scraping_process(
            web_driver=web_driver, filters=filters
        )

        # Append scraped openings to list
        openings += scraped_openings

        # Find the next button pagination
        next_button_url = retrieve_tag_href(
            soup=container_soup, filter=filters["pagination_button"]
        )

    # If web driver not empty, quit
    if web_driver:
        web_driver.quit()

    # Return the openings
    return openings
