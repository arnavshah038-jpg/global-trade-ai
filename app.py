import streamlit as st
import yfinance as yf
import pandas as pd
from engine import analyze_impact, fetch_live_trade_news


st.set_page_config(page_title="AI Trade Intel Engine", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #31333f; }
    div[data-testid="stExpander"] { border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title(" Global Trade & Geopolitical AI Analyzer")
st.markdown("-")


st.sidebar.header(" Live Market Intelligence")
st.sidebar.info("Scrape real-time global trade news from Reuters.")

if st.sidebar.button("Fetch Latest News"):
    with st.sidebar:
        with st.spinner('Scraping news...'):
            news_list = fetch_live_trade_news()
            st.write(" Latest Headlines")
            for n in news_list:
                st.write(f"🔹 {n}")
                st.markdown("-")


st.subheader("🔍 News Impact Analysis")
headline = st.text_input("Enter News Headline or Agriculture Update:", 
                         placeholder="e.g., Massive wheat shortage in Punjab due to unseasonal rain...")

if st.button("Run Deep AI Analysis"):
    if headline:
        
        result = analyze_impact(headline)
        advice = result['advice']
        
       
        alert_color = "red" if advice['intensity'] == "CRITICAL" else "green" if advice['intensity'] == "HIGH" else "#FFA500"
        
        st.markdown(f"""
            <div style="background-color:rgba(255,255,255,0.05); border-left: 10px solid {alert_color}; padding:25px; border-radius:10px; margin-bottom: 25px;">
                <h1 style="color:{alert_color}; margin:0; font-size: 28px;">{advice['action']}</h1>
                <p style="font-size:18px; color:#e0e0e0; margin-top: 10px;">{advice['msg']}</p>
            </div>
        """, unsafe_allow_html=True)

        
        m1, m2, m3 = st.columns(3)
        m1.metric("Detected Sector", result['sector'])
        
        sentiment_val = result['sentiment']
        status = "Bullish" if sentiment_val > 0.05 else "Bearish" if sentiment_val < -0.05 else "Neutral"
        m2.metric("Market Sentiment", status, f"{result['score']}%")
        
        # Picking the main stock for the ticker display
        primary_ticker = result['stocks'][0]
        m3.metric("Primary Ticker", primary_ticker)

        st.markdown("-")
        
        # 4. Details & Chart Row
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Analysis Report")
            st.write(f"**Source Context:** {headline}")
            
            st.write(" Sector Stocks to Watch:")
            for stock in result['stocks']:
                
                st.markdown(f"- [{stock}](https://finance.yahoo.com/quote/{stock})")
            
            with st.expander("See Methodology"):
                st.write("Using TextBlob NLP for Sentiment and Custom Keyword Mapping for Sector Correlation.")
        
        with col2:
            st.subheader(f"Market Trend: {primary_ticker}")
            try:
                
                ticker_obj = yf.Ticker(primary_ticker)
                hist = ticker_obj.history(period="1mo")
                
                if not hist.empty:
                    st.line_chart(hist['Close'], use_container_width=True)
                    st.caption(f"Real-time 30-day closing price for {primary_ticker}")
                else:
                    st.warning(f"Live data for {primary_ticker} is currently unavailable.")
            except Exception as e:
                st.error(f"Stock API Error: {e}")
    else:
        st.warning("Please enter a headline first!")

# Footer logic
st.markdown("-")
st.caption("AI Model: TextBlob NLP Engine | Data Source: Yahoo Finance & Reuters Commodities News")
