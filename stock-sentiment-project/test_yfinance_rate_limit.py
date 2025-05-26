import yfinance as yf
import pandas as pd
import time

# Format pandas output so float numbers show normally
pd.set_option('display.float_format', '{:.2f}'.format)

# Sample data to simulate headlines
# Each dictionary contains a stock ticker and the timestamp 
test_data = [
    {"ticker": "AAPL", "time": "2025-05-23 09:30:00-04:00"},
    {"ticker": "MSFT", "time": "2025-05-23 09:30:00-04:00"},
    {"ticker": "NVDA", "time": "2025-05-23 09:30:00-04:00"},
    {"ticker": "TSLA", "time": "2025-05-23 09:30:00-04:00"},
    {"ticker": "GOOG", "time": "2025-05-23 09:30:00-04:00"},
]


# function that fetches the price at a given time for a given stock ticker
def get_price_at_time(ticker_symbol, timestamp):
    try:
        # Create ticker object
        ticker = yf.Ticker(ticker_symbol)
        # Download 1-minute price data for the past 1 day
        df = ticker.history(interval="1m", period="1d")

        # Convert timestamp 
        time_to_check = pd.to_datetime(timestamp)

        # Checking if the exact time exists in the DataFrame index 
        if time_to_check in df.index: 
            return df.loc[time_to_check] 
        else:
            return " No price for that exact timestamp" 
    except Exception as e:
        return f" Error: {e}"  # invalid ticker or error issue

# Loop through each test entry
for item in test_data:
    ticker_symbol = item["ticker"]
    headline_time = item["time"]

    print(f"\n Fetching price for {ticker_symbol} at {headline_time}...")
    # Call the function to get the price at that time
    result = get_price_at_time(ticker_symbol, headline_time)

    # Check if a price row was returned
    if isinstance(result, pd.Series):
        print(f"\n Price data for {ticker_symbol}:\n{result}")
    else:
        print(result)

    #This will make it wait 1 second before making/printing the next request to avoid hitting rate limits or getting blocked
    print(" Waiting 1 second before next request...\n")
    time.sleep(1)
