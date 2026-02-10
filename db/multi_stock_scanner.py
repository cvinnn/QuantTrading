#!/usr/bin/env python3
"""
Multi-Stock Scanner for IDX Momentum Signals
Scans multiple stocks and alerts on high-confidence patterns
"""

import sys
import json
import requests
import time
from typing import Dict, List
sys.path.insert(0, '/Users/cevin/Documents/QuantResearch/docs')
from idx_momentum_indicator import IDXMomentumIndicator

class MultiStockScanner:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.datasaham.io/api/emiten"
        self.indicator = IDXMomentumIndicator()
        self.results = {}
    
    def fetch_orderbook(self, symbol: str) -> Dict:
        """Fetch order book data from API"""
        url = f"{self.base_url}/{symbol}/orderbook"
        headers = {'x-api-key': self.api_key}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Analyze single stock"""
        data = self.fetch_orderbook(symbol)
        if not data or not data.get('success'):
            return None
        
        ob = data['data']
        
        # Extract data
        bid_volumes = [int(b['volume']) for b in ob['bid'][:5]]
        bid_freqs = [int(b['que_num']) for b in ob['bid'][:5]]
        ask_volumes = [int(a['volume']) for a in ob['offer'][:5]]
        ask_freqs = [int(a['que_num']) for a in ob['offer'][:5]]
        haka = ob['fbuy'] / 1_000_000
        haki = ob['fsell'] / 1_000_000
        
        net_flow = [ob['fnet'] / 1e9, ob['fnet'] / 1e9 * 0.8, ob['fnet'] / 1e9 * 0.6]
        
        # Analyze
        bullish = self.indicator.detect_bullish_accumulation(
            bid_vols=bid_volumes,
            bid_freqs=bid_freqs,
            offer_vols=ask_volumes,
            offer_freqs=ask_freqs,
            haka_volume_recent=haka,
            net_flow_3days=net_flow
        )
        
        bearish = self.indicator.detect_bearish_distribution(
            price_momentum=min(1.0, abs(ob['fnet']) / 1e12),
            bid_vols=bid_volumes,
            bid_freqs=bid_freqs,
            offer_vols=ask_volumes,
            offer_freqs=ask_freqs,
            haki_volume_recent=haki
        )
        
        return {
            'symbol': symbol,
            'name': ob['name'],
            'price': int(ob['lastprice']),
            'volume': ob['volume'],
            'bullish_conf': bullish['confidence'],
            'bullish_action': bullish['action'],
            'bearish_conf': bearish['confidence'],
            'bearish_action': bearish['action'],
            'fnet': ob['fnet'],
            'spread': int(ob['offer'][0]['price']) - int(ob['bid'][0]['price'])
        }
    
    def scan_stocks(self, symbols: List[str]) -> None:
        """Scan multiple stocks"""
        print("\n" + "="*100)
        print("IDX MOMENTUM SCANNER - REAL-TIME MULTI-STOCK ANALYSIS")
        print("="*100)
        
        bullish_signals = []
        bearish_signals = []
        neutral_stocks = []
        
        for i, symbol in enumerate(symbols, 1):
            print(f"\n[{i}/{len(symbols)}] Analyzing {symbol}...", end=" ", flush=True)
            result = self.analyze_stock(symbol)
            
            if result:
                self.results[symbol] = result
                
                # Categorize
                if result['bullish_conf'] > 75:
                    bullish_signals.append(result)
                    print("🟢 BULLISH")
                elif result['bearish_conf'] > 75:
                    bearish_signals.append(result)
                    print("🔴 BEARISH")
                else:
                    neutral_stocks.append(result)
                    print("⚫ NEUTRAL")
            else:
                print("⚠️ ERROR")
            
            # Rate limit
            if i < len(symbols):
                time.sleep(0.5)
        
        # Display Results
        print("\n" + "="*100)
        print("SCAN RESULTS SUMMARY")
        print("="*100)
        
        # Bullish Signals
        if bullish_signals:
            print(f"\n🟢 BULLISH SIGNALS ({len(bullish_signals)}):")
            print(f"{'Symbol':<8} | {'Name':<30} | {'Price':>8} | {'Bull %':>7} | {'FNet':>12} | {'Signal':<15}")
            print("-" * 100)
            for result in sorted(bullish_signals, key=lambda x: x['bullish_conf'], reverse=True):
                fnet_str = f"{'BUY' if result['fnet'] > 0 else 'SELL'}"
                print(f"{result['symbol']:<8} | {result['name']:<30} | {result['price']:>8,} | {result['bullish_conf']:>7.0f}% | {fnet_str:>12} | {result['bullish_action']:<15}")
        
        # Bearish Signals
        if bearish_signals:
            print(f"\n🔴 BEARISH SIGNALS ({len(bearish_signals)}):")
            print(f"{'Symbol':<8} | {'Name':<30} | {'Price':>8} | {'Bear %':>7} | {'FNet':>12} | {'Signal':<15}")
            print("-" * 100)
            for result in sorted(bearish_signals, key=lambda x: x['bearish_conf'], reverse=True):
                fnet_str = f"{'BUY' if result['fnet'] > 0 else 'SELL'}"
                print(f"{result['symbol']:<8} | {result['name']:<30} | {result['price']:>8,} | {result['bearish_conf']:>7.0f}% | {fnet_str:>12} | {result['bearish_action']:<15}")
        
        # Neutral
        if neutral_stocks:
            print(f"\n⚫ NEUTRAL ({len(neutral_stocks)}):")
            print(f"{'Symbol':<8} | {'Name':<30} | {'Price':>8} | {'Bull %':>7} | {'Bear %':>7}")
            print("-" * 100)
            for result in sorted(neutral_stocks, key=lambda x: x['bullish_conf'], reverse=True):
                print(f"{result['symbol']:<8} | {result['name']:<30} | {result['price']:>8,} | {result['bullish_conf']:>7.0f}% | {result['bearish_conf']:>7.0f}%")
        
        # Statistics
        print(f"\n" + "="*100)
        print(f"STATISTICS:")
        print(f"  Total Scanned: {len(symbols)}")
        print(f"  Bullish Signals: {len(bullish_signals)} ({len(bullish_signals)/len(symbols)*100:.1f}%)")
        print(f"  Bearish Signals: {len(bearish_signals)} ({len(bearish_signals)/len(symbols)*100:.1f}%)")
        print(f"  Neutral: {len(neutral_stocks)} ({len(neutral_stocks)/len(symbols)*100:.1f}%)")
        print("="*100 + "\n")
    
    def export_results(self, filename: str = "/tmp/scan_results.json") -> None:
        """Export results to JSON"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"✓ Results exported to {filename}")

if __name__ == "__main__":
    api_key = "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92"
    
    # Popular IDX stocks
    default_stocks = [
        "BBCA", "BBRI", "BCA",    # Banks
        "ASII", "UNVR", "INDF",   # Large caps
        "TLKM", "JSMR", "HMSP",   # Mid caps
        "PPRE", "PGAS", "GGRM"    # Others
    ]
    
    symbols = sys.argv[1:] if len(sys.argv) > 1 else default_stocks
    
    scanner = MultiStockScanner(api_key)
    scanner.scan_stocks(symbols)
    scanner.export_results()
