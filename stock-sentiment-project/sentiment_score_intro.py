import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# Defining custom sentiment dictionary
# Final merged sentiment dictionary (From student list)
sentiment_dict = {

    # Strong positive
    "soars": 2, "surge": 2, "beat": 2, "growth": 2, "record": 2, "outperform": 2, "tops": 2, "celebrates": 2,
    "profit": 2, "developing drug": 2, "developed immunotherapeutic drugs": 2,
    "genetic medicine development": 2, "accelerating genetic medicine": 2, "more promising growth opportunities": 2,
    
    # Mild positive
    "gain": 1, "up": 1, "buy": 1, "strong": 1, "launch": 1, "debuts": 1, "open": 1, "approve": 1,
    "positive": 1, "expands": 1, "rebranding": 1, "supporting inventory growth": 1, "financing agreement": 1,
    "debt payoff": 1, "material transfer agreement": 1, "potential acquisition": 1,
    "agreement to merge": 1, "seeks to merge": 1, "agreement with leading": 1, "acquire substantially": 1,
    "assumption agreement": 1, "acquire equity": 1, "premium": 1, "leading providers": 1,
    "predicting growth": 1, "reports growth": 1, "nasdaq regain compliance": 1, "balance sheet increase": 1,
    "total asset increase": 1, "asset increase": 1, "approval phase": 1, "pivotal phase": 1, "acquire": 1,
    "favorable safety": 1, "not side affect": 1, "visit casino": 1, "chinese stimulus": 1, "innovative ai": 1,
    "higher margin ads": 1, "goldman upgrade": 1, "morgan upgrade": 1, "brand leader": 1,
    "authorizing quarterly dividend": 1, "quarterly dividend": 1, "monetary stimulus": 1,
    "rate cuts": 1, "big cuts": 1, "research contract": 1, "advanced link terminals": 1,
    "focus digital platforms": 1, "focus streaming platforms": 1, "promising growth": 1,
    "quantum contract award": 1, "ai force research": 1, "enhancing customer support": 1,
    "expanded service network": 1, "sufficient production capital": 1, "improve unit costs": 1,
    "mass production": 1, "smart device lineup": 1, "expansion smart device": 1,
    "interactive experience": 1, "help kids": 1, "make learning more": 1, "learning more engaging": 1,
    "enhance memory retention": 1, "additional earn-out payment": 1, "additional payment": 1,
    "owned subsidiary": 1, "accelerate business development": 1, "accelerate development": 1,
    "accelerate growth": 1, "proposed purchase price": 1, "non-binding proposal": 1,
    "pleased to announce": 1, "gold drilling completed": 1, "diamond drill completed": 1,
    "receiving a grant": 1, "develop technology": 1, "commercial agreement": 1,
    "supply alternative": 1, "successful launch": 1, "first income": 1, "strategic initiatives": 1,
    "purchase premium": 1, "growth equity": 1, "increased investment": 1,
    "enhancing long-term value": 1, "donation": 1, "partnership": 1, "donation and partnership": 1,
    "social responsibility": 1, "strengthening public image": 1, "customer loyalty": 1,
    "positive brand awareness": 1, "community support": 1, "boosting user activity": 1,
    "won community": 1, "won award": 1, "reduce debt": 1, "monetizing asset": 1,
    "attractive cap": 1, "strong support": 1, "accelerating development": 1, "expand treatment": 1, "surplus": 1,

    # Negative
    "miss": -2, "misses": -2, "lawsuit": -2, "down": -1, "cut": -1, "recall": -2, "fall": -1, "drop": -2,
    "plunges": -2, "loss": -2, "warns": -2, "delay": -1, "fear": -1, "crash": -3, "struggle": -2, "negative": -1,
    "definitive agreement": -1, "cramer optimistic": -1, "sue": -1, "monopoly": -1,
    "reverse split": -1, "compliance ruling": -1, "court compliance": -1,

    # Neutral/monitor (no score, but matched)
    "casino": 0, "ai drama": 0, "china content": 0, "short platform": 0, "short drama": 0, "announces": 1
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

