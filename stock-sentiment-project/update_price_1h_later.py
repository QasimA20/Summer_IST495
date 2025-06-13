import mysql.connector
import yfinance as yf
import numpy as np
from datetime import datetime, timedelta
import time

# Connect to your MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Get rows missing the 1-hour-later price
cursor.execute("""
    SELECT id, ticker, date 
    FROM headlines 
    WHERE price_1h_later IS NULL
""")
rows = cursor.fetchall()

print(f"Found {len(rows)} rows to process...\n")

for row in rows:
    headline_id = row['id']
    ticker = row['ticker']
    base_time = row['date']
    target_time = base_time + timedelta(hours=1)  # Shift by 1 hour

    try:
        # this will skip if its in the future
        if target_time > datetime.now():
            print(f" Skipping ID {headline_id} ({ticker}) — 1h target is in the future")
            continue

        # Fetch hourly price data for the day of the target
        start_date = target_time.strftime('%Y-%m-%d')
        end_date = (target_time + timedelta(days=1)).strftime('%Y-%m-%d')

        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date, interval="1h")

        if hist.empty:
            print(f"No data for ID {headline_id} ({ticker})")
            continue

        hist.index = hist.index.tz_convert(None)
        ts_naive = target_time.replace(tzinfo=None)

        #takes the absolute time difference and finds the smallest one
        closest_idx = np.abs(hist.index - ts_naive).argmin()

        # getting the closing price at that closest time
        closest_price = float(round(hist.iloc[closest_idx]['Close'], 2))

        # Update the 1-hour-later price in the database
        cursor.execute("""
            UPDATE headlines
            SET price_1h_later = %s
            WHERE id = %s
        """, (closest_price, headline_id))
        conn.commit()

        print(f" Updated ID {headline_id} ({ticker}) — price_1h_later: {closest_price}")
        time.sleep(1.5)  # Prevent rate limit

    except Exception as e:
        print(f" Error on ID {headline_id} ({ticker}): {e}")
        continue

cursor.close()
conn.close()

print("\n price_1h_later update complete.")
