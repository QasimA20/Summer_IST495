import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the labeled headlines CSV
df = pd.read_csv('data/vader_test_headlines.csv')

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Empty lists to store VADER results
vader_scores = []
vader_sentiments = []

for headline in df['headline']:
    # Get the compound sentiment score from VADER
    score = analyzer.polarity_scores(headline)['compound']
    vader_scores.append(score)

    # Convert compound score into a sentiment label
    if score >= 0.05:
        vader_sentiments.append('positive')
    elif score <= -0.05:
        vader_sentiments.append('negative')
    else:
        vader_sentiments.append('neutral')

# Add the results to DataFrame
df['vader_score'] = vader_scores
df['vader_sentiment'] = vader_sentiments

# Check if VADER's sentiment matched my manual label
df['match'] = df['vader_sentiment'] == df['manual_sentiment']

# Print results into a readable table
print(df[['headline', 'manual_sentiment', 'vader_sentiment', 'vader_score', 'match']])

# This saves the results to a new CSV file for more efficient reporting
df.to_csv('data/vader_comparison_results.csv', index=False)
print("\nSaved results to: data/vader_comparison_results.csv")

