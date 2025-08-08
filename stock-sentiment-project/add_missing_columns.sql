
-- =========================================================
-- B) RUN ONLY IF YOUR TABLE IS MISSING THE COLUMNS
--    (Uncomment this block and run once)
-- =========================================================

/*
USE stock_news;

ALTER TABLE headlines
  -- metadata
  ADD COLUMN sector               VARCHAR(64)  NOT NULL DEFAULT '',
  ADD COLUMN industry             VARCHAR(128) NOT NULL DEFAULT '',

  -- absolute prices
  ADD COLUMN price_4h_later       DECIMAL(10,2) NOT NULL DEFAULT 0,
  ADD COLUMN price_24h_later      DECIMAL(10,2) NOT NULL DEFAULT 0,
  ADD COLUMN price_4d_later       DECIMAL(10,2) NOT NULL DEFAULT 0,
  ADD COLUMN price_7d_later       DECIMAL(10,2) NOT NULL DEFAULT 0,

  -- percentage changes
  ADD COLUMN price_change_pct_1h  DECIMAL(7,2)  NOT NULL DEFAULT 0,
  ADD COLUMN price_change_pct_4h  DECIMAL(7,2)  NOT NULL DEFAULT 0,
  ADD COLUMN price_change_pct_24h DECIMAL(7,2)  NOT NULL DEFAULT 0,
  ADD COLUMN price_change_pct_4d  DECIMAL(7,2)  NOT NULL DEFAULT 0,
  ADD COLUMN price_change_pct_7d  DECIMAL(7,2)  NOT NULL DEFAULT 0,

  -- sentiment fields
  ADD COLUMN sentiment_score      DECIMAL(4,3)  NOT NULL DEFAULT 0,
  ADD COLUMN matched_keywords     TEXT NULL,
  ADD COLUMN sentiment_label      VARCHAR(12)   NOT NULL DEFAULT '',
  ADD COLUMN sentiment_confidence DECIMAL(4,3)  NOT NULL DEFAULT 0,
  ADD COLUMN confidence_score     DECIMAL(4,3)  NOT NULL DEFAULT 0,

  -- labels for dashboard
  ADD COLUMN price_label_1h       VARCHAR(8)    NOT NULL DEFAULT '',
  ADD COLUMN price_label_4h       VARCHAR(8)    NOT NULL DEFAULT '',
  ADD COLUMN price_label_24h      VARCHAR(8)    NOT NULL DEFAULT '',
  ADD COLUMN price_label_4d       VARCHAR(8)    NOT NULL DEFAULT '',
  ADD COLUMN price_label_7d       VARCHAR(8)    NOT NULL DEFAULT '';
*/




-- NOTE: If your MySQL complains about "IF NOT EXISTS" on columns/indexes,
-- you're on an older 8.0 build. Just remove the "IF NOT EXISTS" and run once.