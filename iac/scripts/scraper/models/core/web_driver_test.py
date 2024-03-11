from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebDriverTest:
    def __init__(self, url, delay) -> None:
        # Set up Chrome WebDriver
        chrome_options = webdriver.ChromeOptions()
        service = webdriver.ChromeService()

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

        self.chrome = webdriver.Chrome(options=chrome_options, service=service)

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
