import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# query headlines with price data and keyword matches
query = """
SELECT 
    id, headline, matched_keywords, sentiment_score,
    price_at_time, price_4d_later
FROM headlines
WHERE 
    price_at_time IS NOT NULL 
    AND price_4d_later IS NOT NULL
    AND matched_keywords IS NOT NULL
"""
#dataframe
df = pd.read_sql(query, conn)

# split keywords
def extract_keywords(matched_str):
    if matched_str == "none":
        return []
    # Take the comma-separated keywords and return them as a clean list
    return [kw.strip() for kw in matched_str.split(",")]

# Building keyword-level data for analysis
keyword_data = []
for _, row in df.iterrows():
    keywords = extract_keywords(row['matched_keywords'])
    #simple math calculation
    pct_change = ((row['price_4d_later'] - row['price_at_time']) / row['price_at_time']) * 100

    for kw in keywords:
        keyword_data.append({
            'keyword': kw,
            'price_change_pct_4d': pct_change,
            'sentiment_score': row['sentiment_score']
        })

keyword_df = pd.DataFrame(keyword_data)

# Aggregate performance of each of the keywords
summary = keyword_df.groupby('keyword').agg(
    avg_price_change_pct_4d=('price_change_pct_4d', 'mean'),
    count=('price_change_pct_4d', 'count'),
    avg_sentiment_score=('sentiment_score', 'mean')
).reset_index()

# Only keep keywords seen 2+ times for reliability (more efficient results)
filtered_summary = summary[summary['count'] >= 2].sort_values(by='avg_price_change_pct_4d', ascending=False)



 #Nicely formatted output
print("\nKeyword Impact Analysis on 4-Day Price Change")
print("-" * 72)
print()  # blank line for spacing
print(filtered_summary.to_string(index=False))  # cleaner display with no row numbers
#print(filtered_summary)

# Save as CSV for future analysis
filtered_summary.to_csv("keyword_impact_summary.csv", index=False)

cursor.close()
conn.close()
