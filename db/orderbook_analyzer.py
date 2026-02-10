#!/usr/bin/env python3
"""
Real-time Order Book Analyzer for IDX Stocks
Fetches and analyzes order book data from datasaham.io API
"""

import json
import sys
import requests
from typing import Dict, List, Tuple

class OrderBookAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.datasaham.io/api/emiten"
    
    def fetch_orderbook(self, symbol: str) -> Dict:
        """Fetch order book data from API"""
        url = f"{self.base_url}/{symbol}/orderbook"
        headers = {'x-api-key': self.api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None
    
    def analyze_orderbook(self, data: Dict) -> None:
        """Analyze and display order book data"""
        if not data or not data.get('success'):
            print("Failed to get order book data")
            return
        
        ob = data['data']
        
        print("\n" + "=" * 80)
        print(f"{ob['name']} ({ob['symbol']}) - LIVE ORDER BOOK")
        print("=" * 80)
        
        # Market Status
        print(f"\n📊 MARKET STATUS:")
        print(f"   Last Price: IDR {ob['lastprice']:,}")
        print(f"   High: IDR {ob['high']:,} | Low: IDR {ob['low']:,} | Open: IDR {ob['open']:,}")
        print(f"   Volume: {ob['volume']:,} lots | Value: IDR {ob['value']:,}")
        print(f"   Frequency: {ob['frequency']:,} transactions")
        print(f"   Status: {ob['status']}")
        
        # Broker Activity
        print(f"\n💰 BROKER ACTIVITY:")
        print(f"   Foreign Buy: IDR {ob['fbuy']:,}")
        print(f"   Foreign Sell: IDR {ob['fsell']:,}")
        print(f"   Foreign Net: IDR {ob['fnet']:,} ({'BUY' if ob['fnet'] > 0 else 'SELL'})")
        print(f"   Domestic: {ob['domestic']}%")
        
        # Top Bids
        print(f"\n📈 TOP 5 BID SIDE (Buyers):")
        print(f"   {'Price':>8} | {'Volume':>12} | {'Queue':>8} | {'Avg/Que':>8}")
        print(f"   {'-'*8}|{'-'*12}|{'-'*8}|{'-'*8}")
        for bid in ob['bid'][:5]:
            price = int(bid['price'])
            volume = int(bid['volume'])
            queue = int(bid['que_num'])
            avg = volume / queue if queue > 0 else 0
            print(f"   {price:>8,} | {volume:>12,} | {queue:>8,} | {avg:>8.0f}")
        
        # Top Asks
        print(f"\n📉 TOP 5 OFFER SIDE (Sellers):")
        print(f"   {'Price':>8} | {'Volume':>12} | {'Queue':>8} | {'Avg/Que':>8}")
        print(f"   {'-'*8}|{'-'*12}|{'-'*8}|{'-'*8}")
        for ask in ob['offer'][:5]:
            price = int(ask['price'])
            volume = int(ask['volume'])
            queue = int(ask['que_num'])
            avg = volume / queue if queue > 0 else 0
            print(f"   {price:>8,} | {volume:>12,} | {queue:>8,} | {avg:>8.0f}")
        
        # Calculate totals
        total_bid_vol = sum(int(b['volume']) for b in ob['bid'])
        total_bid_que = sum(int(b['que_num']) for b in ob['bid'])
        total_ask_vol = sum(int(a['volume']) for a in ob['offer'])
        total_ask_que = sum(int(a['que_num']) for a in ob['offer'])
        
        print(f"\n📊 ORDER BOOK ANALYSIS:")
        print(f"   Total Bid: {total_bid_vol:,} lots ({total_bid_que:,} orders)")
        print(f"   Total Ask: {total_ask_vol:,} lots ({total_ask_que:,} orders)")
        print(f"   Volume Ratio (Ask/Bid): {total_ask_vol/total_bid_vol:.2f}x")
        print(f"   Queue Ratio (Ask/Bid): {total_ask_que/total_bid_que:.2f}x")
        
        # Spread Analysis
        best_bid = int(ob['bid'][0]['price'])
        best_ask = int(ob['offer'][0]['price'])
        spread = best_ask - best_bid
        spread_pct = (spread / best_ask) * 100
        
        print(f"\n🎯 SPREAD ANALYSIS:")
        print(f"   Best Bid: IDR {best_bid:,}")
        print(f"   Best Ask: IDR {best_ask:,}")
        print(f"   Spread: {spread} pips ({spread_pct:.3f}%)")
        print(f"   Mid Price: IDR {(best_bid + best_ask) / 2:,.0f}")
        
        # Liquidity Analysis
        top_bid_vol = int(ob['bid'][0]['volume'])
        top_ask_vol = int(ob['offer'][0]['volume'])
        
        print(f"\n💧 LIQUIDITY AT TOP LEVEL:")
        print(f"   Best Bid Liquidity: {top_bid_vol:,} lots")
        print(f"   Best Ask Liquidity: {top_ask_vol:,} lots")
        print(f"   Liquidity Ratio (Ask/Bid): {top_ask_vol/top_bid_vol:.2f}x")
        
        # Market Phase Detection
        print(f"\n🎭 MARKET MICROSTRUCTURE SIGNALS:")
        if total_ask_vol > total_bid_vol * 1.1:
            print(f"   ⚠️ More sellers than buyers (Ask/Bid: {total_ask_vol/total_bid_vol:.2f}x)")
        elif total_bid_vol > total_ask_vol * 1.1:
            print(f"   ✓ More buyers than sellers (Bid/Ask: {total_bid_vol/total_ask_vol:.2f}x)")
        else:
            print(f"   ➡️ Balanced order book")
        
        if spread <= 1:
            print(f"   ✓ Very tight spread ({spread} pips) - high liquidity")
        elif spread <= 3:
            print(f"   ✓ Tight spread ({spread} pips) - good liquidity")
        else:
            print(f"   ⚠️ Wide spread ({spread} pips) - lower liquidity")
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    api_key = "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92"
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BBCA"
    
    analyzer = OrderBookAnalyzer(api_key)
    data = analyzer.fetch_orderbook(symbol)
    analyzer.analyze_orderbook(data)
