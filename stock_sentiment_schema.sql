CREATE DATABASE IF NOT EXISTS stock_news;
USE stock_news;

CREATE TABLE IF NOT EXISTS headlines (
  id INT AUTO_INCREMENT PRIMARY KEY,
  ticker VARCHAR(10) NOT NULL,
  headline TEXT NOT NULL,
  date DATETIME NOT NULL,
  price_at_time DECIMAL(10, 2),
  price_1h_later DECIMAL(10, 2)
);


SHOW TABLES;


