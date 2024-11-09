import requests
import streamlit as st
from datetime import datetime

# Streamlit app title
st.title("Latest News Dashboard")

# NewsAPI credentials and endpoint
api_key = '388f9bdf475f4ecdab6aed960195fea9'
url = 'https://newsapi.org/v2/top-headlines'

# Parameters for the API request
params = {
    'apiKey': api_key,
    'country': 'us',  # Use 'us' for the United States; change if you need news from other countries
    'category': 'general',  # Default category
    'pageSize': 20  # Number of articles to fetch
}

# Function to fetch news from NewsAPI
def fetch_news(category):
    params['category'] = category
    response = requests.get(url, params=params)
    data = response.json()
    
    # Extract necessary fields from each article
    articles = [
        {
            'title': article['title'],
            'date': article['publishedAt'],
            'summary': article['description']
        }
        for article in data.get('articles', [])
    ]
    return articles

# Display filter options
category_filter = st.selectbox("Select Category", options=["All", "Business", "Entertainment", "General", "Health", "Science", "Sports", "Technology"])
date_filter = st.date_input("Select Date", datetime.today())

# Fetch articles based on the selected category
articles = fetch_news(category_filter.lower() if category_filter != "All" else 'general')

# Filter articles by selected date
filtered_articles = [
    article for article in articles
    if datetime.strptime(article["date"], "%Y-%m-%dT%H:%M:%SZ").date() == date_filter
]

# Display filtered articles
if filtered_articles:
    for article in filtered_articles:
        st.subheader(article["title"])
        st.write(f"Published on: {article['date']}")
        st.write(article["summary"])
else:
    st.write("No articles found for the selected filters.")
