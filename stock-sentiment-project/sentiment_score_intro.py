import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Defining custom sentiment dictionary
# I will update this over time!

sentiment_dict = {

    # Positive sentiment
    "beat": 2,
    "soars": 2,
    "surge": 2,
    "gain": 1,
    "up": 1,
    "buy": 1,
    "strong": 1,
    "growth": 2,
    "rises": 1,
    "launch": 1,
    "debuts": 1,
    "celebrates": 2,
    "record": 2,
    "expands": 1,
    "tops": 2,
    "profit": 2,
    "outperform": 2,
    "open": 1,
    "approve": 1,
    "positive": 1,

    # Negative sentiment
    "miss": -2,
    "misses": -2,
    "lawsuit": -2,
    "down": -1,
    "cut": -1,
    "recall": -2,
    "fall": -1,
    "drop": -2,
    "plunges": -2,
    "loss": -2,
    "warns": -2,
    "delay": -1,
    "fear": -1,
    "crash": -3,
    "struggle": -2,
    "negative": -1
}

# update headlines
cursor.execute("""
    SELECT id, headline
    FROM headlines
    WHERE sentiment_score IS NULL AND matched_keywords IS NULL
""")
rows = cursor.fetchall()

for row in rows:
    headline_id = row['id']
    headline = row['headline'].lower()

    score = 0
    matches = []

    # Count how many times each keyword appears in the headline
    for keyword, value in sentiment_dict.items():
        count = headline.count(keyword)
        if count > 0:
            score += count * value # multiply by how many times it appears (this is to add more context to the sentiment)
            matches.extend([keyword] * count)  # Repeat the word if it appears multiple times

    matched_str = ", ".join(matches) if matches else "none"

    # Save sentiment score
    cursor.execute("""
        UPDATE headlines
        SET sentiment_score = %s,
            matched_keywords = %s
        WHERE id = %s
    """, (score, matched_str, headline_id))
    conn.commit()

    print(f" ID {headline_id}: score = {score}, keywords = {matched_str}")


cursor.close()
conn.close()
print(" Matched Keywords and Sentiment Scoring complete!")

