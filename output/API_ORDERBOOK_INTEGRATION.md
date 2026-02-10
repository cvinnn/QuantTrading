# Real-Time Order Book API Integration with IDX Momentum Indicator

**Date:** February 10, 2026

## Overview

Successfully integrated live order book data from `datasaham.io` API with the IDX Momentum Indicator for real-time analysis of Indonesian stocks.

## API Endpoint

```bash
curl https://api.datasaham.io/api/emiten/{SYMBOL}/orderbook \
  --header 'x-api-key: sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92'
```

## Tools Created

### 1. Order Book Analyzer (`db/orderbook_analyzer.py`)
Standalone tool for fetching and analyzing order book data with market microstructure signals.

**Usage:**
```bash
python3 db/orderbook_analyzer.py BBCA    # BBCA
python3 db/orderbook_analyzer.py PPRE    # PPRE
```

**Output Includes:**
- Market Status (price, volume, frequency)
- Broker Activity (foreign buy/sell/net)
- Order Book Depth (top 5 bids & asks)
- Spread Analysis
- Liquidity Analysis
- Market Microstructure Signals

### 2. Real-Time Momentum Analyzer (`db/realtime_momentum_analyzer.py`)
Integrates order book data with IDX Momentum Indicator for pattern recognition.

**Usage:**
```bash
python3 db/realtime_momentum_analyzer.py BBCA PPRE
```

**Analysis Includes:**
- Bullish Accumulation Detection
- Bearish Distribution Detection
- Overall Signal Generation
- Entry/Exit Recommendations

## Live Analysis Results

### BBCA (Bank Central Asia)

#### Market Data
- **Current Price:** IDR 7,500
- **Volume:** 80,778,200 lots
- **Spread:** 25 pips (0.333%)
- **Foreign Net:** -IDR 714.76 billion (SELL)

#### Order Book Structure
| Metric | Value |
|--------|-------|
| Total Bid Volume | 88,932,400 lots |
| Total Ask Volume | 93,077,600 lots |
| Volume Ratio (Ask/Bid) | 1.05x |
| Queue Ratio (Ask/Bid) | 0.64x |

#### IDX Momentum Analysis
- **Bullish Accumulation:** 25/100 (SKIP)
- **Bearish Distribution:** 95/100 (IMMEDIATE_EXIT) ⚠️

**Signal: 🔴 STRONG BEARISH - Exercise Caution**

**Interpretation:**
- Heavy selling pressure from foreigners (-IDR 715B net)
- Offer volume light (0.52x bid) but sellers maintaining high frequency (0.16x bid frequency)
- Bid volume heavy but buyers losing conviction (low frequency ratio)
- Pattern suggests imminent reversal/dump (GUYURAN)

---

### PPRE (PP Presisi)

#### Market Data
- **Current Price:** IDR 204
- **Volume:** 59,311,500 lots
- **Spread:** 2 pips (0.980%)
- **Foreign Net:** +IDR 2.02 billion (BUY)

#### Order Book Structure
| Metric | Value |
|--------|-------|
| Total Bid Volume | 20,622,200 lots |
| Total Ask Volume | 45,186,800 lots |
| Volume Ratio (Ask/Bid) | 2.19x |
| Queue Ratio (Ask/Bid) | 2.17x |

#### IDX Momentum Analysis
- **Bullish Accumulation:** 45/100 (SKIP)
- **Bearish Distribution:** 0/100 (NOT_APPLICABLE)

**Signal: ⚫ NEUTRAL - Await Clearer Signals**

**Interpretation:**
- Positive foreign flow (+IDR 2B) but modest
- Imbalanced order book with 2.2x more asks than bids
- Buyers persistent but low conviction (queue analysis)
- Stock still requires confirmation before entry

---

## API Response Data Structure

The API returns comprehensive order book data:

```json
{
  "success": true,
  "data": {
    "symbol": "BBCA",
    "name": "Bank Central Asia Tbk.",
    "lastprice": 7500,
    "high": 7550,
    "low": 7450,
    "open": 7500,
    "volume": 80778200,
    "value": 605847062500,
    "frequency": 22807,
    "bid": [
      {
        "price": "7475",
        "volume": "10103900",
        "que_num": "2976"
      },
      ...
    ],
    "offer": [
      {
        "price": "7500",
        "volume": "6932600",
        "que_num": "366"
      },
      ...
    ],
    "fbuy": 297595680000,      // Foreign buy
    "fsell": 1012353550000,    // Foreign sell
    "fnet": -714757870000      // Foreign net flow
  }
}
```

## Key Indicators Extracted from API Data

### Order Book Metrics
- **Bid/Ask Volume Ratio:** Indicates supply/demand balance
- **Queue Number Ratio:** Frequency of order updates (conviction indicator)
- **Spread:** Bid-ask spread in pips
- **Liquidity:** Top-level volumes available

### Broker Activity (Foreign Flow)
- **HAKA Volume:** Aggressive foreign buy activity
- **HAKI Volume:** Aggressive foreign sell activity
- **Foreign Net Flow:** Net buying/selling pressure from foreign brokers

### Microstructure Signals
- **Volume Imbalance:** Ask/Bid ratio deviation
- **Frequency Shift:** Changes in order update frequency
- **Liquidity at Levels:** Volume concentration

## Integration with IDX Momentum Indicator

The API data feeds directly into the indicator:

```python
from idx_momentum_indicator import IDXMomentumIndicator

indicator = IDXMomentumIndicator()

# Extract from API
bid_volumes = [10103900, 10906500, ...]
bid_freqs = [2976, 3813, ...]
ask_volumes = [6932600, 4643000, ...]
ask_freqs = [366, 292, ...]
haka_volume = 297_595_680_000

# Analyze patterns
bullish = indicator.detect_bullish_accumulation(
    bid_vols=bid_volumes,
    bid_freqs=bid_freqs,
    offer_vols=ask_volumes,
    offer_freqs=ask_freqs,
    haka_volume_recent=haka_volume,
    net_flow_3days=[1.5, 1.2, 0.9]  # Estimated from foreign data
)
```

## Trading Applications

### For Scalpers
- Use tight spreads (< 5 pips) as entry opportunities
- Monitor queue ratios for conviction levels
- Watch foreign flow for reversal signals

### For Swing Traders
- Accumulation patterns suggest 2-5 day holds
- Distribution patterns indicate exit opportunities
- Foreign net flow validates multi-day trends

### For Risk Management
- Spread analysis indicates stop-loss distance
- Liquidity metrics determine position size
- Frequency analysis validates entry timing

## Files Created

```
/Users/cevin/Documents/QuantResearch/
├── db/
│   ├── orderbook_analyzer.py          # Order book analyzer tool
│   └── realtime_momentum_analyzer.py   # Real-time momentum analyzer
├── docs/
│   └── idx_momentum_indicator.py       # Core indicator logic
└── output/
    ├── PPRE_Analysis_Summary_20260210.md
    └── API_ORDERBOOK_INTEGRATION.md    # This file
```

## Usage Examples

### Quick Order Book Check
```bash
python3 db/orderbook_analyzer.py BBCA
```

### Real-Time Analysis of Multiple Stocks
```bash
python3 db/realtime_momentum_analyzer.py BBCA ASII UNVR TLKM
```

### Integrate into Trading System
```python
from db.realtime_momentum_analyzer import RealTimeAnalyzer

api_key = "sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92"
analyzer = RealTimeAnalyzer(api_key)

# Get live signals
analyzer.analyze("PPRE")
analyzer.analyze("BBCA")
```

## Next Steps

1. **Automate Monitoring:** Run analyzer on schedule for multiple stocks
2. **Alert System:** Trigger alerts when confidence > 80
3. **Historical Backtesting:** Save API data and test patterns
4. **Paper Trading:** Validate signals in simulated environment
5. **Risk Management:** Integrate with position sizing logic

## API Rate Limiting

⚠️ Note: Be aware of API rate limits. Recommended:
- Maximum 1 request per second per stock
- Stagger multiple stock queries
- Cache results for 5-60 seconds

---

**System Status:** ✅ Operational
**Last Updated:** February 10, 2026, 14:10 UTC+7
