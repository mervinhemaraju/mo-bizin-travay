from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import os

# Retrieve environment variables
URL = os.environ["URL"]
DELAY = os.environ["DELAY"]

# Set up Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless=new")


chrome = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

# Open the desired webpage
chrome.get(URL)

# Wait for the "quotes" divs to load
wait = WebDriverWait(chrome, DELAY)
quote_elements = wait.until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "quote"))
)

# Extract the HTML of all "quote" elements, parse them with BS4 and save to JSON
quote_data = []

for quote_element in quote_elements:
    print(quote_element.get_attribute("outerHTML"))
    soup = BeautifulSoup(quote_element.get_attribute("outerHTML"), "html.parser")
    quote_text = soup.find("span", class_="text").text
    author = soup.find("small", class_="author").text
    tags = [tag.text for tag in soup.find_all("a", class_="tag")]
    quote_info = {"Quote": quote_text, "Author": author, "Tags": tags}
    quote_data.append(quote_info)


with open("quote_info.json", "w") as json_file:
    json.dump(quote_data, json_file, indent=4)

# Close the WebDriver
chrome.quit()
