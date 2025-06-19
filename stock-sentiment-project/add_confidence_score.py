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

        # Count matches
    num_matches = len(matches)

    # Get the sentiment score for this headline
    cursor.execute("SELECT sentiment_score FROM headlines WHERE id = %s", (headline_id,))
    score_result = cursor.fetchone()
    score = score_result['sentiment_score'] if score_result else 0.0

    # New confidence logic based on matches + strength
    #Don’t just trust how many things were said, trust how strong they are too.

    if num_matches == 0:
        confidence = "None"
    elif num_matches == 1:
        confidence = "Low"
    elif num_matches <= 3:
        confidence = "Medium" if abs(score) >= 0.8 else "Low"
    else:
        if abs(score) >= 0.8:
            confidence = "High"
        elif abs(score) >= 0.4:
            confidence = "Medium"
        else:
            confidence = "Low"


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
