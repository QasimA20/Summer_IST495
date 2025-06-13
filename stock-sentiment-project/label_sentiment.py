import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Find headlines with score but missing its label
cursor.execute("""
    SELECT id, sentiment_score
    FROM headlines
    WHERE sentiment_score IS NOT NULL AND sentiment_label IS NULL
""")
rows = cursor.fetchall()

for row in rows:
    headline_id = row['id']
    score = row['sentiment_score']

    # Converting the score to label
    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    cursor.execute("""
        UPDATE headlines
        SET sentiment_label = %s
        WHERE id = %s
    """, (label, headline_id))
    conn.commit()

    print(f" Labeled ID {headline_id} — {label}")

cursor.close()
conn.close()
print(" Sentiment labeling complete.")
