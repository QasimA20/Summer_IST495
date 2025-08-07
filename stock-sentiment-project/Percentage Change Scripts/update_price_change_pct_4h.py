import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# rows where 4h percentage change hasn't been calculated yet
cursor.execute("""
    SELECT id, price_at_time, price_4h_later
    FROM headlines
    WHERE 
        price_change_pct_4h IS NULL
        AND price_4h_later IS NOT NULL
        AND date >= CURDATE() - INTERVAL 10 DAY
""")
rows = cursor.fetchall()



for row in rows:
    headline_id = row['id']
    price_now = row['price_at_time']
    price_4h = row.get('price_4h_later')

    # Skip zero prices
    if not price_now or price_now == 0:
        continue

    # Calculating 4-hour percentage change
    pct_4h = round(((price_4h - price_now) / price_now) * 100, 2)

    # Update the database
    cursor.execute("""
        UPDATE headlines
        SET price_change_pct_4h = %s
        WHERE id = %s
    """, (pct_4h, headline_id))
    conn.commit()

    print(f" ID {headline_id}: 4h = {pct_4h}%")

cursor.close()
conn.close()
print(" 4-hour percentage change calculation complete.")
