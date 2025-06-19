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

    # Strong positive (~1.0)
    "soars": 1.0, "surge": 1.0, "beat": 1.0, "growth": 0.95, "record": 1.0, "outperform": 1.0, 
    "tops": 0.9, "celebrates": 0.9, "profit": 0.95, "developing drug": 1.0,
    "developed immunotherapeutic drugs": 1.0, "genetic medicine development": 1.0, 
    "accelerating genetic medicine": 1.0, "more promising growth opportunities": 0.95,

    # Mild positive (~0.3 to 0.7)
    "gain": 0.6, "up": 0.4, "buy": 0.4, "strong": 0.6, "launch": 0.5, "debuts": 0.5, 
    "approve": 0.6, "positive": 0.5, "expands": 0.5, "rebranding": 0.3, 
    "supporting inventory growth": 0.5, "financing agreement": 0.4, "debt payoff": 0.5,
    "material transfer agreement": 0.3, "potential acquisition": 0.5, "agreement to merge": 0.5,
    "seeks to merge": 0.4, "agreement with leading": 0.4, "acquire substantially": 0.5,
    "assumption agreement": 0.3, "acquire equity": 0.5, "premium": 0.6, 
    "leading providers": 0.4, "predicting growth": 0.5, "reports growth": 0.5,
    "nasdaq regain compliance": 0.6, "balance sheet increase": 0.5, "total asset increase": 0.5,
    "asset increase": 0.5, "approval phase": 0.6, "pivotal phase": 0.5, "acquire": 0.5,
    "favorable safety": 0.6, "not side affect": 0.5, "visit casino": 0.3, "chinese stimulus": 0.6,
    "innovative ai": 0.6, "higher margin ads": 0.7, "goldman upgrade": 0.7, "morgan upgrade": 0.7,
    "brand leader": 0.5, "authorizing quarterly dividend": 0.6, "quarterly dividend": 0.5,
    "monetary stimulus": 0.7, "rate cuts": 0.5, "big cuts": 0.5, "research contract": 0.4,
    "advanced link terminals": 0.4, "focus digital platforms": 0.5,
    "focus streaming platforms": 0.5, "promising growth": 0.5, "quantum contract award": 0.6,
    "ai force research": 0.6, "enhancing customer support": 0.5, "expanded service network": 0.4,
    "sufficient production capital": 0.5, "improve unit costs": 0.5, "mass production": 0.4,
    "smart device lineup": 0.5, "expansion smart device": 0.4, "interactive experience": 0.4,
    "help kids": 0.3, "make learning more": 0.4, "learning more engaging": 0.4,
    "enhance memory retention": 0.4, "additional earn-out payment": 0.4,
    "additional payment": 0.3, "owned subsidiary": 0.4, "accelerate business development": 0.6,
    "accelerate development": 0.6, "accelerate growth": 0.6, "proposed purchase price": 0.3,
    "non-binding proposal": 0.3, "pleased to announce": 0.5, "gold drilling completed": 0.4,
    "diamond drill completed": 0.4, "receiving a grant": 0.4, "develop technology": 0.5,
    "commercial agreement": 0.4, "supply alternative": 0.3, "successful launch": 0.6,
    "first income": 0.5, "strategic initiatives": 0.4, "purchase premium": 0.5,
    "growth equity": 0.6, "increased investment": 0.6, "enhancing long-term value": 0.6,
    "donation": 0.4, "partnership": 0.4, "donation and partnership": 0.5,
    "social responsibility": 0.4, "strengthening public image": 0.4, "customer loyalty": 0.4,
    "positive brand awareness": 0.4, "community support": 0.5, "boosting user activity": 0.4,
    "won community": 0.4, "won award": 0.5, "reduce debt": 0.5, "monetizing asset": 0.4,
    "attractive cap": 0.4, "strong support": 0.4, "accelerating development": 0.6,
    "expand treatment": 0.5, "surplus": 0.5,

    # Negative (re-weighted and expanded)
    "miss": -0.9, "misses": -0.9, "lawsuit": -0.8, "down": -0.6, "cut": -0.5, "recall": -0.8,
    "fall": -0.6, "drop": -0.8, "plunges": -1.0, "loss": -0.9, "warns": -0.8, "delay": -0.6,
    "fear": -0.5, "crash": -1.0, "struggle": -0.7, "negative": -0.5, "reverse split": -0.6,
    "compliance ruling": -0.5, "court compliance": -0.5, "layoffs": -0.9,
    "fired": -0.9, "investigation": -0.8, "fraud": -1.0, "downgrade": -0.8,
    "short report": -0.7, "selloff": -0.9, "slump": -0.7, "decline": -0.6, "weakened": -0.6,
    "bankruptcy": -1.0, "insider trading": -1.0, "data breach": -0.9, "hacked": -0.8,
    "monopoly": -0.6, "sue": -0.7, "closed stores": -0.8, "delisting": -1.0,
    "earnings miss": -0.8, "canceled contract": -0.9, "fined": -0.9, "legal challenge": -0.8,

    # Neutral/monitor (0.0)
    "casino": 0.0, "ai drama": 0.0, "china content": 0.0, "short platform": 0.0,
    "short drama": 0.0, "announces": 0.0
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

    matched_scores = []
    matches = []

    for keyword, value in sentiment_dict.items():
        count = headline.count(keyword)
        if count > 0:
            matched_scores.extend([value] * count)  # Add the score N times
            matches.extend([keyword] * count)

    if matched_scores:
        score = round(sum(matched_scores) / len(matched_scores), 3)  # use average
        matched_str = ", ".join(matches)
    else:
        score = 0.0
        matched_str = "none"

    # Save sentiment score
    cursor.execute("""
        UPDATE headlines
        SET sentiment_score = %s,
            matched_keywords = %s
        WHERE id = %s
    """, (score, matched_str, headline_id))
    conn.commit()

    print(f"ID {headline_id}: score = {score}, keywords = {matched_str}")


