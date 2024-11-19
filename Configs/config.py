from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json ,time

LOGIN_URL = "https://www.facebook.com/login"
BASE_URL = "https://www.facebook.com"

def get_driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Run headless if needed
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    with open('cookies.json', 'r') as file:
            cookies = json.load(file)

    driver.get(BASE_URL)
    time.sleep(2)

    for cookie in cookies:
            cookie.pop("sameSite", None) 
            driver.add_cookie(cookie)

    print("coookkies saved ...")



    return driver
