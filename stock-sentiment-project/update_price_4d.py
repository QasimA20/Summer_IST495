import mysql.connector
import yfinance as yf
from datetime import datetime, timedelta
import time
import numpy as np

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Only get headlines missing price_4d_later
cursor.execute("""
    SELECT id, ticker, date
    FROM headlines
    WHERE price_4d_later IS NULL
""")
rows = cursor.fetchall()


# Looping through each headline row

for row in rows:
    headline_id = row['id']
    ticker = row['ticker']
    base_time = row['date']

    if base_time > datetime.now():
        print(f" Skipping future-dated headline ID {headline_id}")
        continue

    try:
        # Calculate what the date is 4 days after the headline
        target_date = base_time + timedelta(days=4)

        if target_date > datetime.now():
            print(f" Skipping price_4d_later for ID {headline_id} — date is still in the future")
            continue

         #Define the date range
        start = base_time.strftime('%Y-%m-%d')
        end = (base_time + timedelta(days=5)).strftime('%Y-%m-%d')
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start, end=end)

        if hist.empty:
            print(f" No data found for ID {headline_id} ({ticker})")
            continue

        hist.index = hist.index.tz_convert(None)
        ts_naive = target_date.replace(tzinfo=None)

        #Find the closest available trading date to the target
        closest_idx = np.abs(hist.index - ts_naive).argmin()
        closest_price = round(hist.iloc[closest_idx]['Close'], 2)

        cursor.execute("""
            UPDATE headlines
            SET price_4d_later = %s
            WHERE id = %s
        """, (float(closest_price), headline_id))
        conn.commit()

        print(f" ID {headline_id}: 4d = {closest_price}")
        print()
        time.sleep(1.2)

    except Exception as e:
        print(f" Error on ID {headline_id} ({ticker}): {e}")
        continue

cursor.close()
conn.close()
print(" Done updating price_4d_later!")

