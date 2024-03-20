import logging
from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:
    # Define custom headers
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36",
    }

    def __init__(self, url, delay, dry_run) -> None:
        # Log event
        logging.info("Setting chrome options.")

        # Set up Chrome WebDriver
        chrome_options = webdriver.ChromeOptions()

        # Set the driver url
        self.url = url

        # If dry run enabled, add parameters
        if dry_run:
            service = webdriver.ChromeService()
        else:
            service = webdriver.ChromeService("/opt/chromedriver")
            chrome_options.binary_location = "/opt/chrome/chrome"

        # Set additional chrome options
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1280x1696")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-dev-tools")
        chrome_options.add_argument("--no-zygote")
        chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
        chrome_options.add_argument(f"--data-path={mkdtemp()}")
        chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        chrome_options.add_argument("--remote-debugging-port=9222")
        # Add custom headers to Chrome options
        chrome_options.add_argument(f'user-agent={self.custom_headers["User-Agent"]}')

        # Set chrome web driver
        self.chrome = webdriver.Chrome(options=chrome_options, service=service)

        # Log event
        logging.info("Chrome options has been applied.")
        logging.info(f"Fetching url {self.url}")

        # Open the desired webpage
        self.chrome.get(self.url)

        # Sets the delay
        self.delay = delay

        # Log event
        logging.info(f"Web driver initialized with url {url}")

    def load_elements(self, wrapper_filter, openings_filter):
        # Wait for main container
        container = WebDriverWait(self.chrome, self.delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, wrapper_filter))
        )

        # Wait for openings
        openings = WebDriverWait(container, self.delay).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, openings_filter))
        )

        # Return the container and the openings
        return container, openings

    def quit(self):
        # Quit the chrome driver
        self.chrome.quit()
