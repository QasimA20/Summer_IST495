# All of the price fetching scripts combined into one
# This script updates missing stock price fields in your database, including price_at_time and future prices

import mysql.connector
import yfinance as yf
from datetime import datetime, timedelta
import time
import numpy as np
from pandas.tseries.offsets import BDay
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)
now = datetime.now()
cutoff = pd.Timestamp.now() - BDay(7)


print(f"\n Script started at {now.strftime('%Y-%m-%d %H:%M:%S')}")


# Helper function to fetch stock price at a specific datetime using Yahoo Finance
def get_price_at(ticker, dt):
    try:
        # Try fetching precise 1-minute data (first attempt)
        #data = yf.Ticker(ticker).history(
            #start=dt,
            #end=dt + timedelta(minutes=15),
            #interval="1m"
        #)

        data = yf.Ticker(ticker).history(
            start=dt - timedelta(minutes=30),
            end=dt + timedelta(minutes=30),
            interval="1m"
        )
        

        if not data.empty:
            return round(data["Close"].iloc[0], 2)

        # --- Fallback using your original hourly logic ---
        #start_date = dt.strftime('%Y-%m-%d')
        #end_date = (dt + timedelta(days=1)).strftime('%Y-%m-%d')

        #stock = yf.Ticker(ticker)
        #hist = stock.history(start=start_date, end=end_date, interval='1h')

        # --- Fallback using wider hourly range (fix for missing data) ---
        start_date = (dt - timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = (dt + timedelta(days=2)).strftime('%Y-%m-%d')

        stock = yf.Ticker(ticker)
        print(f"⏳ Fallback for {ticker}: {start_date} → {end_date}")
        hist = stock.history(start=start_date, end=end_date, interval='1h')



        if hist.empty:
            print(f"No price data for fallback ID ({ticker}) at {dt}")
            return None

        # Remove timezone info
        hist.index = hist.index.tz_convert(None)
        ts_naive = dt.replace(tzinfo=None)

        # Find the closest time to the desired timestamp
        closest_row = hist.iloc[np.abs(hist.index - ts_naive).argmin()]
        price = float(round(closest_row['Close'], 2))
        return price

    except Exception as e:
        print(f"Error fetching price for {ticker} at {dt}: {e}")
        return None


max_updates = 250
update_count = 0

# -Fill in price_at_time if missing 
print("Checking for rows missing price_at_time...")
cursor.execute("""
    SELECT id, ticker, date FROM headlines
    WHERE price_at_time IS NULL
    AND ticker IS NOT NULL AND ticker != ''
    ORDER BY date ASC
    LIMIT %s
""", (max_updates,))
rows = cursor.fetchall()


from pandas.tseries.offsets import BDay
import pandas as pd

rows = [row for row in rows if pd.Timestamp(row["date"]) >= cutoff]

for row in rows:
   # price = get_price_at(row["ticker"], row["date"])

    headline_time = row["date"]
    
    # Skip if headline is too recent (less than 1 day ago)
    #if headline_time > now - timedelta(days=1):
        #print(f"Skipping ID {row['id']} ({row['ticker']}) — too recent to fetch price_at_time")
        #continue

    price = get_price_at(row["ticker"], headline_time)

    if price is not None:
        cursor.execute("UPDATE headlines SET price_at_time = %s WHERE id = %s", (float(price), row["id"]))
        conn.commit()
        update_count += 1
        print(f"✅ Updated price_at_time for {row['ticker']} at {row['date']} to {price}\n")

    if update_count >= max_updates:
        break
    time.sleep(1.5)  # Sleep to avoid rate limits

# --- STEP 2: Fill in the rest of the future price fields ---
price_fields = {
    'price_1h_later': timedelta(hours=1),
    'price_4h_later': timedelta(hours=4),
    'price_24h_later': timedelta(hours=24),
    'price_4d_later': BDay(4),      # business days, not calendar days
    'price_7d_later': BDay(7)       # business days, not calendar days
    #'price_4d_later': timedelta(days=4),
    #'price_7d_later': timedelta(days=7)
}

for field, wait_time in price_fields.items():
    if update_count >= max_updates:
        break

    print(f"Checking for rows missing {field}...\n")
    query = f"""
        SELECT id, ticker, date FROM headlines
        WHERE {field} IS NULL
        AND price_at_time IS NOT NULL  -- ✅ skip if we never got the base price
        AND date <= %s
        AND ticker IS NOT NULL AND ticker != ''
        ORDER BY date ASC
        LIMIT %s
    """

    cutoff_time = now - wait_time
    if hasattr(cutoff_time, 'to_pydatetime'):
        cutoff_time = cutoff_time.to_pydatetime()

    cursor.execute(query, (cutoff_time, max_updates - update_count))


    #cursor.execute(query, (now - wait_time, max_updates - update_count))
    rows = cursor.fetchall()

    rows = [row for row in rows if pd.Timestamp(row["date"]) >= cutoff]


    for row in rows:
        #target_time = row["date"] + wait_time
        # Handles both timedelta and BDay correctly
        target_time = wait_time + row["date"]

        price = get_price_at(row["ticker"], target_time)
        if price is not None:
            update_query = f"UPDATE headlines SET {field} = %s WHERE id = %s"
            cursor.execute(update_query, (float(price), row["id"]))
            conn.commit()
            update_count += 1
            print(f"✅ Updated {field} for {row['ticker']} at {target_time} to {price}\n")

        if update_count >= max_updates:
            break
        time.sleep(1.5)  # Wait between API calls to avoid getting blocked

# --- Wrap up ---
cursor.close()
conn.close()
print(f"Done. Total updates: {update_count}")
