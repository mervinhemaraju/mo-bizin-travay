from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:
    def __init__(self, url, delay) -> None:
        # Set up Chrome WebDriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")

        # Load chrome driver manager service
        self.chrome = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=chrome_options
        )

        # Open the desired webpage
        self.chrome.get(url)

        # Wait for the "openings" tag to load
        self.wait = WebDriverWait(self.chrome, delay)

    def load_elements(self, main_filter):
        return self.wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, main_filter))
        )

    def quit(self):
        # Quit the chrome driver
        self.chrome.quit()
