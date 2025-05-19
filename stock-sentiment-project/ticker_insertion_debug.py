# Trial version of headline scraper to test ticker extraction
#Try to use selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Set up ChromeDriver path and options
chromedriver_path = "/Users/qasim/Desktop/chromedriver"
options = Options()
options.add_argument("user-agent=Mozilla/5.0")  # Mimics a real browser

# Launch Chrome
#I found chromedriver online
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Load Finviz news 
driver.get("https://finviz.com/news.ashx?v=3")
time.sleep(5)  # Let the page fully load 

# Parse the HTML
soup = BeautifulSoup(driver.page_source, "html.parser")
rows = soup.find_all("tr") #table row

print(f" Found {len(rows)} rows\n")

# Extract and print ticker + headline from each row
for row in rows:
    # Headlines are in <a> tags
    headline_tag = row.find("a", class_="nn-tab-link")
    headline = headline_tag.get_text(strip=True) if headline_tag else None

    ticker_tag = row.select_one(".stock-news-label") # Searches for any tag with that class
    ticker = ticker_tag.get_text(strip=True) if ticker_tag else "N/A"

    if headline:
        print(f"[{ticker}] {headline}")

driver.quit()

#This script works but is very unreliable, it uses Selenium 
# and often gets blocked or returns 0 rows due to Finviz's bot protection.

