import yfinance as yf
import pandas as pd

#create a Ticker object #for example i chose AAPL
ticker_str = "AAPL"
ticker = yf.Ticker(ticker_str)

#This will get the 1-minute interval prices for the past day
df = ticker.history(interval="1m", period="1d")

print(df.head())  # Show rows
print("") #formatting purposes


#Set a random headline's timestamp 
#Ex: "2025-05-21 09:30:00-04:00"
headline_time = "2025-05-21 09:30:00-04:00"
time_to_check = pd.to_datetime(headline_time)

# Download 1-minute price data for AAPL (could be most recent date)
ticker = yf.Ticker("AAPL")

# Trying to find the price at that exact timestamp

if time_to_check in df.index:
    # Use .loc to look up the row in the DataFrame
    price_row = df.loc[time_to_check]
    print(f"\nTicker: {ticker_str}")
    print("Price at headline time:")
    pd.set_option('display.float_format', '{:.2f}'.format) #Number Formatting
    print(price_row)

else:
    print("No exact price match found for this time.")
    # I did this just incase I enter an incorrect time,
    # It will print the 5 closest available times
    print("Closest available timestamps:")
    print(df.index[:5])

# Getting the price one hour later
# I found out about pd.Timedelta while researching how to add time offsets in pandas
time_plus_1hour = time_to_check + pd.Timedelta(hours=1)

 
# This returns the stock price data for that specific minute
if time_plus_1hour in df.index:
    price_1h_later = df.loc[time_plus_1hour]
    print(f"\nTicker: {ticker_str}")
    print("\n Price one hour later:")
    print(price_1h_later)
else:
    print("\n Cannot find price one hour later.")