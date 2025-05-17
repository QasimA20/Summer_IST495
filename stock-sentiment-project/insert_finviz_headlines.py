from pyfinviz.news import News
import mysql.connector
from datetime import datetime
import re


#Not finished, has errors!
def extract_ticker(headline):
    # Check for tickers in parentheses
    match = re.search(r'\(([A-Z]{1,5})\)', headline) # Look for (A-Z letters, 1 to 5 long)
    if match:
        return match.group(1)
    
    # Otherwise, look for uppercase words (or potential tickers)
    words = headline.split() # this breaks the sentence into individual words
    for word in words:
        if word.isupper() and 1 <= len(word) <= 5: #Looks for all capital letters
            return word
    
    return "N/A"


# STOCKS_NEWS view
news = News(view_option=News.ViewOption.STOCKS_NEWS)

print(news.news_df)  #showing stock-specific headlines

# Extract the DataFrame
df = news.news_df

# MySQL connection with my password
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",  
    database="stock_news"
)
cursor = conn.cursor()

# This SQL query is written as a Python string 
# and sent to MySQL using the cursor.
# The %s placeholders will be filled in with the actual data
query = """
    INSERT INTO headlines (ticker, headline, date, price_at_time, price_1h_later)
    VALUES (%s, %s, %s, %s, %s)
"""

# Iterate through DataFrame rows. It is skipping the index and only using the row data
for _, row in df.iterrows():
    ticker = extract_ticker(row["Headline"]) #extracts the ticker symbol
    headline = row["Headline"]
    date = datetime.now() #current date and time as the timestamp
    price_at_time = None #put it at none for now, not finished
    price_1h_later = None
    values = (ticker, headline, date, price_at_time, price_1h_later)
    cursor.execute(query, values) #Insert the data into the database table

conn.commit()
cursor.close()
conn.close() # Close the connection to the database

print(" Headlines inserted successfully!") #to ensure it runs smoothly


