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

#headlines that are missing the 24-hour-later price
cursor.execute("""
    SELECT id, ticker, date
    FROM headlines
    WHERE price_24h_later IS NULL
""")
rows = cursor.fetchall()

# Loop through each headline entry
for row in rows:
    headline_id = row['id']
    ticker = row['ticker']
    base_time = row['date']  # Time when headline was published

    if base_time > datetime.now():
        print(f" Skipping future-dated headline ID {headline_id}")
        continue



    try:
        # Calculate 24 hours after the headline
        target_time = base_time + timedelta(hours=24)

        # if time is still in the future
        if target_time > datetime.now():
            print(f" Skipping price_24h_later for ID {headline_id} — time is still in the future")
            continue

        # Defining the historical range to fetch from yfinance
        start = base_time.strftime('%Y-%m-%d')
        end = (base_time + timedelta(days=2)).strftime('%Y-%m-%d')
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start, end=end, interval='1h')

        if hist.empty:
            print(f" No data found for ID {headline_id} ({ticker})")
            continue

        # Convert timestamp to timezone-naive for comparison
        hist.index = hist.index.tz_convert(None)
        ts_naive = target_time.replace(tzinfo=None)

        closest_idx = np.abs(hist.index - ts_naive).argmin()
        closest_price = round(hist.iloc[closest_idx]['Close'], 2)

        cursor.execute("""
            UPDATE headlines
            SET price_24h_later = %s
            WHERE id = %s
        """, (float(closest_price), headline_id))
        conn.commit()

        print(f" ID {headline_id}: 24h = {closest_price}")
        print()
        time.sleep(1.2)  #  avoid rate limiting

    except Exception as e:
        print(f" Error on ID {headline_id} ({ticker}): {e}")
        continue

cursor.close()
conn.close()
print(" Done updating price_24h_later!")
