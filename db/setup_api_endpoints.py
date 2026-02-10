"""
Create API Endpoints table in database
Stores all Datasaham API endpoints with documentation
"""

import mysql.connector
from mysql.connector import errorcode
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_CONFIG


def create_api_endpoints_table():
    """Create table to store API endpoints"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        create_table = """
        CREATE TABLE IF NOT EXISTS api_endpoints (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(50) NOT NULL,
            endpoint_name VARCHAR(100) NOT NULL,
            method VARCHAR(10) NOT NULL,
            url_path VARCHAR(255) NOT NULL,
            description TEXT,
            required_params VARCHAR(255),
            optional_params VARCHAR(255),
            response_format VARCHAR(50),
            rate_limit_tier VARCHAR(20),
            use_case VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_category (category),
            INDEX idx_endpoint_name (endpoint_name),
            UNIQUE KEY unique_endpoint (category, method, url_path)
        );
        """
        
        cursor.execute(create_table)
        print("✅ API Endpoints table created")
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error creating table: {err}")
        return False


def insert_datasaham_endpoints():
    """Insert all Datasaham API endpoints into database"""
    
    endpoints = [
        # Calendar
        ("Calendar", "Get Dividends", "GET", "/api/calendar/dividend", "Get dividend calendar events", None, None, "JSON", "Free", "Track dividend payments"),
        ("Calendar", "Get Bonus", "GET", "/api/calendar/bonus", "Get bonus share calendar events", None, None, "JSON", "Free", "Track bonus share distributions"),
        ("Calendar", "Get Stock Splits", "GET", "/api/calendar/stock-split", "Get stock split calendar events", None, None, "JSON", "Free", "Track stock splits"),
        ("Calendar", "Get Right Issues", "GET", "/api/calendar/right-issue", "Get right issue calendar events", None, None, "JSON", "Free", "Track rights offerings"),
        ("Calendar", "Get Warrants", "GET", "/api/calendar/warrant", "Get warrant calendar events", None, None, "JSON", "Free", "Track warrant launches"),
        ("Calendar", "Get RUPS", "GET", "/api/calendar/rups", "Get RUPS calendar events", None, None, "JSON", "Free", "Track shareholder meetings"),
        ("Calendar", "Get IPO", "GET", "/api/calendar/ipo", "Get IPO calendar events", None, None, "JSON", "Free", "Track new IPOs"),
        ("Calendar", "Get Economic", "GET", "/api/calendar/economic", "Get economic calendar events", None, None, "JSON", "Free", "Track economic announcements"),
        ("Calendar", "Get Tender Offers", "GET", "/api/calendar/tender-offer", "Get tender offer calendar events", None, None, "JSON", "Free", "Track tender offers"),
        ("Calendar", "Get Today's Events", "GET", "/api/calendar/today", "Get today's calendar events", None, None, "JSON", "Free", "Track today's corporate actions"),
        
        # Main
        ("Main", "Search", "GET", "/api/main/search", "Search for stocks by name or code", "query", None, "JSON", "Free", "Find specific stocks"),
        ("Main", "Trending", "GET", "/api/main/trending", "Get trending stocks", None, "limit,offset", "JSON", "Free", "Identify market trends"),
        ("Main", "Morning Briefing", "GET", "/api/main/morning-briefing", "Get morning market briefing", None, None, "JSON", "Free", "Daily market overview"),
        ("Main", "Commodities Impact", "GET", "/api/main/commodities-impact", "Get commodities impact analysis", None, None, "JSON", "Free", "Analyze commodity effects on IDX"),
        ("Main", "Forex IDR Impact", "GET", "/api/main/forex-idr-impact", "Get forex impact on IDR", None, None, "JSON", "Free", "Analyze forex effects"),
        ("Main", "US Stocks Parent", "GET", "/api/main/us-stocks-parent", "Get US stock parent companies", None, None, "JSON", "Premium", "Track US parent companies"),
        ("Main", "Broker Codes", "GET", "/api/main/broker-codes", "Get all broker codes", None, None, "JSON", "Free", "Get broker reference list"),
        
        # Global Market
        ("Global Market", "Market Overview", "GET", "/api/global/market-overview", "Get global market overview", None, None, "JSON", "Free", "Global market status"),
        ("Global Market", "Indices Impact", "GET", "/api/global/indices-impact", "Get global indices impact on IDX", None, None, "JSON", "Free", "Analyze global index effects"),
        ("Global Market", "Impact Analysis", "GET", "/api/global/impact-analysis", "Get detailed impact analysis", None, None, "JSON", "Premium", "Comprehensive impact analysis"),
        
        # Chart
        ("Chart", "Get OHLCV Data", "GET", "/api/chart/{symbol}/{timeframe}", "Get OHLCV chart data", "symbol,timeframe", "limit,offset,period", "JSON", "Free", "Get price history and technical data"),
        
        # Sectors
        ("Sectors", "Get All Sectors", "GET", "/api/sectors/", "Get all sectors", None, None, "JSON", "Free", "List all market sectors"),
        ("Sectors", "Get Subsectors", "GET", "/api/sectors/{sectorId}/subsectors", "Get subsectors by sector", "sectorId", None, "JSON", "Free", "List subsectors"),
        ("Sectors", "Get Companies", "GET", "/api/sectors/{sectorId}/subsectors/{subSectorId}/companies", "Get companies by subsector", "sectorId,subSectorId", None, "JSON", "Free", "List companies in subsector"),
        ("Sectors", "Get Sector Correlation", "GET", "/api/sectors/correlation/{sector}", "Get sector correlation matrix", "sector", None, "JSON", "Premium", "Analyze sector correlations"),
        
        # Movers
        ("Movers", "Get Movers", "GET", "/api/movers/{moverType}", "Get market movers (gainer/loser/volume)", "moverType", "limit", "JSON", "Free", "Track market movers"),
        
        # Market Detector
        ("Market Detector", "Broker Activity", "GET", "/api/market-detector/broker-activity/{brokerCode}", "Get broker activity for specific broker", "brokerCode", None, "JSON", "Premium", "Track broker activities"),
        ("Market Detector", "Top Broker", "GET", "/api/market-detector/top-broker", "Get top brokers by activity", None, "limit", "JSON", "Premium", "Identify leading brokers"),
        ("Market Detector", "Top Stock", "GET", "/api/market-detector/top-stock", "Get top stocks by broker activity", None, "limit", "JSON", "Premium", "Find stocks with high broker interest"),
        ("Market Detector", "Broker Summary", "GET", "/api/market-detector/broker-summary/{symbol}", "Get broker summary for stock", "symbol", None, "JSON", "Premium", "Analyze broker flows on stock"),
        
        # Bandarmology
        ("Bandarmology", "Accumulation", "GET", "/api/analysis/bandar/accumulation/{symbol}", "Get bandar accumulation analysis", "symbol", None, "JSON", "Premium", "Detect institutional accumulation"),
        ("Bandarmology", "Distribution", "GET", "/api/analysis/bandar/distribution/{symbol}", "Get bandar distribution analysis", "symbol", None, "JSON", "Premium", "Detect institutional distribution"),
        ("Bandarmology", "Smart Money", "GET", "/api/analysis/bandar/smart-money/{symbol}", "Get smart money flow analysis", "symbol", None, "JSON", "Premium", "Track smart money flows"),
        ("Bandarmology", "Pump & Dump", "GET", "/api/analysis/bandar/pump-dump/{symbol}", "Get pump & dump detection", "symbol", None, "JSON", "Premium", "Identify manipulation patterns"),
        
        # Retail Opportunity
        ("Retail Opportunity", "Multibagger Scan", "GET", "/api/analysis/retail/multibagger/scan", "Scan for multibagger opportunities", None, "limit", "JSON", "Premium", "Find high-growth stocks"),
        ("Retail Opportunity", "Breakout Alerts", "GET", "/api/analysis/retail/breakout/alerts", "Get breakout alerts", None, "limit", "JSON", "Premium", "Track breakout patterns"),
        ("Retail Opportunity", "Risk-Reward", "GET", "/api/analysis/retail/risk-reward/{symbol}", "Get risk-reward analysis", "symbol", None, "JSON", "Premium", "Calculate risk-reward ratios"),
        ("Retail Opportunity", "Sector Rotation", "GET", "/api/analysis/retail/sector-rotation", "Get sector rotation analysis", None, None, "JSON", "Premium", "Identify rotating sectors"),
        
        # Market Sentiment
        ("Market Sentiment", "Sentiment", "GET", "/api/analysis/sentiment/{symbol}", "Get market sentiment for stock", "symbol", None, "JSON", "Premium", "Analyze retail vs bandar sentiment"),
        ("Market Sentiment", "IPO Momentum", "GET", "/api/analysis/sentiment/ipo/momentum", "Get IPO momentum analysis", None, None, "JSON", "Premium", "Track IPO performance"),
        
        # Advanced Analytics
        ("Advanced Analytics", "Correlation Matrix", "GET", "/api/analysis/correlation", "Get correlation matrix", None, None, "JSON", "Premium", "Analyze stock correlations"),
        ("Advanced Analytics", "Whale Transactions", "GET", "/api/analysis/whale-transactions/{symbol}", "Get whale transaction analysis", "symbol", None, "JSON", "Premium", "Detect whale accumulation"),
        ("Advanced Analytics", "Insider Screening", "GET", "/api/analysis/insider-screening", "Screen for insider trading", None, None, "JSON", "Premium", "Track insider activities"),
        ("Advanced Analytics", "Insider Net", "GET", "/api/analysis/insider-net/{symbols}", "Get net insider buying/selling", "symbols", None, "JSON", "Premium", "Analyze insider trends"),
        ("Advanced Analytics", "Technical Analysis", "GET", "/api/analysis/technical/{symbol}", "Get technical analysis", "symbol", None, "JSON", "Premium", "Get technical indicators"),
        ("Advanced Analytics", "Multi-Market Screener", "GET", "/api/analysis/screener/multi-market", "Screen multiple markets", None, None, "JSON", "Premium", "Comprehensive market screening"),
        
        # Emiten
        ("Emiten", "Info", "GET", "/api/emiten/{symbol}/info", "Get company info", "symbol", None, "JSON", "Free", "Get basic company information"),
        ("Emiten", "Orderbook", "GET", "/api/emiten/{symbol}/orderbook", "Get order book data", "symbol", None, "JSON", "Premium", "Real-time order book"),
        ("Emiten", "Running Trade", "GET", "/api/emiten/running-trade", "Get running trades", None, None, "JSON", "Premium", "Real-time trading data"),
        ("Emiten", "Tradebook Chart", "GET", "/api/emiten/tradebook-chart", "Get tradebook chart", None, None, "JSON", "Premium", "Historical trading data"),
        ("Emiten", "Historical Summary", "GET", "/api/emiten/{symbol}/historical-summary", "Get historical summary", "symbol", None, "JSON", "Premium", "Historical performance data"),
        ("Emiten", "Broker Trade Chart", "GET", "/api/emiten/{symbol}/broker-trade-chart", "Get broker trade chart", "symbol", None, "JSON", "Premium", "Broker trading patterns"),
        ("Emiten", "Seasonality", "GET", "/api/emiten/{symbol}/seasonality", "Get seasonality analysis", "symbol", None, "JSON", "Premium", "Seasonal patterns"),
        ("Emiten", "Profile", "GET", "/api/emiten/{symbol}/profile", "Get company profile", "symbol", None, "JSON", "Free", "Detailed company profile"),
        ("Emiten", "Subsidiary", "GET", "/api/emiten/{symbol}/subsidiary", "Get subsidiary info", "symbol", None, "JSON", "Premium", "Company subsidiary structure"),
        ("Emiten", "Key Stats", "GET", "/api/emiten/{symbol}/keystats", "Get key statistics", "symbol", None, "JSON", "Free", "Key company statistics"),
        ("Emiten", "Insider", "GET", "/api/emiten/insider", "Get all insider data", None, None, "JSON", "Premium", "Insider trading data"),
        ("Emiten", "Symbol Insider", "GET", "/api/emiten/{symbol}/insider", "Get insider data for symbol", "symbol", None, "JSON", "Premium", "Insider data by symbol"),
        ("Emiten", "Fundachart", "GET", "/api/emiten/fundachart", "Get fundachart data", None, None, "JSON", "Premium", "Fund ownership data"),
        ("Emiten", "Fundachart Metrics", "GET", "/api/emiten/fundachart/metrics", "Get fundachart metrics", None, None, "JSON", "Premium", "Fund metrics"),
        ("Emiten", "Financials", "GET", "/api/emiten/{symbol}/financials", "Get financial statements", "symbol", None, "JSON", "Premium", "Financial statements"),
        ("Emiten", "Holding Composition", "GET", "/api/emiten/{symbol}/profile/holding-composition", "Get shareholding", "symbol", None, "JSON", "Premium", "Shareholding structure"),
        ("Emiten", "Foreign Ownership", "GET", "/api/emiten/{symbol}/foreign-ownership", "Get foreign ownership", "symbol", None, "JSON", "Premium", "Foreign investor holding"),
        
        # BETA
        ("BETA", "Insights", "GET", "/api/beta/insights/{symbol}", "Get insights", "symbol", None, "JSON", "Beta", "Beta insights feature"),
        ("BETA", "Earnings", "GET", "/api/beta/earnings/{symbol}", "Get earnings data", "symbol", None, "JSON", "Beta", "Beta earnings feature"),
        ("BETA", "Equities", "GET", "/api/beta/equities/{symbol}", "Get equities data", "symbol", None, "JSON", "Beta", "Beta equities feature"),
        ("BETA", "Key Ratios", "GET", "/api/beta/keyratios/{symbol}", "Get key ratios", "symbol", None, "JSON", "Beta", "Beta key ratios feature"),
    ]
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO api_endpoints 
        (category, endpoint_name, method, url_path, description, required_params, optional_params, response_format, rate_limit_tier, use_case)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        description = VALUES(description),
        use_case = VALUES(use_case),
        updated_at = CURRENT_TIMESTAMP
        """
        
        count = 0
        for endpoint in endpoints:
            try:
                cursor.execute(insert_query, endpoint)
                count += 1
            except Exception as e:
                print(f"⚠️ Error inserting endpoint: {e}")
                continue
        
        conn.commit()
        print(f"✅ Inserted {count} API endpoints into database")
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"❌ Error inserting endpoints: {err}")
        return False


def main():
    print("\n" + "="*60)
    print("📡 Datasaham API Endpoints Setup")
    print("="*60 + "\n")
    
    print("Step 1: Creating API endpoints table...")
    if not create_api_endpoints_table():
        return False
    
    print("\nStep 2: Inserting Datasaham API endpoints...")
    if not insert_datasaham_endpoints():
        return False
    
    print("\n" + "="*60)
    print("✅ API endpoints stored successfully!")
    print("="*60 + "\n")
    return True


if __name__ == "__main__":
    main()
