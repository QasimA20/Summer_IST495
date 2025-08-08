-- Set up database and table
-- Use your database

-- =========================================================
-- A) ONE-TIME SCHEMA SETUP (run this on fresh machines)
-- =========================================================

USE stock_news;

-- create the table
CREATE TABLE IF NOT EXISTS headlines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticker VARCHAR(10) NOT NULL,
  headline VARCHAR(512) NOT NULL,
  date DATETIME NOT NULL,
  price_at_time DECIMAL(10, 2),
  price_1h_later DECIMAL(10, 2),
  UNIQUE (ticker, headline) 
);


-- =========================================================
-- MAIN PROJECT QUERY (Used by Dashboard
-- =========================================================


SELECT
  id,
  ticker,
  sector,
  industry,
  headline,
  price_at_time,
  price_1h_later,
  price_change_pct_1h,
  price_4h_later,
  price_change_pct_4h,
  price_24h_later,
  price_change_pct_24h,
  price_4d_later,
  price_change_pct_4d,
  price_7d_later,
  price_change_pct_7d,
  sentiment_score,
  matched_keywords,
  sentiment_label,
  sentiment_confidence,
  confidence_score,
  DATE_FORMAT(date, '%Y-%m-%d %H:%i:%s') AS clean_date
FROM headlines
WHERE date >= CURDATE() - INTERVAL 10 DAY
  AND WEEKDAY(date) < 5;



























