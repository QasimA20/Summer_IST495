import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",       
    password="Qasim2004",  
    database="stock_news"
)

cursor = conn.cursor(dictionary=True)

# Query to get headline IDs and percentage changes
cursor.execute("""
    SELECT id, 
           price_change_pct_1h,
           price_change_pct_4h,
           price_change_pct_24h,
           price_change_pct_4d,
           price_change_pct_7d
    FROM headlines
""")

rows = cursor.fetchall()

def label_change(pct_change):
    """Classify the percent change """
    if pct_change is None:
        return None
    elif pct_change > 1.0:
        return "Up"
    elif pct_change < -1.0:
        return "Down"
    else:
        return "Neutral"

# Iterate through each row and apply the label logic
for row in rows:
    headline_id = row['id']
    labels = {
        "price_label_1h": label_change(row['price_change_pct_1h']),
        "price_label_4h": label_change(row['price_change_pct_4h']),
        "price_label_24h": label_change(row['price_change_pct_24h']),
        "price_label_4d": label_change(row['price_change_pct_4d']),
        "price_label_7d": label_change(row['price_change_pct_7d']),
    }

    # Build dynamic update query
    update_query = """
        UPDATE headlines
        SET price_label_1h = %s,
            price_label_4h = %s,
            price_label_24h = %s,
            price_label_4d = %s,
            price_label_7d = %s
        WHERE id = %s
    """
    values = (
        labels['price_label_1h'],
        labels['price_label_4h'],
        labels['price_label_24h'],
        labels['price_label_4d'],
        labels['price_label_7d'],
        headline_id
    )

    cursor.execute(update_query, values)
    conn.commit()
    print(f"Labeled ID {headline_id} - {labels}")

cursor.close()
conn.close()
