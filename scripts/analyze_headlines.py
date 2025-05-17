#Create a script that can process multiple headlines (not just one), score each, and store the results
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load CSV
df = pd.read_csv('data/custom_sample_headlines.csv')

# Initialize the analyzer
analyzer = SentimentIntensityAnalyzer()

# Analyze each headline
for headline in df['headline']:
    score = analyzer.polarity_scores(headline)
    print(f"Headline: {headline}")
    print(f"Scores: {score}")
    print("-" * 40)


