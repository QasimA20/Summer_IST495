#this script now displays the correct tickers for each headline

import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import mysql.connector
import pandas as pd
import re

# MySQL connection with my password
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004", 
    database="stock_news"
)
cursor = conn.cursor()

# Load valid tickers from finviz.csv
valid_tickers = set(pd.read_csv("/Users/qasim/Documents/Analyzer Internship Project/Summer_IST495/stock-sentiment-project/finviz.csv")["Ticker"])

# Create the scraper
# I discovered this library after regular requests and Selenium kept getting blocked.
scraper = cloudscraper.create_scraper()
url = "https://finviz.com/news.ashx?v=3"  # URL of the Finviz news page
response = scraper.get(url)

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")  # Parses the page content
rows = soup.find_all("tr")  # This finds all table rows 

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

# Loop through each of the rows
for row in rows:
    # Finds the <a> tag linking to a stock's quote page, which contains the ticker
    # I found this out by inspecting the html page
    ticker_tag = row.select_one('a[href^="/quote.ashx?t="]') 
    headline_tag = row.find("a", class_="nn-tab-link")  # clickable news headline text

    # Skip if some of the data is missing, I will work on finding a solution for this!
    if not ticker_tag or not headline_tag:
        # Save skipped row to CSV
        with open("skipped_headlines.csv", "a") as file:
            file.write(row.get_text(strip=True) + "\n")
        skipped += 1
        continue

    ticker = ticker_tag.get_text(strip=True)

    # Validate that the ticker is in our known list
    if ticker not in valid_tickers:
        with open("skipped_headlines.csv", "a") as file:
            file.write(row.get_text(strip=True) + "\n")
        skipped += 1
        continue

    headline = headline_tag.get_text(strip=True)


    # Scraping the *relative time* text and subtracting that amount from the current time.
    #First I I located the <td> tag containing the time info.
    # To convert this to a real timestamp, I subtract a timedelta from datetime.now()
    ## Now, each row in the MySQL database reflects the actual moment the news likely broke,

    time_tag = row.find("td")
    if time_tag:
        time_str = time_tag.get_text(strip=True).lower()
        try:
            if "min" in time_str:
                minutes = int(re.search(r"(\d+)", time_str).group(1))
                timestamp = datetime.now() - timedelta(minutes=minutes)
            elif "hour" in time_str:
                hours = int(re.search(r"(\d+)", time_str).group(1))
                timestamp = datetime.now() - timedelta(hours=hours)
            else:
                timestamp = datetime.now()  # fallback for unknown format
        except Exception as e:
            print(f" Failed to parse time: '{time_str}' — {e}")
            skipped += 1
            continue
    else:
        skipped += 1
        continue

    print(f"Extracted time from Finviz: {timestamp}")
    values = (ticker, headline, timestamp, None, None)
    cursor.execute(query, values)
    inserted += 1
    print(f"[{timestamp}] [{ticker}] {headline}")

# Finalize the MySQL changes
conn.commit()
cursor.close()
conn.close()  # Close the connection to the database

# Summary
print(f"\n Inserted: {inserted} rows")
print(f" Skipped: {skipped} rows due to invalid or missing data")