
#!/usr/bin/env python3
"""
Extract complete orderbook from API
Saves to CSV dan JSON format
"""

import requests
import json
import csv
from datetime import datetime
from pathlib import Path

API_KEY = 'sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92'

def get_orderbook(symbol):
    """Fetch complete orderbook"""
    url = f"https://api.datasaham.io/api/emiten/{symbol}/orderbook"
    headers = {'x-api-key': API_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data['data']
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def save_to_csv(symbol, data):
    """Save orderbook to CSV (in Lots: 1 lot = 100 shares)"""
    if data is None:
        return None
    
    # Create data directory if not exists
    csv_dir = Path('data/orderbook')
    csv_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = csv_dir / f"{symbol}_orderbook_{timestamp}.csv"
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header dengan info saham
        writer.writerow(['Symbol', symbol])
        writer.writerow(['Last Price', data.get('lastprice')])
        writer.writerow(['Open', data.get('open')])
        writer.writerow(['High', data.get('high')])
        writer.writerow(['Low', data.get('low')])
        writer.writerow(['Volume (Lots)', int(data.get('volume', 0)) // 100])  # Convert to lots
        writer.writerow(['Frequency', data.get('frequency')])
        writer.writerow(['Value', data.get('value')])
        writer.writerow(['Timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # BID side
        writer.writerow(['BID SIDE'])
        writer.writerow(['Rank', 'Price', 'Frequency', 'Volume (Lots)'])
        
        bid_list = data.get('bid', [])
        for i, bid in enumerate(bid_list, 1):
            volume_lots = int(bid.get('volume', 0)) // 100  # Convert shares to lots
            writer.writerow([
                i,
                bid.get('price'),
                bid.get('que_num'),
                volume_lots
            ])
        
        writer.writerow([])
        
        # ASK side
        writer.writerow(['ASK SIDE'])
        writer.writerow(['Rank', 'Price', 'Frequency', 'Volume (Lots)'])
        
        ask_list = data.get('offer', [])
        for i, ask in enumerate(ask_list, 1):
            volume_lots = int(ask.get('volume', 0)) // 100  # Convert shares to lots
            writer.writerow([
                i,
                ask.get('price'),
                ask.get('que_num'),
                volume_lots
            ])
    
    print(f"✅ CSV saved: {csv_file}")
    return csv_file

def save_to_json(symbol, data):
    """Save orderbook to JSON (in Lots: 1 lot = 100 shares)"""
    if data is None:
        return None
    
    json_dir = Path('data/orderbook')
    json_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_file = json_dir / f"{symbol}_orderbook_{timestamp}.json"
    
    # Convert bid/ask volumes to lots
    bid_list = []
    for bid in data.get('bid', []):
        bid_list.append({
            'price': bid.get('price'),
            'que_num': bid.get('que_num'),
            'volume_shares': bid.get('volume'),
            'volume_lots': int(bid.get('volume', 0)) // 100  # Convert to lots
        })
    
    ask_list = []
    for ask in data.get('offer', []):
        ask_list.append({
            'price': ask.get('price'),
            'que_num': ask.get('que_num'),
            'volume_shares': ask.get('volume'),
            'volume_lots': int(ask.get('volume', 0)) // 100  # Convert to lots
        })
    
    # Convert total bid/offer to lots
    total_bid_lot_str = data.get('total_bid_offer', {}).get('bid', {}).get('lot', '0')
    total_ask_lot_str = data.get('total_bid_offer', {}).get('offer', {}).get('lot', '0')
    
    try:
        total_bid_lot_shares = int(str(total_bid_lot_str).replace(',', ''))
        total_ask_lot_shares = int(str(total_ask_lot_str).replace(',', ''))
    except:
        total_bid_lot_shares = 0
        total_ask_lot_shares = 0
    
    # Simplify for JSON - only key fields
    orderbook_data = {
        'symbol': symbol,
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'lastprice': data.get('lastprice'),
            'open': data.get('open'),
            'high': data.get('high'),
            'low': data.get('low'),
            'volume_shares': data.get('volume'),
            'volume_lots': int(data.get('volume', 0)) // 100,  # Convert to lots
            'frequency': data.get('frequency'),
            'value': data.get('value'),
        },
        'bid': bid_list,
        'ask': ask_list,
        'total_bid_offer': {
            'bid': {
                'freq': data.get('total_bid_offer', {}).get('bid', {}).get('freq'),
                'lot_shares': total_bid_lot_shares,
                'lot_lots': total_bid_lot_shares // 100
            },
            'offer': {
                'freq': data.get('total_bid_offer', {}).get('offer', {}).get('freq'),
                'lot_shares': total_ask_lot_shares,
                'lot_lots': total_ask_lot_shares // 100
            }
        },
        'foreign_flow': {
            'fbuy': data.get('fbuy'),
            'fsell': data.get('fsell'),
            'fnet': data.get('fnet'),
        },
        'ownership': {
            'domestic': data.get('domestic'),
            'foreign': data.get('foreign'),
        }
    }
    
    with open(json_file, 'w') as f:
        json.dump(orderbook_data, f, indent=2)
    
    print(f"✅ JSON saved: {json_file}")
    return json_file

def display_full_orderbook(symbol, data):
    """Display complete orderbook (converted to Lots)"""
    
    if data is None:
        print(f"❌ {symbol}: Data tidak tersedia")
        return
    
    bid_list = data.get('bid', [])
    ask_list = data.get('offer', [])
    current_price = data.get('lastprice', 0)
    
    # Header
    print(f"\n{'='*150}")
    print(f"  📊 {symbol.upper()} - COMPLETE ORDERBOOK (in LOTS)")
    print(f"  Last Price: Rp {float(current_price):,.0f} | Volume: {int(data.get('volume', 0)) // 100:,} lots | Frequency: {data.get('frequency'):,}")
    print(f"  Open: {data.get('open')} | High: {data.get('high')} | Low: {data.get('low')}")
    print(f"{'='*150}\n")
    
    # Column headers
    print(f"{'RANK':<6} {'FREQUENCY':<12} {'BID PRICE':<15} {'BID LOTS':<18} │ {'ASK PRICE':<15} {'ASK LOTS':<18} {'FREQUENCY':<12} {'RANK':<6}")
    print(f"{'-'*150}\n")
    
    # Display levels (use max length between bid and ask)
    max_levels = max(len(bid_list), len(ask_list))
    
    for i in range(max_levels):
        # Bid side
        bid_rank = ""
        bid_freq = ""
        bid_price = ""
        bid_lots = ""
        
        if i < len(bid_list):
            bid = bid_list[i]
            bid_rank = str(i + 1)
            bid_freq = str(bid.get('que_num', ''))
            bid_price = f"{float(bid.get('price', 0)):,.0f}"
            bid_lots = f"{int(bid.get('volume', 0)) // 100:,}"  # Convert to lots
        
        # Ask side
        ask_rank = ""
        ask_freq = ""
        ask_price = ""
        ask_lots = ""
        
        if i < len(ask_list):
            ask = ask_list[i]
            ask_price = f"{float(ask.get('price', 0)):,.0f}"
            ask_lots = f"{int(ask.get('volume', 0)) // 100:,}"  # Convert to lots
            ask_freq = str(ask.get('que_num', ''))
            ask_rank = str(i + 1)
        
        # Format output
        print(f"{bid_rank:<6} {bid_freq:<12} {bid_price:>15} {bid_lots:>18} │ {ask_price:>15} {ask_lots:>18} {ask_freq:<12} {ask_rank:<6}")
    
    # Summary
    print(f"\n{'-'*150}")
    
    total_bid_freq = data.get('total_bid_offer', {}).get('bid', {}).get('freq', 0)
    total_bid_lot_shares = data.get('total_bid_offer', {}).get('bid', {}).get('lot', 0)
    total_ask_freq = data.get('total_bid_offer', {}).get('offer', {}).get('freq', 0)
    total_ask_lot_shares = data.get('total_bid_offer', {}).get('offer', {}).get('lot', 0)
    
    try:
        total_bid_lot_shares = int(str(total_bid_lot_shares).replace(',', ''))
        total_ask_lot_shares = int(str(total_ask_lot_shares).replace(',', ''))
    except:
        total_bid_lot_shares = 0
        total_ask_lot_shares = 0
    
    # Convert to lots
    total_bid_lots = total_bid_lot_shares // 100
    total_ask_lots = total_ask_lot_shares // 100
    
    print(f"\n{'TOTAL SUMMARY':^150}")
    print(f"{'─'*150}")
    print(f"Bid Side:  Frequency: {total_bid_freq:>10} | Total Volume: {total_bid_lots:>18,} lots ({total_bid_lot_shares:,} shares)")
    print(f"Ask Side:  Frequency: {total_ask_freq:>10} | Total Volume: {total_ask_lots:>18,} lots ({total_ask_lot_shares:,} shares)")
    print(f"{'='*150}\n")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract Complete Orderbook')
    parser.add_argument('symbols', nargs='*', default=['BMRI', 'BBRI', 'BRMS'],
                        help='Stock symbols (default: BMRI BBRI BRMS)')
    parser.add_argument('--format', choices=['csv', 'json', 'both', 'display'], default='both',
                        help='Output format (default: both)')
    
    args = parser.parse_args()
    
    print("\n🔄 Extracting complete orderbook...\n")
    
    for symbol in args.symbols:
        print(f"📥 Fetching {symbol}...", end=' ', flush=True)
        data = get_orderbook(symbol)
        
        if data:
            print("✓\n")
            
            if args.format in ['csv', 'both']:
                save_to_csv(symbol, data)
            
            if args.format in ['json', 'both']:
                save_to_json(symbol, data)
            
            if args.format in ['display', 'both']:
                display_full_orderbook(symbol, data)
        else:
            print("✗")
    
    print("\n✅ Complete!")

if __name__ == "__main__":
    main()
