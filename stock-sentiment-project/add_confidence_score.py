import mysql.connector
import time


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

cursor.execute("""
    SELECT id, matched_keywords
    FROM headlines
    WHERE sentiment_score IS NOT NULL
      AND matched_keywords IS NOT NULL
      AND sentiment_confidence IS NULL
""")
rows = cursor.fetchall()

for row in rows:
    headline_id = row['id']
    matched = row['matched_keywords']

    # this will convert the matched keywords from string to a list
    matches = matched.split(',') if matched.strip() else []


    # Count how many keywords were matched and then assign it a confidence level
    
    num_matches = len(matches)
    if num_matches == 0:
        confidence = "None"
    elif num_matches == 1:
        confidence = "Low"
    elif num_matches <= 3:
        confidence = "Medium"
    else:
        confidence = "High"

    try:
        # Update the sentiment_confidence column in the database
        cursor.execute("""
            UPDATE headlines
            SET sentiment_confidence = %s
            WHERE id = %s
        """, (confidence, headline_id))
        conn.commit()

        print(f" ID {headline_id}: {confidence} confidence based on {num_matches} matches.")

    except Exception as e:
        print(f" Error on ID {headline_id}: {e}")
        continue

cursor.close()
conn.close()
print("Confidence scoring complete.")
