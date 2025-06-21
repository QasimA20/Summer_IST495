import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Fetch rows with both price_at_time and price_7d_later 
cursor.execute("""
    SELECT id, price_at_time, price_7d_later
    FROM headlines
    WHERE price_at_time IS NOT NULL
      AND price_7d_later IS NOT NULL
      AND price_change_pct_7d IS NULL
""")
rows = cursor.fetchall()

# Loop and calculate the 7-day % change
for row in rows:
    headline_id = row['id']
    price_now = row['price_at_time']
    price_later = row['price_7d_later']

    #  divide-by-zero errors
    if price_now == 0:
        pct_change = None
    else:
        change = ((price_later - price_now) / price_now) * 100
        pct_change = round(change, 2)

    # update the database 
    cursor.execute("""
        UPDATE headlines
        SET price_change_pct_7d = %s
        WHERE id = %s
    """, (pct_change, headline_id))

    print(f"ID {headline_id}: 7-day change = {pct_change}%")

# Commit
conn.commit()
cursor.close()
conn.close()
print("7-day price change percentages updated.")
