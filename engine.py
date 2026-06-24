import yfinance as yf
from textblob import TextBlob
import feedparser 


CROP_STOCK_CORRELATION = {
    "Agriculture": {
        "keywords": ["wheat", "rice", "monsoon", "farming", "drought", "rain", "harvest", "grain", "onion", "potato"],
        "stocks": ["TATACONSUM.NS", "LTFOODS.NS"],
        "desc": "FMCG and Agri-processing"
    },
    "Sugar": {
        "keywords": ["sugar", "ethanol", "cane", "sugar mills", "molasses"],
        "stocks": ["BALRAMCHIN.NS", "RENUKA.NS", "EIDPARRY.NS"],
        "desc": "Sugar and Bio-fuels"
    },
    "Energy/Oil": {
        "keywords": ["crude oil", "petrol", "gas", "russia", "sanction", "brent", "fuel", "energy", "oil", "diesel"],
        "stocks": ["ONGC.NS", "RELIANCE.NS", "BPCL.NS"],
        "desc": "Oil & Gas production"
    },
    "Trade/Logistics": {
        "keywords": ["trade deal", "tariff", "export", "import", "shipping", "fta", "ports", "customs", "vessel", "cargo"],
        "stocks": ["ADANIPORTS.NS", "CONCOR.NS"],
        "desc": "Logistics and Ports"
    },
    "Fertilizer": {
        "keywords": ["fertilizer", "urea", "potash", "subsidy", "phosphates", "dap"],
        "stocks": ["COROMANDEL.NS", "CHAMBLFERT.NS"],
        "desc": "Agri-input Chemicals"
    }
}


def fetch_live_trade_news():
    
    rss_urls = [
        'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839061', # CNBC Commodities
        'http://feeds.feedburner.com/reuters/businessNews', # Reuters Business
        'https://economictimes.indiatimes.com/markets/commodities/rssfeeds/1808151.cms' # ET Commodities
    ]
    
    headlines = []
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = entry.title.strip()
                if len(title) > 20:
                    headlines.append(title)
            if len(headlines) >= 3: break 
        except:
            continue
            
    return headlines[:5] if headlines else ["Market data stable. Please enter news manually."]


def get_trade_advice(sentiment, score, sector):
    if score > 15: 
        return {
            "action": "🟢 BUY / ACCUMULATE",
            "intensity": "HIGH",
            "msg": f"Positive triggers for {sector}. Market sentiment is leaning bullish."
        }
    elif score < -15:
        return {
            "action": "🔴 SELL / CAUTION",
            "intensity": "CRITICAL",
            "msg": f"Risk detected in {sector}. Sentiment is bearish, caution advised."
        }
    else:
        return {
            "action": "🟡 HOLD / WATCH",
            "intensity": "LOW",
            "msg": f"Neutral impact for {sector}. Wait for a clear breakout or news trigger."
        }


def analyze_impact(headline):
    blob = TextBlob(headline)
    sentiment = blob.sentiment.polarity
    
    detected_sector = "General Market"
    target_stocks = ["^NSEI"] 
    
    headline_lower = headline.lower()
    for sector, info in CROP_STOCK_CORRELATION.items():
        if any(word in headline_lower for word in info["keywords"]):
            detected_sector = sector
            target_stocks = info["stocks"]
            break
            
    impact_score = round(sentiment * 100, 2) 
    advice = get_trade_advice(sentiment, impact_score, detected_sector)
    
    return {
        "sentiment": sentiment,
        "sector": detected_sector,
        "stocks": target_stocks,
        "score": impact_score,
        "advice": advice
    }
