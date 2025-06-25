-- Set up database and table
-- Use your database
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

--  To see the data
SELECT * FROM headlines ORDER BY id DESC LIMIT 20;


-- Fix timestamp
SELECT id, ticker, headline, FROM_UNIXTIME(UNIX_TIMESTAMP(date)) AS formatted_date
FROM headlines
ORDER BY id DESC
LIMIT 5;



SELECT
  id,
  ticker,
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
  sentiment_theme,
  sentiment_label,
  sentiment_confidence,
  DATE_FORMAT(date, '%Y-%m-%d %H:%i:%s') AS clean_date
FROM headlines;
/*
WHERE date >= CURDATE() - INTERVAL 10 DAY
  AND WEEKDAY(date) < 5;
*/


SELECT * FROM headlines
WHERE date >= CURDATE() - INTERVAL 10 DAY
  AND WEEKDAY(date) < 5;

DESCRIBE headlines;
-- Selects all weekday headlines from approx. 7 business days ago

-- Use this to clear the table but keep the structure
-- TRUNCATE TABLE headlines;
--  deletes everything
-- DROP TABLE IF EXISTS headlines;


SELECT COUNT(*) FROM headlines
WHERE price_at_time IS NOT NULL AND price_1h_later IS NOT NULL;



ALTER TABLE headlines 
MODIFY price_change_pct_4d DECIMAL(6,4);



SHOW COLUMNS FROM headlines;



ALTER TABLE headlines
MODIFY COLUMN sentiment_score DECIMAL(4,3);

ALTER TABLE headlines
MODIFY COLUMN price_7d_later DECIMAL(6,2);



ALTER TABLE headlines
MODIFY COLUMN price_change_pct_7d DECIMAL(7,2);

SELECT id, ticker, headline, date
FROM headlines
WHERE headline LIKE '%reverse split%' OR headline LIKE '%stock split%';


























