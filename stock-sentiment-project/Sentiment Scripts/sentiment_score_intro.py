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
    "record revenue": 1.0, "jumps": 0.8, "surges": 0.9, "breaks out": 0.8, "AI partnership": 0.7,
    "AI investment": 0.7, "approval": 0.7, "winning": 0.7, "greenlight": 0.7, "jumped": 0.6,
    "soared": 0.6,


    # Mild positive (~0.3 to 0.7)
    "gain": 0.6, "up": 0.4, "buy": 0.4, "strong": 0.6, "launch": 0.5, "debuts": 0.5, 
    "approve": 0.6, "positive": 0.5, "expands": 0.5, "rebranding": 0.3, "innovation": 0.6,
    "supporting inventory growth": 0.5, "financing agreement": 0.4, "debt payoff": 0.5,
    "material transfer agreement": 0.3, "potential acquisition": 0.5, "agreement to merge": 0.5,
    "seeks to merge": 0.4, "agreement with leading": 0.4, "acquire substantially": 0.5,
    "assumption agreement": 0.3, "acquire equity": 0.5, "premium": 0.6, "expansion": 0.5,
    "leading providers": 0.4, "predicting growth": 0.5, "reports growth": 0.5,
    "nasdaq regain compliance": 0.6, "balance sheet increase": 0.5, "total asset increase": 0.5,
    "asset increase": 0.5, "approval phase": 0.6, "pivotal phase": 0.5, "acquire": 0.5,
    "favorable safety": 0.6, "not side affect": 0.5, "visit casino": 0.3, "chinese stimulus": 0.6,
    "innovative ai": 0.6, "higher margin ads": 0.7, "goldman upgrade": 0.7, "morgan upgrade": 0.7,
    "brand leader": 0.5, "authorizing quarterly dividend": 0.6, "quarterly dividend": 0.5,
    "monetary stimulus": 0.7, "rate cuts": 0.5, "big cuts": 0.5, "research contract": 0.4,
    "advanced link terminals": 0.4, "focus digital platforms": 0.5, "investment": 0.4,
    "focus streaming platforms": 0.5, "promising growth": 0.5, "quantum contract award": 0.6,
    "ai force research": 0.6, "enhancing customer support": 0.5, "expanded service network": 0.4,
    "sufficient production capital": 0.5, "improve unit costs": 0.5, "mass production": 0.4,
    "smart device lineup": 0.5, "expansion smart device": 0.4, "interactive experience": 0.4,
    "help kids": 0.3, "make learning more": 0.4, "learning more engaging": 0.4,
    "enhance memory retention": 0.4, "additional earn-out payment": 0.4, "modernize": 0.4,
    "additional payment": 0.3, "owned subsidiary": 0.4, "accelerate business development": 0.6,
    "accelerate development": 0.6, "accelerate growth": 0.6, "proposed purchase price": 0.3,
    "non-binding proposal": 0.3, "pleased to announce": 0.5, "gold drilling completed": 0.4,
    "diamond drill completed": 0.4, "receiving a grant": 0.4, "develop technology": 0.5,
    "commercial agreement": 0.4, "supply alternative": 0.3, "successful launch": 0.6,
    "first income": 0.5, "strategic initiatives": 0.4, "purchase premium": 0.5,
    "growth equity": 0.6, "increased investment": 0.6, "enhancing long-term value": 0.6,
    "donation": 0.4, "partnership": 0.4, "donation and partnership": 0.5, "improves": 0.4,
    "social responsibility": 0.4, "strengthening public image": 0.4, "customer loyalty": 0.4,
    "positive brand awareness": 0.4, "community support": 0.5, "boosting user activity": 0.4,
    "won community": 0.4, "won award": 0.5, "reduce debt": 0.5, "monetizing asset": 0.4,
    "attractive cap": 0.4, "strong support": 0.4, "accelerating development": 0.6,
    "expand treatment": 0.5, "surplus": 0.5, "opens": 0.5, "rebound": 0.4, "boost": 0.5,
     "AI tools": 0.6, "cloud acceleration": 0.6, "first quarter results": 0.4, "agreement": 0.3, "adds": 0.3, 
    "incremental loan": 0.4,  "restructuring": 0.3, "opens facility": 0.4, "expands service": 0.5,
    "resume shipments": 0.4, "collaboration": 0.5, "surprise win": 0.6, "AI expansion": 0.6, "launches AI model": 0.5,
    "declares dividend": 0.3, "declares cash dividend": 0.4, "declares quarterly cash dividend": 0.4,
    "declares monthly cash dividend": 0.4, "dividend": 0.3, "cash dividend": 0.4, "quarterly dividend": 0.3, "monthly dividend": 0.3,
    "preferred dividend": 0.2, "distribution": 0.2, "declares distribution": 0.3, "regular dividend": 0.3, "income fund declares": 0.3,
    "partners with": 0.3, "help banks test AI tools": 0.4, "open its AI models": 0.3, "build first industrial AI cloud": 0.4,
    "maintains healthy fundamentals": 0.4, "attracts": 0.4, "broadens drone delivery service": 0.3, "secures": 0.3,
    "restarts shipments": 0.4, "achieves primary endpoint": 0.5, "bets big": 0.4, "digital makeover": 0.3, "revenue potential": 0.4,
    "expand into": 0.3, "preps overhaul": 0.3, "unveils": 0.2, "raises forecast": 0.4, "bull case for stocks": 0.4,
    "unlock real estate liquidity": 0.3, "highlighting strategic progress": 0.3, "first fully-licensed ai video model": 0.4,
    "strategic integration": 0.3, "enhance digital engagement": 0.3, "midyear outlook": 0.2, "pragmatic optimism": 0.3,
    "top 100 rankings": 0.3, "new numbers": 0.2, "releases strong earnings": 0.3, "releases new product": 0.3,
    "releases new model": 0.3, "releases new feature": 0.3, "releases beta version": 0.2, "releases cloud platform": 0.4,
    "releases software update": 0.3, "releases ai tool": 0.4, "releases guidance": 0.2, "achieves": 0.5, "potential": 0.2,
    "advance ai": 0.4, "thanks": 0.2, "appoints": 0.2, "jumping": 0.5, "climbs": 0.4, "soaring": 0.6, "ranks": 0.3,
    "increases stake": 0.4, "all-time high": 0.5, "grants": 0.2, "introduces": 0.3, "selected": 0.3, "rise": 0.3,
    "integration": 0.3, "grand opening": 0.3, "unveils new": 0.3, "sale": 0.2, "signs deal": 0.4, "new highs": 0.4,
    "restarts": 0.4, "stock repurchase program": 0.5, "acquisition": 0.4, "new corporate name": 0.1, "appoints chief financial officer": 0.2,
    "new cfo": 0.2,  "acquires": 0.4, "joint venture": 0.3, "solar installation": 0.3, "promotion": 0.2,
    "successful renewal": 0.4, "acquisition of infill portfolio": 0.4, "build a hospital": 0.4, "announces new chief": 0.2,



    # Strong Negative 
    "miss": -0.9, "misses": -0.9, "lawsuit": -0.8, "down": -0.6, "cut": -0.5, "recall": -0.8,
    "fall": -0.6, "drop": -0.8, "reverse stock split": -0.9, "restructuring layoffs": -0.8, 
    "executive exits": -0.6, "shareholder lawsuit": -0.9, "trading halted": -1.0, "releases disappointing earnings": -0.6,
    "loss": -0.9, "warns": -0.8, "delay": -0.6, "trap": -0.7,
    "fear": -0.5, "crash": -1.0, "struggle": -0.7, "negative": -0.5, "reverse split": -0.6,
    "compliance ruling": -0.5, "court compliance": -0.5, "layoffs": -0.9, "plummeted": -1.0,
    "fired": -0.9, "investigation": -0.8, "fraud": -1.0, "downgrade": -0.8,
    "short report": -0.7, "selloff": -0.9, "slump": -0.7, "decline": -0.6, "weakened": -0.6,
    "bankruptcy": -1.0, "insider trading": -1.0, "data breach": -0.9, "hacked": -0.8,
    "monopoly": -0.6, "sue": -0.7, "closed stores": -0.8, "delisting": -1.0, "plunges": -1.0, 
    "earnings miss": -0.8, "canceled contract": -0.9, "fined": -0.9, "legal challenge": -0.8,
    "slowing": -0.5, "concerns": -0.4, "delays": -0.6, "uncertainty": -0.5, "feud": -0.6, 
    "dispute": -0.6, "tariff impact": -0.6, "conflict": -0.6, "regulatory hurdles": -0.5, 
    "immigration raid": -0.7, "valuation trap": -0.7, "shutdown": -0.8, "stock looks like it's in trouble": -0.6,
    "releases fraud investigation results": -0.7, "releases bankruptcy statement": -1.0,
    "guidance cut": -0.7, "slashing forecast": -0.8, "warns of slowdown": -0.7, "disappoints investors": -0.6,
    "regulatory probe": -0.8, "investigation launched": -0.7, "ceo steps down": -0.6, "executive departure": -0.6,
    "missed expectations": -0.8, "pulls guidance": -0.8, "dividend suspended": -0.9, "cash burn": -0.7,
    "cutting workforce": -0.8, "restructuring plan": -0.5, "dilution": -0.6, "raises debt": -0.5, "revises outlook lower": -0.7,
    "sec charges": -1.0, "settles fraud charges": -0.9, "product defect": -0.8, "safety issue": -0.7, "delays product launch": -0.6,
    "cutting dividend": -0.8, "material weakness": -0.8, "trash": -0.6, "slashes": -0.6, "tumbles": -0.8, "proposes ban": -0.6,



    #Mild Negs
    "choppy market": -0.4, "anything but trash": -0.5, "being choppier": -0.3, "mulls sale of": -0.2, 
    "gloomy about economy": -0.4, "what the chart says may come next": -0.2,
    "releases weak guidance": -0.5, "releases layoffs plan": -0.4, "releases restated earnings": -0.6,
    "releases downward revision": -0.5, "under pressure": -0.3, "uncertain outlook": -0.4,
    "market headwinds": -0.3, "demand slowdown": -0.4, "weaker-than-expected": -0.4, "execution risk": -0.3,
    "missed deadline": -0.3, "volatile trading": -0.3, "slight miss": -0.3, "tumbles slightly": -0.3,
    "trimming forecast": -0.4, "elevated risk": -0.3, "market volatility": -0.3, "profit warning": -0.4,
    "underperformance": -0.3, "tightening conditions": -0.3, "revises outlook": -0.3, "sales below forecast": -0.4,
    "margins under pressure": -0.4, "rising costs": -0.3, "slower growth": -0.4, "falling short": -0.4, "guidance uncertainty": -0.3,
    "increased competition": -0.3, "fading": -0.3, "inflation": -0.4, "slow": -0.3, "all-time low": -0.5,
    "struggling": -0.6, "worries": -0.4, "new lows": -0.4, "maintains a hold rating": -0.2, "keeps a hold rating": -0.2,
    "reiterates a hold rating": -0.2, "closes public offering": -0.2, "reopening convertible notes": -0.3,
    "pricing of senior notes": -0.3, "debt refinancing": -0.2, "adjournment of annual meeting": -0.3,
    "reschedules earnings release": -0.3, "closing of secondary offering": -0.2, "liquidation of funds": -0.4,
    "senior unsecured notes": -0.3, "announces closing of secondary public offering": -0.3, "announces closing": -0.2,





    # Neutral/monitor for now (0.0)
    "casino": 0.0, "ai drama": 0.0, "china content": 0.0, "short platform": 0.0,
    "short drama": 0.0, 
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


