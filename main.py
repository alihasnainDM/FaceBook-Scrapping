from Scripts.facebook_scraper import FacebookScraper
from Scripts.data_handler import DataHandler
from dotenv import load_dotenv
import os

load_dotenv()

def main():

    email = os.environ.get("F_EMAIL") 
    password = os.environ.get("F_PASSWORD") 

    search_input = "Restaurants"   
    
    page_url = f"https://www.facebook.com/search/pages/?q={search_input}"

    scraper = FacebookScraper(email, password)
    data_handler = DataHandler()

    try:
        # scraper.login()
        # print("loggedIn ...")
        pages_data = scraper.scrape_pages(page_url,search_input)
        # if pages_data:
        #     data_handler.save_to_csv(pages_data,filename=f"facebook_{search_input}.csv")
        # else:
        #     print("No Data found")
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
