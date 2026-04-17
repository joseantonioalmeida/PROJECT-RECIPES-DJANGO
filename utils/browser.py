from time import sleep
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


ROOT_PATH = Path(__file__).parent.parent
CHROMEDRIVER_NAME = "chromedriver.exe"
CHROMEDRIVER_PATH = ROOT_PATH / 'bin' / CHROMEDRIVER_NAME


# -- head
def make_chrome_browser(*optiona):
    chrome_options = webdriver.ChromeOptions()

    if optiona is not None:
        for option in optiona:
            chrome_options.add_argument(option)
            
    chrome_service = Service(executable_path=str(CHROMEDRIVER_PATH))
    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser

if __name__ == "__main__":
    browser = make_chrome_browser('headless')
    browser.get("https://www.google.com")
    sleep(5)  # Wait for 5 seconds to see the browser
    browser.quit()