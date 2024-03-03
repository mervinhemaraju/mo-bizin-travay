from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os


def retrieve_tag_value(soup, filter):
    tag = soup.select(filter)

    return tag[0].text.strip() if len(tag) > 0 else "N/A"


# Retrieve environment variables
URL = os.environ["URL"]
DELAY = os.environ["DELAY"]
PRINCIPAL_FILTER = os.environ["PRINCIPAL_FILTER"]
FILTERS_NAME = os.environ["FILTER_NAME"]
FILTER_POSTED_DATE = os.environ["FILTER_POSTED_DATE"]
RECRUITER = os.environ["RECRUITER"]

# Set up Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")


chrome = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

# Open the desired webpage
chrome.get(URL)

# Wait for the "openings" tag to load
wait = WebDriverWait(chrome, DELAY)
position_elements = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, PRINCIPAL_FILTER))
)

# Extract the HTML of all openings elements, parse them with BS4 and save to JSON
openings = []

for opening in openings:
    # outer = position.get_attribute("outerHTML")
    soup = BeautifulSoup(opening.get_attribute("outerHTML"), "html.parser")
    opening_title = retrieve_tag_value(soup, FILTERS_NAME)
    opening_posted_date = retrieve_tag_value(soup, FILTER_POSTED_DATE)

    opening_info = {
        "title": opening_title,
        "posted_date": opening_posted_date,
        "recruiter": RECRUITER,
    }
    openings.append(opening_info)

with open("openings.json", "w") as json_file:
    json.dump(openings, json_file, indent=4)

# Close the WebDriver
chrome.quit()
