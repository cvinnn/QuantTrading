#!/usr/bin/env python3
"""
Real-time IDX Momentum Analysis
Combines IDX Momentum Indicator with live order book data from datasaham.io API
"""

import sys
import json
import requests
from typing import Dict, List
sys.path.insert(0, '/Users/cevin/Documents/QuantResearch/docs')
from idx_momentum_indicator import IDXMomentumIndicator

class RealTimeAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.datasaham.io/api/emiten"
        self.indicator = IDXMomentumIndicator()
    
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
    
    def extract_orderbook_data(self, data: Dict) -> tuple:
        """Extract key order book data for analysis"""
        if not data or not data.get('success'):
            return None
        
        ob = data['data']
        
        # Extract bid data
        bid_prices = [int(b['price']) for b in ob['bid'][:5]]
        bid_volumes = [int(b['volume']) for b in ob['bid'][:5]]
        bid_freqs = [int(b['que_num']) for b in ob['bid'][:5]]
        
        # Extract ask data
        ask_prices = [int(a['price']) for a in ob['offer'][:5]]
        ask_volumes = [int(a['volume']) for a in ob['offer'][:5]]
        ask_freqs = [int(a['que_num']) for a in ob['offer'][:5]]
        
        # Extract broker data
        haka_volume = ob['fbuy']  # Foreign aggressive buy
        haki_volume = ob['fsell']  # Foreign aggressive sell
        fnet = ob['fnet']
        
        return {
            'bid_prices': bid_prices,
            'bid_volumes': bid_volumes,
            'bid_freqs': bid_freqs,
            'ask_prices': ask_prices,
            'ask_volumes': ask_volumes,
            'ask_freqs': ask_freqs,
            'haka_volume': haka_volume / 1_000_000,  # Convert to millions
            'haki_volume': haki_volume / 1_000_000,
            'fnet': fnet,
            'current_price': int(ob['lastprice']),
            'high': int(ob['high']),
            'low': int(ob['low']),
            'volume': ob['volume'],
            'name': ob['name'],
            'symbol': ob['symbol']
        }
    
    def analyze(self, symbol: str) -> None:
        """Fetch order book and perform momentum analysis"""
        print(f"\n{'='*80}")
        print(f"REAL-TIME IDX MOMENTUM ANALYSIS - {symbol}")
        print(f"{'='*80}")
        
        # Fetch data
        data = self.fetch_orderbook(symbol)
        if not data:
            return
        
        ob_data = self.extract_orderbook_data(data)
        if not ob_data:
            return
        
        # Display order book summary
        print(f"\n📊 ORDER BOOK SNAPSHOT:")
        print(f"   Current Price: IDR {ob_data['current_price']:,}")
        print(f"   Day High: IDR {ob_data['high']:,} | Day Low: IDR {ob_data['low']:,}")
        print(f"   Volume: {ob_data['volume']:,} lots")
        print(f"   Foreign Net: IDR {ob_data['fnet']:,.0f}")
        
        # Calculate estimated net flow (simplified 3-day as recent vs historical)
        net_flow_3days = [ob_data['fnet'] / 1e9, ob_data['fnet'] / 1e9 * 0.8, ob_data['fnet'] / 1e9 * 0.6]
        
        # Analyze bullish accumulation
        bullish_result = self.indicator.detect_bullish_accumulation(
            bid_vols=ob_data['bid_volumes'],
            bid_freqs=ob_data['bid_freqs'],
            offer_vols=ob_data['ask_volumes'],
            offer_freqs=ob_data['ask_freqs'],
            haka_volume_recent=ob_data['haka_volume'],
            net_flow_3days=net_flow_3days
        )
        
        # Analyze bearish distribution
        price_momentum = min(1.0, abs(ob_data['fnet']) / 1e12)  # Normalize
        bearish_result = self.indicator.detect_bearish_distribution(
            price_momentum=price_momentum,
            bid_vols=ob_data['bid_volumes'],
            bid_freqs=ob_data['bid_freqs'],
            offer_vols=ob_data['ask_volumes'],
            offer_freqs=ob_data['ask_freqs'],
            haki_volume_recent=ob_data['haki_volume']
        )
        
        # Display results
        print(f"\n🎯 PATTERN ANALYSIS:")
        print(f"\n   BULLISH ACCUMULATION:")
        print(f"      Confidence: {bullish_result['confidence']}/100")
        print(f"      Action: {bullish_result['action']}")
        for key, val in bullish_result['details'].items():
            print(f"      ✓ {key}: {val}")
        
        print(f"\n   BEARISH DISTRIBUTION:")
        print(f"      Confidence: {bearish_result['confidence']}/100")
        print(f"      Action: {bearish_result['action']}")
        if bearish_result['confidence'] > 0:
            for key, val in bearish_result['details'].items():
                print(f"      {key}: {val}")
        else:
            print(f"      (No bearish signals detected)")
        
        # Overall signal
        print(f"\n{'='*80}")
        if bullish_result['confidence'] > 75:
            print(f"🟢 STRONG BULLISH SIGNAL - Consider entry")
        elif bullish_result['confidence'] > 60:
            print(f"🟡 MODERATE BULLISH - Watch for confirmation")
        elif bearish_result['confidence'] > 75:
            print(f"🔴 STRONG BEARISH SIGNAL - Exercise caution")
        else:
            print(f"⚫ NEUTRAL - Await clearer signals")
        
        print(f"{'='*80}\n")

if __name__ == "__main__":
    api_key = "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92"
    symbols = sys.argv[1:] if len(sys.argv) > 1 else ["BBCA", "PPRE"]
    
    analyzer = RealTimeAnalyzer(api_key)
    for symbol in symbols:
        analyzer.analyze(symbol)
