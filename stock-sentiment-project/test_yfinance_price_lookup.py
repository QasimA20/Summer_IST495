import mysql.connector  
import pandas as pd     
import yfinance as yf   
import time             

#  Connect to MySQL 
conn = mysql.connector.connect(
    host="localhost",           
    user="root",                 
    password="Qasim2004",     
    database="stock_news"       
)
cursor = conn.cursor(dictionary=True)  # gives us each row as a dictionary 

# Find headlines that are missing price info 
cursor.execute("""
    SELECT id, ticker, date
    FROM headlines
    WHERE price_at_time IS NULL OR price_1h_later IS NULL
""")
rows = cursor.fetchall()  # fetch all those rows from the DB

print(f"Found {len(rows)} rows that need price updates.")  # just letting us know how many

# Loop through each row one-by-one 
for row in rows:
    headline_id = row["id"]          # unique ID of row
    ticker_symbol = row["ticker"]    # stock symbol

    # Convert the date column to a proper datetime object
    timestamp = pd.to_datetime(row["date"])

    try:
        # Create a Ticker object from yfinance so we can fetch price data
        ticker = yf.Ticker(ticker_symbol)

        df = ticker.history(interval="1m", period="2d")

        # Initialize our two target prices
        price_at_time = None
        price_1h_later = None

        # Try to get the price at the exact moment the news dropped
        if timestamp in df.index:
            price_at_time = df.loc[timestamp]["Close"]  # use 'Close' price at that minute

        # Now 1 hour later
        timestamp_later = timestamp + pd.Timedelta(hours=1)  # adds 1 hour to original time
        if timestamp_later in df.index:
            price_1h_later = df.loc[timestamp_later]["Close"]

        #Save the prices back into the MySQL database 
        # This SQL query updates the row by ID, inserting both prices
        update_query = """
            UPDATE headlines
            SET price_at_time = %s, price_1h_later = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (price_at_time, price_1h_later, headline_id))
        conn.commit()  # save changes

        print(f" Updated ID {headline_id} | Ticker: {ticker_symbol} | Time: {timestamp}")
    
    except Exception as e:
        #  error message
        print(f" Failed for ID {headline_id} ({ticker_symbol}): {e}")

    # To avoid rate-limiting or getting blocked by yfinance
    time.sleep(1)

cursor.close()  
conn.close()     
print(" All updates complete.")
