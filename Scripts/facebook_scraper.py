from Configs.config import get_driver, LOGIN_URL, BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, StaleElementReferenceException
import time, json
import pandas as pd

class FacebookScraper:
    def __init__(self, email, password):
        self.driver = get_driver()
        self.email = email
        self.password = password

    def login(self):
        self.driver.get(LOGIN_URL)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        self.driver.find_element(By.ID, "email").send_keys(self.email)
        self.driver.find_element(By.ID, "pass").send_keys(self.password)
        self.driver.find_element(By.NAME, "login").click()

        WebDriverWait(self.driver, 10).until(EC.url_changes(LOGIN_URL))

    def scrape_pages(self, page_url,search_input):
        css_selector = (".x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l."
                         "x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm."
                         "xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg."
                         "xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.xzsf02u.x1pd3egz")

        # Open the page and wait for the page to load properly
        self.driver.get(page_url)
        time.sleep(5)
        # Scrolling
        for i in range(1,3):
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            print(f"Scroll {i}")
            time.sleep(2)

        # Try to find the elements
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
            print(f"Found {len(elements)} elements matching the CSS selector.")
        except Exception as e:
            print(f"Error while fetching elements: {e}")
            return []

        
        page_links = []
        for i in elements:
            page_links.append(i.get_attribute("href"))

        scraped_data = []
        for index ,page_link in enumerate(page_links):
            try:
                print(f"[{index + 1}] Navigating to page: {page_link}")

                self.driver.get(page_link)
                time.sleep(5)

                try:
                    name = self.driver.find_element(By.CSS_SELECTOR,"div.x78zum5.x15sbx0n.x5oxk1f.x1jxijyj.xym1h4x.xuy2c7u.x1ltux0g.xc9uqle h1.html-h1").text
                except:
                    name = "None"
                try:
                    category = self.driver.find_element(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xamitd3.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn span.x1vvkbs.x1xmvt09.x6prxxf.xvq8zen.xo1l8bm.xzsf02u").text.split('Page · ')[1]
                except:
                    category = "None"
                try:
                    location = self.driver.find_element(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z.x78zum5.xdt5ytf.x193iq5w.xeuugli.x1r8uery.x1iyjqo2.xs83m0k.xamitd3.xsyo7zv.x16hj40l.x10b6aqq.x1yrsyyn div.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1heor9g.x1sur9pj.xkrqix3.x1s688f span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u").text
                except:
                    location = "None"
                try:
                    phone_number = self.driver.find_element(By.XPATH,"//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1xmvt09') and contains(@class, 'x1lliihq') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'xudqn12') and contains(@class, 'x3x7a5m') and contains(@class, 'x6prxxf') and contains(@class, 'xvq8zen') and contains(@class, 'xo1l8bm') and contains(@class, 'xzsf02u') and contains(@class, 'x1yc453h')][starts-with(text(), '+') or starts-with(text(), '0')]").text
                except:
                    phone_number = "None"
                try:
                    website_url = self.driver.find_element(By.CSS_SELECTOR,"a.x1i10hfl.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x1sur9pj.xkrqix3.x1qq9wsj.x1s688f").text
                except:
                    website_url = "None"                
                try:
                    email = self.driver.find_element(By.XPATH,"//span[contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1xmvt09') and contains(@class, 'x1lliihq') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'xudqn12') and contains(@class, 'x3x7a5m') and contains(@class, 'x6prxxf') and contains(@class, 'xvq8zen') and contains(@class, 'xo1l8bm') and contains(@class, 'xzsf02u') and contains(@class, 'x1yc453h')][contains(text(), '@')]").text
                except:
                    email = "None"

                print(f"Name: {name}")
                # print(f"Category: {category}")
                # print(f"Location: {location}")

                scraped_data.append({"Name": name,"Page URL": page_link, "Category": category,"Location": location,"Phone Number":phone_number,"Email":email,"Website URL":website_url})
                    # scraped_data.append({"page_url": page_link, "category": category,"location":location,"phone_no":phone_no,"email":email})
                df = pd.DataFrame(scraped_data)
                df.to_csv(f"Data/facebook_{search_input}.csv", index=False)


            except Exception as e:
                print(f"Unexpected error while scraping page {index + 1}: {e}")
        # return scraped_data
    def close(self):
        self.driver.quit()
