# Summer_IST495
Real-time dictionary-based sentiment analysis for stock news headlines (IST 495 Internship)

**Intern: Qasim Ansari**

**Email: qia5020@psu.edu**

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


**Prerequisites**

- Python 3.11 (recommended) / 64‑bit on Windows

- MySQL Server (local OK)

- pip and python -m venv

---

**Environment Setup**

> You need data before the dashboard is useful. Do these in order:
> env → DB → insert → prices → sentiment → dashboard.


*Windows (PowerShell)*

```powershell
# 0) Create & activate venv, install deps
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --no-cache-dir -r requirements.txt

# 1) Apply DB schema (adds/normalizes columns)
First create the table(s) using **stock_sentiment_schema.sql**, then normalize columns with **add_missing_columns.sql**.
mysql -u root -p stock_news < add_missing_columns.sql


# 2) Set DB env vars for this session
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASS="YourPasswordHere!"
$env:DB_NAME="stock_news"

# 3) Insert headlines **(best during market hours 9:30–16:00 ET)**
python -u "stock-sentiment-project\insert_finviz_headlines.py"

# 4) Fill prices
python -u "Price Scripts\unified_price_scripts.py"

# 5) Compute percentage changes (required by dashboard)
python -u "Price Scripts/<your_pct_change_script.py>"

# 6) Tag sentiment
python -u "Sentiment Scripts\sentiment_score_intro.py"

# 7) Launch dashboard
streamlit run "dashboard\sentiment_dashboard.py"
# If streamlit not found: python -m streamlit run "dashboard\sentiment_dashboard.py"
```

*MacOS*
```
# 0) Create & activate venv, install deps
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --no-cache-dir -r requirements.txt

# 1) Apply DB schema (adds/normalizes columns)
mysql -u root -p stock_news < add_missing_columns.sql

# 2) Set DB env vars for this session
export DB_HOST="localhost"; export DB_USER="root"; export DB_PASS="<YOUR_PASSWORD_HERE>"; export DB_NAME="stock_news"

# 3) Insert headlines  (best during market hours 9:30–16:00 ET)
python stock-sentiment-project/insert_finviz_headlines.py

# 4) Fill absolute prices
python "Price Scripts/unified_price_scripts.py"

# 5) Compute percentage changes (required by dashboard)
python "Price Scripts/<your_pct_change_script.py>"

# 6) Tag sentiment
python "Sentiment Scripts/sentiment_tagging.py"

# 7) Launch dashboard (after ~1–2 trading days of data)
python -m streamlit run Dashboard/sentiment_dashboard.py
```

*Configuration: Database Credentials (do this first)**
Don’t use someone else’s password. Every script should read credentials from environment variables so each user supplies their own. Pick one method:

Set environment variables (recommended)
*Windows (PowerShell)*
```
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASS="<YOUR_PASSWORD_HERE>"
$env:DB_NAME="stock_news"
```

*MacOS/Linux*
```
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASS="<YOUR_PASSWORD_HERE>"
export DB_NAME="stock_news"
```
These apply only to the current terminal session. Open a new terminal → set them again 

---

**Database Setup**
1) Create DB & user (example)
```
CREATE DATABASE IF NOT EXISTS stock_news;
-- CREATE USER 'root'@'localhost' IDENTIFIED BY 'YourPasswordHere';
-- GRANT ALL PRIVILEGES ON stock_news.* TO 'root'@'localhost';
```

2) Apply schema/migrations

Make sure to create the table(s) using **stock_sentiment_schema.sql**, then normalize columns with **add_missing_columns.sql**.

**MySQL Workbench (GUI)**
- Open **stock_sentiment_schema.sql** → make sure the default schema is **stock_news** (double-click it in the left panel so it’s bold) → **Run** (⚡️).
  - The file includes `USE stock_news;` so queries target the correct database. If your DB name is different, edit that line.
- Open **add_missing_columns.sql** → **Run** (⚡️).  
  This adds any missing columns and switches defaults to `NULL` without touching existing data.

**CLI (either OS)**
```bash
# Create tables and point to the right DB
mysql -u root -p < stock_sentiment_schema.sql

# Then add/normalize any missing columns
mysql -u root -p stock_news < add_missing_columns.sql
Workbench: Open → run (⚡️)
```

- *Verify*
```
USE stock_news;
SHOW TABLES;
DESCRIBE headlines;
SELECT COUNT(*) AS rows_in_headlines FROM headlines;
```


3) Environment variables
   
*Windows*
```
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASS="YourPasswordHere"
$env:DB_NAME="stock_news"
```

*MacOS*
```
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASS="YourPasswordHere"
export DB_NAME="stock_news"
```
---

**CSV Path Note (Finviz)**

Mac + cron: absolute path like /Users/qasim/finviz.csv for reliability when run by cron.

Windows/manual: use data/finviz.csv inside the repo.

---

## Runbook — Scripts
**1) Insert Headlines**

- Windows
```
python -u "stock-sentiment-project\insert_finviz_headlines.py"
```

- MacOS
```
python stock-sentiment-project/insert_finviz_headlines.py
```


**2) Unified Price Update**

- Windows
```
python -u "Price Scripts\unified_price_scripts.py"
```

- MacOS
```
python "Price Scripts/unified_price_scripts.py"
```


**3) Sentiment Tagging**

- Windows
```
python -u "Sentiment Scripts\sentiment_tagging.py"
```

- MacOS
```
python "Sentiment Scripts/sentiment_tagging.py"
```


**4) Price Change Percentages**

- Windows
```

```

- MacOS
```

```


**4) Dashboard (Streamlit)**

- Windows
```
streamlit run "Dashboard\sentiment_dashboard.py"
# If streamlit not found:
python -m streamlit run "Dashboard\sentiment_dashboard.py"
```

- MacOS
```
python -m streamlit run Dashboard/sentiment_dashboard.py
```


---

## Scheduling (optional)

macOS (cron)
```
*/30 9-16 * * 1-5 /usr/bin/env bash -lc 'cd /path/to/Summer_IST495 && source .venv/bin/activate && python stock-sentiment-project/insert_finviz_headlines.py >> ~/Desktop/cron_output.log 2>&1'
```

---


## TroubleShooting


- No module named rpds.rpds
```
.\.venv\Scripts\activate
python -m pip install --no-cache-dir rpds-py==0.18.1
```

- No module named pyarrow.lib
```
.\.venv\Scripts\activate
python -m pip uninstall -y pyarrow
python -m pip install --no-cache-dir pyarrow==14.0.2
```


- NumPy ABI error (module compiled using NumPy 1.x cannot run in NumPy 2.0.x)
```
.\.venv\Scripts\activate
python -m pip uninstall -y numpy
python -m pip install "numpy==1.26.4"
python -m pip install --force-reinstall --no-cache-dir pandas==2.2.2 pyarrow==14.0.2
```

- Windows _cffi_backend error (curl_cffi/yfinance)
```
.\.venv\Scripts\activate
python -m pip uninstall -y cffi
python -m pip install cffi==1.16.0
python -m pip install --force-reinstall curl_cffi==0.13.0
```

- Wrong Python/env (packages “installed” but still missing)
```
.\.venv\Scripts\activate
python -c "import sys; print(sys.executable)"
where python
where pip
```
Ensure Streamlit is using the same interpreter shown above.


---

## Data Dictionary (key fields)

- id (PK, INT)
- ticker — Stock ticker symbol
- headline — News headline text
- date — Headline timestamp (UTC/local normalized by script)
- price_at_time — Price at headline timestamp
- price_*_later — Absolute prices at 1h, 4h, 24h, 4d, 7d after
- price_change_pct_* — Percentage changes vs price_at_time
- sentiment_score — average dictionary score in [-1, 1]
- matched_keywords — JSON list of matched terms/phrases
- sentiment_confidence — label: low|medium|high
- confidence_score — numeric confidence 0–1

---

## Database Schema (headlines)

Key fields used by scripts & dashboard:

- ticker (VARCHAR)

- headline (TEXT)

- date (DATETIME)

- price_at_time (DECIMAL)

- price_1h_later, price_4h_later, price_24h_later, price_4d_later, price_7d_later (DECIMAL, NULL by default)

- price_change_pct_1h, price_change_pct_4h, price_change_pct_24h, price_change_pct_4d, price_change_pct_7d (DECIMAL, NULL by default)

- sentiment_score (DECIMAL in [-1,1], NULL by default)

- matched_keywords (TEXT, NULL by default)

- sentiment_confidence (VARCHAR(32), e.g., low|medium|high)

- confidence_score (DECIMAL(4,3), numeric 0–1)

- labels, price_label_* (VARCHAR)

- Migrations: add_missing_columns.sql both ADD COLUMN IF NOT EXISTS and MODIFY existing columns to NULL DEFAULT NULL. sentiment_confidence is VARCHAR(32).

---


## Known Limitations

- Only last 7 business days are emphasized in the dashboard by default.
- Prices around weekends/holidays may be deferred; scripts include fallback logic but verify edge cases.
- Only run headlines script during market hours.
- Finviz can throttle or change markup; scraper may require maintenance.





