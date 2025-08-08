# Summer_IST495
Real-time dictionary-based sentiment analysis for stock news headlines (IST 495 Internship)

**Intern: Qasim Ansari**

## Project Overview

This internship project focuses on real-time sentiment analysis of stock market news headlines using a custom-built dictionary-based scoring system.

Unlike black-box machine learning sentiment models, this approach is transparent, explainable, and easily adaptable. The system ingests live headlines, assigns sentiment scores using a curated keyword dictionary, and correlates sentiment with actual stock price movements.

The end product is an interactive Streamlit dashboard that allows users to:

Explore recent headlines and their sentiment scores

Track sentiment trends for specific tickers over time

Compare sentiment with actual price changes at multiple intervals

Identify top positive/negative keywords driving market tone

This work combines data engineering, sentiment analysis, and dashboard design into a complete, automated pipeline.

---

## Project Objectives

1. **Build a Real-Time Sentiment Scoring Engine**
   Python scripts ingest live stock headlines from Finviz

   Headlines are cleaned, tokenized, and scored using a custom sentiment dictionary

   Scores are scaled between -1 (strongly negative) and +1 (strongly positive)

3. **Develop and Maintain a Custom Dictionary**  
   Work iteratively to expand, tune, and refine a word-score dictionary based on real-world feedback and test results. Adjust for domain-specific terms.

4. **Design a Visual Dashboard (Jupyter/Streamlit)**  
   Build an interactive dashboard that allows sorting/filtering by score, date, or topic. Users should be able to explore sentiment patterns and outliers in headline tone over time.

---

## Learning Goals

- Deepen understanding of Python through hands-on coding
- Learn how to build and evolve a sentiment dictionary
- Gain experience using data visualization and dashboard tools 
- Improve GitHub workflow and version control discipline
- Practice managing a multi-phase data project with weekly deliverables

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| **Python** | Data processing, scoring logic |
| **Jupyter Notebook** | Exploration, testing, reporting |
| **VS Code** | Development and file structure |
| **GitHub** | Version control and weekly progress sharing |
| **Pandas** | Text parsing, web scraping, data handling |

---
