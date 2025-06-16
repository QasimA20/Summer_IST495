import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor(dictionary=True)

# THEME DICTIONARY 
# Grouping phrases into broad sentiment themes

sentiment_theme_dict = {
    "merger": ["agreement to merge", "seeks to merge", "definitive agreement", "agreement", "merge", "seeks", "definitive"],
    "acquisition": ["potential acquisition", "acquire substantially", "acquire equity", "acquire outstanding", "assumption agreement", "premium", "acquire", "substantially", "equity", "outstanding", "assumption", "agreement"],
    "growth": ["reports growth", "promising growth", "predicting growth", "growth", "promising", "reports", "predicting"],
    "research": ["research contract", "developing drug", "developed immunotherapeutic drugs", "genetic medicine development", "accelerating genetic medicine", "fully optimized genetic medicine", "contract", "developing", "developed", "genetic", "medicine", "accelerating", "fully optimized"],
    "financials": ["gross margin up", "cash flow increase", "balance sheet increase", "total asset increase", "asset increase", "reduce debt", "debt payoff", "enhancing liquidity", "attractive cap", "gross", "margin", "cash", "flow", "balance", "sheet", "total", "asset", "reduce", "debt", "payoff", "liquidity", "cap"],
    "legal": ["sue", "monopoly", "compliance ruling", "court compliance", "lawsuit", "ruling", "court"],
    "brand": ["rebranding", "brand leader", "positive brand awareness", "positive", "brand", "awareness"],
    "social": ["donation", "partnership", "donation and partnership", "social responsibility", "community support", "strengthening public image", "customer loyalty", "community", "support", "responsibility", "image", "loyalty"],
    "recognition": ["won community", "won award", "award", "won"],
    "support": ["enhancing customer support", "expanded service network", "sufficient production capital", "improve unit costs", "customer", "support", "network", "capital", "production", "improve", "unit", "costs"],
    "ads": ["higher margin ads", "higher margin", "margin", "ads"],
    "dividends": ["authorizing quarterly dividend", "quarterly dividend", "dividend", "quarterly", "authorizing"],
    "stimulus": ["monetary stimulus", "big cuts", "rate cuts", "stimulus", "cuts", "rate"],
    "compliance": ["reverse split", "NASDAQ regain compliance", "compliance", "reverse", "split", "regain"],
    "technology": ["advanced link terminals", "ai force research", "smart device lineup", "interactive experience", "ai", "smart", "device", "interactive", "experience", "advanced", "link", "terminals"],
    "education": ["help kids", "make learning more", "learning more engaging", "enhance memory retention", "learning", "kids", "engaging", "retention", "enhance"],
    "launch": ["successful launch", "first income", "launch", "successful", "first", "income"],
    "investment": ["increased investment", "growth equity", "enhancing long-term value", "investment", "equity", "long-term", "value"],
    "public sector": ["receiving a grant", "grant", "receiving"],
    "strategy": ["strategic initiatives", "initiatives", "strategic"],
    "casino": ["visit casino", "casino", "visit"],
    "media": ["AI drama", "short platform", "short drama", "drama", "platform", "short"],
    "hardware": ["expansion smart device", "mass production", "smart device", "device", "expansion", "mass", "production"],
    "contract": ["quantum contract award", "commercial agreement", "supply alternative", "contract", "commercial", "supply", "alternative", "award"],
    "purchase": ["proposed purchase price", "non-binding proposal", "purchase", "price", "proposal", "non-binding"],
    "award": ["won award", "award", "won"],
    "development": ["accelerate business development", "accelerate development", "accelerate growth", "accelerate", "development"]
}

#fetch headlines
cursor.execute("""
    SELECT id, headline
    FROM headlines
    WHERE sentiment_theme IS NULL
""")
rows = cursor.fetchall()

# process each headline
for row in rows:
    headline_id = row['id']
    headline_text = row['headline'].lower()

    matched_themes = []

    # Looping through each theme and check for keyword matches
    for theme, keywords in sentiment_theme_dict.items():
        for phrase in keywords:
            if phrase in headline_text:
                matched_themes.append(theme)
                break 

   
    if not matched_themes:
        theme_result = "unspecified"
    else:
        theme_result = ", ".join(sorted(set(matched_themes)))

    # update
    cursor.execute("""
        UPDATE headlines
        SET sentiment_theme = %s
        WHERE id = %s
    """, (theme_result, headline_id))
    conn.commit()

    print(f" ID {headline_id} — Theme: {theme_result}\n")


cursor.close()
conn.close()
print(" Sentiment theme tagging complete.")
