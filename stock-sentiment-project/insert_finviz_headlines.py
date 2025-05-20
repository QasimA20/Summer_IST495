#this script now displays the correct tickers for each headline

import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector

# MySQL connection with my password
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004", 
    database="stock_news"
)
cursor = conn.cursor()

# Create the scraper
# I discovered this library after regular requests and Selenium kept getting blocked.
scraper = cloudscraper.create_scraper()
url = "https://finviz.com/news.ashx?v=3" #URL of the Finviz news page
response = scraper.get(url)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser") #Parses the page content
rows = soup.find_all("tr") # This finds all table rows 

print(f"Found {len(rows)} rows!\n")

# This SQL query is written as a Python string 
# and sent to MySQL using the cursor.
# The %s placeholders will be filled in with the actual data
query = """
INSERT IGNORE INTO headlines (ticker, headline, date, price_at_time, price_1h_later)
VALUES (%s, %s, %s, %s, %s)
"""


# Counters to track insert success/failure
# I did this because some of the data was giving me trouble inputting
inserted = 0
skipped = 0

#Loop through each of the rows
for row in rows:
    # Finds the <a> tag linking to a stock's quote page, which contains the ticker
    #I found this out by inspecting the html page
    ticker_tag = row.select_one('a[href^="/quote.ashx?t="]') 
    headline_tag = row.find("a", class_="nn-tab-link") #clickable news headline text

    #skip if some of the data is missing, i will work on finding a solution for this!
    if not ticker_tag or not headline_tag:
        # Save skipped row to CSV
        with open("skipped_headlines.csv", "a") as file:
            file.write(row.get_text(strip=True) + "\n")

        skipped += 1
        continue

    ticker = ticker_tag.get_text(strip=True)

    # Validating the ticker (not finished)
    if not (1 <= len(ticker) <= 5 and ticker.isalpha() and ticker.isupper()):
        # Save skipped row to CSV
        with open("skipped_headlines.csv", "a") as file:
            file.write(row.get_text(strip=True) + "\n")

        skipped += 1
        continue

    headline = headline_tag.get_text(strip=True)
    # Gets the current date and time
    timestamp = datetime.now()

    values = (ticker, headline, timestamp, None, None)
    cursor.execute(query, values)
    inserted += 1
    print(f"[{timestamp}] [{ticker}] {headline}")

# finalize the MySQL changes
conn.commit()
cursor.close()
conn.close() # Close the connection to the database

#summary
print(f"\n Inserted: {inserted} rows")
print(f" Skipped: {skipped} rows due to invalid or missing data")