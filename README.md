# Summer_IST495
Real-time dictionary-based sentiment analysis for stock news headlines (IST 495 Internship)

**Intern: Qasim Ansari**

## Project Overview

This internship project focuses on real-time sentiment analysis of stock market news headlines using a custom-built dictionary-based scoring system.

Unlike black-box machine learning sentiment models, this approach is transparent, explainable, and easily adaptable. The system ingests live headlines, assigns sentiment scores using a curated keyword dictionary, and correlates sentiment with actual stock price movements.

The end product is an interactive Streamlit dashboard that allows users to:

- Explore recent headlines and their sentiment scores

- Track sentiment trends for specific tickers over time

- Compare sentiment with actual price changes at multiple intervals

- Identify top positive/negative keywords driving market tone

- This work combines data engineering, sentiment analysis, and dashboard design into a complete, automated pipeline.

---

## Project Objectives

1. **Build a Real-Time Sentiment Scoring Engine**
   
   - Python scripts ingest live stock headlines from Finviz

   - Headlines are cleaned, tokenized, and scored using a custom sentiment dictionary

   - Scores are scaled between -1 (strongly negative) and +1 (strongly positive)
     

2. **Develop and Maintain a Custom Dictionary**
   
   - Iteratively expanded to capture finance-specific language (e.g., “EPS beat,” “buyback,” “SEC probe”)

   - Includes both individual keywords and multi-word phrases

   - Weighted scoring ensures high-impact terms influence sentiment appropriately
     

3. **Correlate Sentiment with Stock Price Movements**

   - Uses yfinance to retrieve stock prices at: time of headline, 1h, 4h, 24h, 4d, and 7d after

   - Calculates percentage changes to validate sentiment accuracy against real price movement


4. **Design a Visual Dashboard (Jupyter/Streamlit)**  
   Streamlit app with:

   - Ticker-specific sentiment & price trend charts

   - Top keywords for all tickers or a specific stock

   - Market-wide “latest headlines” view with sentiment labels

   - Buy/Hold/Sell recommendations based on sentiment trends

   - Supports date filtering, keyword exploration, and performance summaries

---


## Learning Goals Achieved

- Python & Data Processing – End-to-end ETL workflow from scraping to analysis

- Sentiment Analysis – Designed a transparent, domain-specific scoring system

- Database Integration – MySQL storage and querying for historical headlines

- Data Visualization – Interactive financial dashboard using Streamlit and Altair

- Version Control – Managed a multi-week development cycle using Git/GitHub

- Project Management – Delivered incremental features with weekly progress milestones

---

## Technical Architecture
Data Flow:

1. Scraper (insert_finviz_headlines.py) → Fetches headlines + tickers

2. Database Storage → MySQL table headlines
   
4. Price Fetcher (update_price_xx.py) → Adds historical/future prices at set intervals

5. Sentiment Tagger (analyze_keywords.py) → Scores headlines using dictionary

6. Dashboard (sentiment_dashboard.py) → Visualizes results interactively
   

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python** | Data ingestion, sentiment scoring, price calculations |
| **Pandas** | Text Parsing, cleaning, and transformation |
| **BeautifulSoup** | Web scraping headlines from Finviz |
| **yfinance** | Stock price retrieval |
| **MySQL** | Persistent storage for headlines and price data |
| **Streamlit** | Interactive dashboard front-end |
| **Altair** | Data visualization for sentiment/price trends |
| **Jupyter Notebook** | Exploration, testing, reporting |
| **VS Code** | Development and file structure |
| **GitHub** | Version control and weekly progress sharing |

---

## Setup, Runbook, and TroubleShooting (Detailed)

*A complete, step‑by‑step guide to run this project on macOS or Windows, from fresh clone → dashboard demo*

**Environment Setup**

## Quick Start (Data-first)

> You need data before the dashboard is useful. Do these in order:
> env → DB → insert → prices → sentiment → dashboard.

### Windows (PowerShell)

```powershell
# 0) Create & activate venv, install deps
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --no-cache-dir -r requirements.txt

# 1) Apply DB schema (adds/normalizes columns)
mysql -u root -p stock_news < add_missing_columns.sql

# 2) Set DB env vars for this session
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASS="YourPasswordHere"
$env:DB_NAME="stock_news"

# 3) Insert headlines
python -u "stock-sentiment-project\insert_finviz_headlines.py"

# 4) Fill prices
python -u "Price Scripts\unified_price_scripts.py"

# 5) Tag sentiment
python -u "Sentiment Scripts\sentiment_tagging.py"

# 6) Launch dashboard
streamlit run "Dashboard\sentiment_dashboard.py"
# If streamlit not found: python -m streamlit run "Dashboard\sentiment_dashboard.py" 



