#all of the neccessary libraries needed
import streamlit as st
import mysql.connector
from datetime import datetime
import pandas as pd
import altair as alt
from collections import Counter
from pandas.tseries.offsets import BDay


#Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Qasim2004",
    database="stock_news"
)
cursor = conn.cursor()


# Fetching all headlines in the past 7 days across all tickers
cursor.execute("""
    SELECT date, ticker, matched_keywords
    FROM headlines
    WHERE date >= CURDATE() - INTERVAL 14 DAY
""")
rows_all = cursor.fetchall()

df_headlines_all = pd.DataFrame(rows_all, columns=["date", "ticker", "matched_keywords"])
df_headlines_all["date"] = pd.to_datetime(df_headlines_all["date"])

# Filter to only keep headlines from the past 7 business days
today = datetime.today()
seven_bdays_ago = today - BDay(7)
df_headlines_all = df_headlines_all[df_headlines_all["date"] >= seven_bdays_ago]


# Page Configuration
st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")

# Sidebar sections
st.sidebar.header("IST 495  -  Qasim Ansari")
st.sidebar.markdown("-------")

st.sidebar.markdown("### About")
st.sidebar.info(
    "This dashboard allows real-time analysis of stock-related news sentiment and price trends using custom logic and live financial data feeds."
)


# title
st.markdown("""
    <h1 style='display: flex; align-items: center;'>
        <span style='font-size: 1.5em;'>📈📉</span>&nbsp;Real-Time Stock News Sentiment & Prediction Dashboard
    </h1>
""", unsafe_allow_html=True)

# Ticker input section
ticker_input = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA)", value="tsla").upper().strip()

# Initialize placeholders
headline_count = 0
recent_headlines = []


# Keeping track of whether user analyzed a ticker or not
if "analyze_clicked" not in st.session_state:
    st.session_state.analyze_clicked = False


# Run only if Analyze button is clicked
if st.button("Analyze"):
    st.session_state.analyze_clicked = True

    # This will fetch headline count for ticker
    count_query = "SELECT COUNT(*) FROM headlines WHERE ticker = %s"
    cursor.execute(count_query, (ticker_input,))
    headline_count = cursor.fetchone()[0]

    # Fetch 7 most recent headlines for ticker
    query = """
        SELECT headline, sentiment_score, date
        FROM headlines
        WHERE ticker = %s AND sentiment_score IS NOT NULL
        ORDER BY date DESC
        LIMIT 7
    """
    cursor.execute(query, (ticker_input,))
    recent_headlines = cursor.fetchall()

    # Get the most recent stored stock price
    cursor.execute("""
        SELECT price_at_time FROM headlines
        WHERE ticker = %s AND price_at_time IS NOT NULL
        ORDER BY date DESC
        LIMIT 1
    """, (ticker_input,))
    result = cursor.fetchone()

    # If we found a valid price, display it in green on the dashboard
    if result:
        recent_price = result[0]
        st.markdown(f"### <span style='color:green'>{ticker_input} Stock Price: ${recent_price:.2f}</span>", unsafe_allow_html=True)
    else:
        st.warning("No recent price data available for this ticker in the past 7 days.")

    # Fetch all price changes (past 7 days)
    cursor.execute("""
        SELECT price_change_pct_1h, price_change_pct_4h, price_change_pct_24h,
               price_change_pct_4d, price_change_pct_7d
        FROM headlines
        WHERE ticker = %s AND date >= CURDATE() - INTERVAL 7 DAY
    """, (ticker_input,))
    rows = cursor.fetchall()

    # Prepare a list of all available price changes
    # Flatten values with labels for comparison
    changes = []
    for row in rows:
        timeframes = ['1h', '4h', '24h', '4d', '7d']
        for i, val in enumerate(row):
            if val is not None:
                changes.append((val, timeframes[i]))

    #  Display the biggest price movement
    if changes:
        biggest_change = max(changes, key=lambda x: abs(x[0]))
        pct, timeframe = biggest_change

        # Decide the color/emoji based on whether the change is positive or negative
        color = 'green' if pct > 0 else 'red'
        emoji = '📈' if pct > 0 else '📉'
        #display results
        st.markdown(
            f"**Biggest Movement:** {emoji} "
            f"<span style='color:{color}'>"
            f"{pct:+.2f}% (Over {timeframe})</span>",
            unsafe_allow_html=True
        )

    # Number of headlines analyzed
    st.sidebar.markdown("### 📰 Headlines Analyzed")
    st.sidebar.write(f"✅ {headline_count} headlines found for `{ticker_input}` in the past 7 days.")

    # Looping through each headline and display its sentiment label

    if recent_headlines:
        st.subheader("📰 Latest News & Sentiment Analysis")
        for row in recent_headlines:
            headline, score, date = row
            date_str = date.strftime("%b %d, %Y")

            if score > 0.1:
                label = "🟢 Positive"
            elif score < -0.1:
                label = "🔴 Negative"
            else:
                label = "⚪ Neutral"

            st.markdown(f"**• {headline}**  \n→ *{label}*  ({date_str})")


# --- Predict Next-Day Price Based on 24h Change ---
# This block tries to forecast the next day's stock price using the average 24-hour price change over the past week.

# Get all 24h price change percentages for this ticker in past 7 days
    cursor.execute("""
        SELECT price_at_time, price_change_pct_24h
        FROM headlines
        WHERE ticker = %s AND date >= CURDATE() - INTERVAL 7 DAY
            AND price_change_pct_24h IS NOT NULL
    """, (ticker_input,))
    price_data = cursor.fetchall()

# Calculate the average percentage change
# Clean the data by filtering out any rows where the 24h change is missing

    valid_changes = [pct for _, pct in price_data if pct is not None]

    # Only proceed if we have valid price changes to work with
    if valid_changes:
        avg_pct_change = sum(valid_changes) / len(valid_changes)

    # Use the most recent price_at_time as base price
        latest_price_row = max(price_data, key=lambda x: x[0])  # latest price_at_time
        base_price = latest_price_row[0]

    # Predict next-day price using average 24h % change
        #predicted_price = base_price * (1 + avg_pct_change / 100)
        predicted_price = float(base_price) * (1 + float(avg_pct_change) / 100)


    # Color/symbol the prediction based on price direction 
        if predicted_price > base_price:
            color = "green"
            arrow = "📈"
        elif predicted_price < base_price:
            color = "red"
            arrow = "📉"
        else:
            color = "gray"
            arrow = "➖"

    # Display prediction result
        st.subheader("📊 Predicted Next-Day Price")
        st.markdown(
            f"Based on recent trends, the estimated next-day price is: "
            f"<span style='color:{color}'>{arrow} ${predicted_price:.2f}</span>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Not enough data to estimate next-day price.")


# This section visualizes how sentiment and price moved together over the past 7 days.

# Query both daily average sentiment and average closing price by date
    cursor.execute("""
        SELECT DATE(date) as day, 
            AVG(sentiment_score) as avg_sentiment,
            AVG(price_at_time) as avg_price
        FROM headlines 
        WHERE ticker = %s AND sentiment_score IS NOT NULL 
            AND price_at_time IS NOT NULL 
            AND date >= CURDATE() - INTERVAL 7 DAY
        GROUP BY day
        ORDER BY day
    """, (ticker_input,))
    combo_data = cursor.fetchall()

# Create DataFrame
    #Storing the results in a Pandas DataFrame
    df_combo = pd.DataFrame(combo_data, columns=["Date", "Average Sentiment", "Average Price"])
    df_combo["Date"] = pd.to_datetime(df_combo["Date"])

    #Making sure the sentiment and price columns are numerical (just in case of bad values)
    df_combo["Average Sentiment"] = pd.to_numeric(df_combo["Average Sentiment"], errors='coerce')
    df_combo["Average Price"] = pd.to_numeric(df_combo["Average Price"], errors='coerce')


# Creating a line chart with individual lines for average sentiment using Altair

    sentiment_line = alt.Chart(df_combo).mark_line(point=True, color='steelblue').encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Average Sentiment:Q', axis=alt.Axis(title='Avg Sentiment')),
        tooltip=[
            alt.Tooltip('Date:T'),
            alt.Tooltip('Average Sentiment:Q', format='.2f', title='Avg Sentiment')
        ]
    )

    # Separate line chart for average price
    price_line = alt.Chart(df_combo).mark_line(point=True, color='orange').encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Average Price:Q', axis=alt.Axis(title='Avg Price ($)'), scale=alt.Scale(zero=False)),
        tooltip=[
            alt.Tooltip('Date:T'),
            alt.Tooltip('Average Price:Q', format='.2f', title='Avg Price')
        ]
    )

    # Overlay both charts and combine with independent y-axis scales

    combined_chart = alt.layer(sentiment_line, price_line).resolve_scale(y='independent')

# Display
    st.subheader("📈 Sentiment vs. Price Movement")
    st.markdown("This comparison shows whether market sentiment is reflected in price changes.")
    st.altair_chart(combined_chart, use_container_width=True)





# Sentiment Accuracy Summary 
# This section evaluates whether the average sentiment on each day aligns with actual stock performance afterwards

    st.markdown("### 🧠 Daily Sentiment Accuracy Summary")
    st.caption("A 4-day price change is required for inclusion. Only eligible dates from the past 7 business days are shown.")

# Query sentiment and multiple price change intervals per day
    cursor.execute("""
        SELECT DATE(date) as day, 
            AVG(sentiment_score) as avg_sentiment,
            AVG(price_change_pct_1h) as price_change_pct_1h,
            AVG(price_change_pct_4h) as price_change_pct_4h,
            AVG(price_change_pct_24h) as price_change_pct_24h,
            AVG(price_change_pct_4d) as price_change_pct_4d,
            AVG(price_change_pct_7d) as price_change_pct_7d
        FROM headlines 
        WHERE ticker = %s 
            AND sentiment_score IS NOT NULL 
            AND price_change_pct_4d IS NOT NULL 
            AND date >= CURDATE() - INTERVAL 7 DAY
        GROUP BY day
        ORDER BY day
    """, (ticker_input,))
    score_data = cursor.fetchall()

# Convert to DataFrame and store the results
    df_score = pd.DataFrame(score_data, columns=[
        "date", "avg_sentiment", "price_change_pct_1h", "price_change_pct_4h",
        "price_change_pct_24h", "price_change_pct_4d", "price_change_pct_7d"
    ])

#  Only proceed if we got results back from the query
    if not df_score.empty:
        for _, row in df_score.iterrows():
            date_str = pd.to_datetime(row['date']).strftime('%b %d')
            sentiment = round(row['avg_sentiment'], 2)
            direction = "positive" if sentiment >= 0 else "negative"

        # Price fields in order of priority
            price_fields = [
                'price_change_pct_7d',
                'price_change_pct_4d',
                'price_change_pct_24h',
                'price_change_pct_4h',
                'price_change_pct_1h'
            ]

            matched_pct = None
            matched_field = None

            for field in price_fields:
                if field in row and row[field] is not None:
                    pct = row[field]

                    # Match if sentiment direction and price change direction agree
                    if (direction == "positive" and pct > 0) or (direction == "negative" and pct < 0):
                        matched_pct = round(pct, 2)
                        matched_field = field
                        break

            # Fallback to 4-day if no match
            if matched_pct is None:
                matched_pct = round(row.get('price_change_pct_4d', 0), 2)
                matched_field = 'price_change_pct_4d'

        # determine icons and verdict
            triangle = "📈" if matched_pct > 0 else "📉" if matched_pct < 0 else "➖"
            verdict = "✅ Right" if (sentiment >= 0 and matched_pct >= 0) or (sentiment < 0 and matched_pct < 0) else "❌ Wrong"

        # Show header
            st.markdown(f"### {date_str} – {ticker_input.upper()}")

        # Show colored verdict card
            summary_text = f"**Avg Sentiment:** {sentiment} | **{matched_field.replace('_', ' ').title()} %:** {triangle} {matched_pct}% | {verdict}"

            if "✅" in verdict:
                st.success(summary_text)
            else:
                st.error(summary_text)
    else:
        st.info("No sentiment accuracy data available for the past 7 days.")




# Sidebar: Headlines Date Range + Top Keywords

with st.sidebar:
    # Date Range (Always Show)
    # Show the earliest and latest dates from the full headlines dataset

    if not df_headlines_all.empty:
        start_date = df_headlines_all['date'].min().strftime('%b %d')
        end_date = df_headlines_all['date'].max().strftime('%b %d')
        st.markdown("### 🗓️ Dashboard Date Range")
        st.caption(f"Showing headlines from {start_date} to {end_date}")

    from collections import Counter

    # Top Keywords, show only if ticker not analyzed
    if not ticker_input or not st.session_state.get("analyze_clicked"):
        st.markdown("### 🧠 Top Keywords (All Tickers)")

        # Clean and gather all matched keywords from all headlines
        keyword_series_all = df_headlines_all['matched_keywords'].dropna().astype(str)
        all_keywords_all = []
        for keywords in keyword_series_all:
            all_keywords_all.extend([kw.strip() for kw in keywords.split(',') if kw.strip()])

        # Count top 5 keywords across all tickers
        top_keywords_all = Counter(all_keywords_all).most_common(5)
        if top_keywords_all:
            for word, count in top_keywords_all:
                st.markdown(f"- **{word}** ({count})")
        else:
            st.caption("No keywords found across all tickers.")

    # Top Keywords for that specific ticker -- show only if a ticker is analyzed
    elif ticker_input and st.session_state.get("analyze_clicked"):
        st.markdown(f"### 🧠 Top Keywords ({ticker_input})")

        # Query matched keywords for selected ticker in the past 7 days
        cursor.execute("""
            SELECT matched_keywords FROM headlines
            WHERE ticker = %s AND date >= CURDATE() - INTERVAL 7 DAY
                AND matched_keywords IS NOT NULL
        """, (ticker_input,))
        rows = cursor.fetchall()


        # Clean and extract keyword list
        keyword_list = []
        for row in rows:
            keywords = row[0].split(',')
            keyword_list.extend([k.strip() for k in keywords if k.strip()])

        # Count for the top 5 keywords for selected ticker
        top_keywords_ticker = Counter(keyword_list).most_common(5)
        if top_keywords_ticker:
            for word, count in top_keywords_ticker:
                st.markdown(f"- **{word}** ({count})")
        else:
            st.caption("No matched keywords for this ticker.")


# Default View: Show recent news if no ticker analyzed yet
if not st.session_state.analyze_clicked:
    st.subheader("📰 Latest Market Headlines (Across All Stocks)")


    # Fetch 10 most recent headlines with valid sentiment and price data
    cursor.execute("""
        SELECT ticker, headline, sentiment_score, price_at_time, date
        FROM headlines
        WHERE sentiment_score IS NOT NULL AND price_at_time IS NOT NULL
        ORDER BY date DESC
        LIMIT 10
    """)
    recent_news = cursor.fetchall()


    # Displaying each headline in a clean, styled block
    if recent_news:
        for ticker, headline, score, price, date in recent_news:
            label = "🟢 Positive" if score > 0.1 else "🔴 Negative" if score < -0.1 else "⚪ Neutral"
            date_str = pd.to_datetime(date).strftime("%b %d, %Y")

            st.markdown(f"""
            <div style='padding: 10px 15px; border-left: 4px solid #ccc; margin-bottom: 15px; background-color: #f9f9f9; border-radius: 8px;'>
                <b>{ticker}</b> — <span style='color:gray'>{date_str}</span><br>
                <span>{headline}</span><br>
                <i>{label} | Price: ${price:.2f}</i>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No recent headlines available.")






