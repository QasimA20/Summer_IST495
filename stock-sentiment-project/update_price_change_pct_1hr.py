import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# rows where 1h percentage change hasn't been calculated yet
cursor.execute("""
    SELECT id, price_at_time, price_1h_later
    FROM headlines
    WHERE 
        price_change_pct_1h IS NULL AND price_1h_later IS NOT NULL
""")
rows = cursor.fetchall()

for row in rows:
    headline_id = row['id']
    price_now = row['price_at_time']
    price_1h = row.get('price_1h_later')

    # Skip zero prices
    if not price_now or price_now == 0:
        continue

    # Calculating 1-hour percentage change
    pct_1h = round(((price_1h - price_now) / price_now) * 100, 2)

    # Update the database
    cursor.execute("""
        UPDATE headlines
        SET price_change_pct_1h = %s
        WHERE id = %s
    """, (pct_1h, headline_id))
    conn.commit()

    print(f" ID {headline_id}: 1h = {pct_1h}%")

cursor.close()
conn.close()
print("1-hour percentage change calculation complete.")
