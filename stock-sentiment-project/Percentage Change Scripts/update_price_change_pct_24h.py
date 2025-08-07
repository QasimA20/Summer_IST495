import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# rows where 24h percentage change hasn't been calculated yet
cursor.execute("""
    SELECT id, price_at_time, price_24h_later
    FROM headlines
    WHERE 
        price_change_pct_24h IS NULL
        AND price_24h_later IS NOT NULL
        AND date >= CURDATE() - INTERVAL 10 DAY
""")
rows = cursor.fetchall()


for row in rows:
    headline_id = row['id']
    price_now = row['price_at_time']
    price_24h = row.get('price_24h_later')

   
    # Calculating 24-hour percentage change
    pct_24h = round(((price_24h - price_now) / price_now) * 100, 2)

    # Update
    cursor.execute("""
        UPDATE headlines
        SET price_change_pct_24h = %s
        WHERE id = %s
    """, (pct_24h, headline_id))
    conn.commit()

    print(f" ID {headline_id}: 24h = {pct_24h}%")

cursor.close()
conn.close()
print(" 24-hour percentage change calculation complete.")
