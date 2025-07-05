#working on fetching prices_at_time of headline
import mysql.connector
import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
import numpy as np

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",  
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Get headlines that still need price updates
cursor.execute("""
    SELECT id, ticker, date 
    FROM headlines 
    WHERE price_at_time IS NULL 
    LIMIT 10
""")
rows = cursor.fetchall()

#Loop through headlines
for row in rows:
    headline_id = row['id']
    ticker = row['ticker']
    timestamp = row['date']

    # Sanitize ticker: remove $ if present and force uppercase
    #ticker = ticker.strip().upper()
    #if ticker.startswith('$'):
        #ticker = ticker[1:]


    try:
        # Skip future timestamps
        if timestamp > datetime.now():
            print(f"Skipping future timestamp for ID {headline_id} ({ticker})")
            continue

        # Format the date range: from the date of the headline to the next day
        # This ensures we capture hourly price data for the entire relevant period
        start_date = timestamp.strftime('%Y-%m-%d')
        end_date = (timestamp + timedelta(days=1)).strftime('%Y-%m-%d')


        # Fetch historical hourly price data from Yahoo Finance
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date, interval='1h')

        if hist.empty:
            print(f"No price data for ID {headline_id} ({ticker})")
            continue

        # Remove timezone info from the index to avoid comparison errors with naive datetime
        hist.index = hist.index.tz_convert(None)
        ts_naive = timestamp.replace(tzinfo=None)

        # Find closest available time to timestamp
        #timezone-naive version
        closest_row = hist.iloc[np.abs(hist.index - ts_naive).argmin()]
        price = float(round(closest_row['Close'], 2))

        # Update MySQL with matched price
        cursor.execute("""
            UPDATE headlines
            SET price_at_time = %s
            WHERE id = %s
        """, (price, headline_id))
        conn.commit()

        print(f" Updated ID {headline_id} ({ticker}) — price_at_time: {price}")
        time.sleep(1.5)

    except Exception as e:
        print(f"Error on ID {headline_id} ({ticker}): {e}")
        continue

cursor.close()
conn.close()
print("Price update (price_at_time) complete!")


