from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def create_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    print("Creating Chrome driver")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )