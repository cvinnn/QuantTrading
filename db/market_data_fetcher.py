"""
Market Data Fetcher - Fetch marketcap dari yfinance
Runs every 15 minutes during IDX market hours
"""

import yfinance as yf
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, time
import time as time_module
import sys
import os
import pytz

# Add parent directory to path for config imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DB_CONFIG


class MarketDataFetcher:
    """Fetch dan store market data dari yfinance"""
    
    def __init__(self):
        self.config = DB_CONFIG
        self.tz = pytz.timezone('Asia/Jakarta')
        # IDX market hours
        self.market_open_morning = time(8, 45)
        self.market_close_morning = time(12, 0)
        self.market_open_afternoon = time(13, 30)
        self.market_close_afternoon = time(16, 15)
    
    def is_market_open(self):
        """Check jika market sedang buka"""
        now = datetime.now(self.tz).time()
        is_open = (self.market_open_morning <= now <= self.market_close_morning or 
                   self.market_open_afternoon <= now <= self.market_close_afternoon)
        return is_open
    
    def get_all_saham_codes(self):
        """Get semua stock codes dari database"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            query = "SELECT kode_saham FROM saham"
            cursor.execute(query)
            results = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            codes = [row[0] for row in results]
            return codes
        except mysql.connector.Error as err:
            print(f"❌ Error fetching saham codes: {err}")
            return []
    
    def fetch_marketcap_from_yfinance(self, kode_saham):
        """
        Fetch marketcap dari yfinance untuk single stock
        Format: KODE.JK untuk IDX stocks
        """
        try:
            ticker_symbol = f"{kode_saham}.JK"
            stock = yf.Ticker(ticker_symbol)
            
            # Get info
            info = stock.info
            marketcap = info.get('marketCap')
            price = info.get('currentPrice')
            volume = info.get('volume')
            
            return {
                'marketcap_idr': marketcap,
                'price': price,
                'volume': volume
            }
        except Exception as e:
            print(f"⚠️ Error fetching {kode_saham}: {e}")
            return None
    
    def insert_market_data(self, kode_saham, marketcap_idr, price, volume):
        """Insert market data ke database"""
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor()
            
            now = datetime.now(self.tz)
            tanggal = now.date()
            waktu = now.time()
            
            insert_query = """
            INSERT INTO market_data (kode_saham, marketcap_idr, price, volume, tanggal, waktu)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            marketcap_idr = VALUES(marketcap_idr),
            price = VALUES(price),
            volume = VALUES(volume),
            updated_at = CURRENT_TIMESTAMP
            """
            
            cursor.execute(insert_query, (
                kode_saham,
                marketcap_idr,
                price,
                volume,
                tanggal,
                waktu
            ))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error inserting market data for {kode_saham}: {err}")
            return False
    
    def fetch_and_store_all(self):
        """Fetch dan store semua stocks"""
        print(f"\n⏰ {datetime.now(self.tz).strftime('%Y-%m-%d %H:%M:%S')}")
        print("📊 Fetching market data from yfinance...")
        
        codes = self.get_all_saham_codes()
        if not codes:
            print("❌ No saham codes found")
            return False
        
        print(f"📈 Fetching {len(codes)} stocks...")
        
        success_count = 0
        for i, kode in enumerate(codes, 1):
            data = self.fetch_marketcap_from_yfinance(kode)
            
            if data and data['marketcap_idr']:
                if self.insert_market_data(
                    kode,
                    data['marketcap_idr'],
                    data['price'],
                    data['volume']
                ):
                    success_count += 1
                    if i % 50 == 0:
                        print(f"  ✅ Processed {i}/{len(codes)} stocks")
            
            # Rate limiting
            time_module.sleep(0.1)
        
        print(f"✅ Successfully stored {success_count}/{len(codes)} stocks")
        return True
    
    def run_scheduler(self):
        """Run continuous scheduler - fetch every 15 minutes during market hours"""
        print("🚀 Market Data Fetcher Started")
        print("⏰ Will fetch every 15 minutes during market hours")
        print("📍 Market hours: 08:45-12:00, 13:30-16:15 (Jakarta Time)")
        
        last_fetch = None
        
        while True:
            now = datetime.now(self.tz)
            
            # Check if market is open
            if self.is_market_open():
                # Fetch every 15 minutes
                if last_fetch is None or (now - last_fetch).total_seconds() >= 900:  # 900 = 15 min
                    self.fetch_and_store_all()
                    last_fetch = now
                else:
                    wait_time = 900 - (now - last_fetch).total_seconds()
                    print(f"⏳ Next fetch in {int(wait_time)} seconds...")
            else:
                print(f"🔴 Market closed. Next check in 5 minutes...")
                last_fetch = None  # Reset on market close
            
            # Check every 60 seconds
            time_module.sleep(60)


def main():
    """Main entry point"""
    fetcher = MarketDataFetcher()
    
    # Option 1: Single fetch
    # fetcher.fetch_and_store_all()
    
    # Option 2: Continuous scheduler
    fetcher.run_scheduler()


if __name__ == "__main__":
    main()
