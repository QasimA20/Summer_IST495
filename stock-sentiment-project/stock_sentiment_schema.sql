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


-- Use this to clear the table but keep the structure
-- TRUNCATE TABLE headlines;

--  deletes everything
-- DROP TABLE IF EXISTS headlines;


SELECT COUNT(*) FROM headlines
WHERE price_at_time IS NOT NULL AND price_1h_later IS NOT NULL;



