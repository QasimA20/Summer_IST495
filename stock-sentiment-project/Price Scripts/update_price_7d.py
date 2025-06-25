import mysql.connector
import yfinance as yf
from datetime import datetime, timedelta
import time
import numpy as np

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# headlines that are missing a price 7 days later
cursor.execute("""
    SELECT id, ticker, date
    FROM headlines
    WHERE price_7d_later IS NULL
""")
rows = cursor.fetchall()

for row in rows:
    headline_id = row['id']
    ticker = row['ticker']
    base_time = row['date']

    #  Skip (precautionary)
    if base_time > datetime.now():
        print(f" Skipping future-dated headline ID {headline_id}")
        continue

    try:
        # Calculating the date exactly 7 days after the headline was posted
        target_date = base_time + timedelta(days=7)

        # If it hasn't been 7 days yet, skip it
        if target_date > datetime.now():
            print(f" Skipping price_7d_later for ID {headline_id} — date is still in the future")
            continue

        # Fetching stock data from the original date to a few days after the 7-day mark
        start = base_time.strftime('%Y-%m-%d')
        end = (base_time + timedelta(days=8)).strftime('%Y-%m-%d')
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start, end=end)

        if hist.empty:
            print(f" No data found for ID {headline_id} ({ticker})")
            continue

        # Remove timezone info to avoid mismatch errors
        hist.index = hist.index.tz_convert(None)

        #making the target datetime timezone-naive
        ts_naive = target_date.replace(tzinfo=None)

        closest_idx = np.abs(hist.index - ts_naive).argmin()
        closest_price = round(hist.iloc[closest_idx]['Close'], 2)

        # Store the value in the database
        cursor.execute("""
            UPDATE headlines
            SET price_7d_later = %s
            WHERE id = %s
        """, (float(closest_price), headline_id))
        conn.commit()

        print(f" ID {headline_id}: 7d = {closest_price}")
        print()  # formatting

        # rate-limiting 
        time.sleep(1.2)

    except Exception as e:
        print(f" Error on ID {headline_id} ({ticker}): {e}")
        continue

#  Done processing
cursor.close()
conn.close()
print(" Done updating price_7d_later!")
