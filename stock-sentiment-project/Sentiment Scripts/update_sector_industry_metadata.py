import pandas as pd
import mysql.connector


# Finviz CSV file that contains ticker metadata
#finviz_df = pd.read_csv('finviz.csv')
finviz_df = pd.read_csv('data/finviz.csv')


# This ensures it aligns with how tickers are stored in MySQL headlines table
finviz_df.rename(columns={'Ticker': 'ticker'}, inplace=True)
finviz_df['ticker'] = finviz_df['ticker'].str.upper()



conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor()

# Looping through each ticker in the metadata CSV and update missing sector/industry
for _, row in finviz_df.iterrows():
    ticker = row['ticker']
    sector = row.get('Sector')
    industry = row.get('Industry')

    update_query = """
    UPDATE headlines
    SET sector = %s,
        industry = %s
    WHERE ticker = %s AND (sector IS NULL OR sector = '')
    """
    cursor.execute(update_query, (sector, industry, ticker))

conn.commit()
cursor.close()
conn.close()

print(" Sector and industry fields updated from finviz.csv.")
