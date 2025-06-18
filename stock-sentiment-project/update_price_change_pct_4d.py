import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Get all rows where we already have both price_at_time and price_4d_later, but did not calculate % yet
cursor.execute("""
    SELECT id, price_at_time, price_4d_later
    FROM headlines
    WHERE price_change_pct_4d IS NULL
      AND price_at_time IS NOT NULL
      AND price_4d_later IS NOT NULL
""")
rows = cursor.fetchall()

for row in rows:
    headline_id = row['id']
    price_now = row['price_at_time']
    price_4d = row['price_4d_later']

    try:
        # Avoid dividing by zero if the price at time was zero just in case!!
        if price_now == 0:
            continue

        # calculating the percentage change
        pct_change = round(((price_4d - price_now) / price_now) * 100, 2)

        # Save that % change back into the headlines table
        cursor.execute("""
            UPDATE headlines
            SET price_change_pct_4d = %s
            WHERE id = %s
        """, (pct_change, headline_id))
        conn.commit()

        print(f" ID {headline_id}: % change_4d = {pct_change}%")

    except Exception as e:
        # Catch any weird errors 
        print(f" Error on ID {headline_id}: {e}")
        continue

# Close everything
cursor.close()
conn.close()
print(" 4-day percentage change update complete.")

