from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    webdriver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=webdriver_service,options=chrome_options)
    print('driver is:', driver.title)
    return driver




