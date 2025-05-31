import mysql.connector
import yfinance as yf
import pandas as pd
import time

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",  # update if needed
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Fetch rows that need price updates
cursor.execute("SELECT * FROM headlines WHERE price_at_time IS NULL OR price_1h_later IS NULL LIMIT 5")
rows = cursor.fetchall()
print(f"Found {len(rows)} rows that need price updates.")

for row in rows:
    row_id = row["id"]
    ticker = row["ticker"]
    raw_timestamp = row["date"]

    try:
        # If timestamp is already datetime (not Unix), skip conversion
        if isinstance(raw_timestamp, int):
            timestamp = pd.to_datetime(raw_timestamp, unit='ms')
        else:
            timestamp = pd.to_datetime(raw_timestamp)

        print(f"\nUpdating ID {row_id} | Ticker: {ticker} | Time: {timestamp}")

        # Fetch price at headline time
        ticker_obj = yf.Ticker(ticker)
        hist = ticker_obj.history(interval="1m", period="2d")  # use longer period for buffer

        price_row_now = hist.loc[timestamp] if timestamp in hist.index else None
        price_row_later = hist.loc[timestamp + pd.Timedelta(hours=1)] if (timestamp + pd.Timedelta(hours=1)) in hist.index else None

        if price_row_now is not None and price_row_later is not None:
            price_now = round(price_row_now["Close"], 2)
            price_later = round(price_row_later["Close"], 2)

            update_query = """
                UPDATE headlines
                SET price_at_time = %s, price_1h_later = %s
                WHERE id = %s
            """
            cursor.execute(update_query, (price_now, price_later, row_id))
            conn.commit()
            print(f"✅ Updated: Now = {price_now}, 1h Later = {price_later}")
        else:
            print("❌ Price not found for one or both timestamps.")

    except Exception as e:
        print(f"⚠️ Error updating ID {row_id}: {e}")

    time.sleep(1)  # prevent yfinance rate limiting

cursor.close()
conn.close()
print("✅ All updates complete.")

