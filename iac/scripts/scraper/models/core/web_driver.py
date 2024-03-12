from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriver:
    def __init__(self, url, delay, dry_run) -> None:
        # Set up Chrome WebDriver
        chrome_options = webdriver.ChromeOptions()

        # Set the driver url
        self.url = url

        # If dry run enabled, add parameters
        if dry_run:
            service = webdriver.ChromeService()
            chrome_options.binary_location = "/opt/chrome/chrome"
        else:
            service = webdriver.ChromeService("/opt/chromedriver")

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

        # Set chrome web driver
        self.chrome = webdriver.Chrome(options=chrome_options, service=service)

        # Open the desired webpage
        self.chrome.get(self.url)

        # Sets the delay
        self.delay = delay

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
