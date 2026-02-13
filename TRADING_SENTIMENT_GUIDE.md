# Trading Sentiment Analysis - Quick Reference Guide

**System**: 6-Rule Trading Sentiment Analysis  
**Target**: confidence ≥ 80 points = BULLISH, else BEARISH  
**Total**: 100 points maximum

---

## The 6 Rules Explained Simply

### Rule 1: Top 10 Bid Volume Stacked Against Offer (15 points)
- **Question**: Are bids weak compared to offers in top 10 levels?
- **Check**: `(sum_bid_vol_top10 × 2) < sum_offer_vol_top10`
- **Meaning**: If YES → sellers outnumber buyers significantly

### Rule 2: Top Bid vs Top Offer (20 points)
- **Question**: Is the best bid much weaker than the best offer?
- **Check**: `(top_bid_vol × 1.8) < top_offer_vol`
- **Meaning**: If YES → immediate market pressure is selling

### Rule 3: Offer Distribution Quality (30 points) ⭐ MOST IMPORTANT
- **Question**: Are seller orders well-distributed across price levels?
- **Logic**:
  1. Look at top 10 offers
  2. Remove the very big ones (> 80% of top)
  3. Find average of remaining
  4. Count how many are above average
  5. If 75%+ are above average → **PASS** (organized selling)
- **Meaning**: Sellers are providing continuous liquidity across multiple levels

### Rule 4: Bid Frequency vs Offer Frequency in Top 10 (15 points)
- **Question**: Are offers being updated more frequently than bids in top 10?
- **Check**: `(sum_bid_freq_top10 × 2) < sum_offer_freq_top10`
- **Meaning**: If YES → sellers are actively defending/increasing positions

### Rule 5: Total Bid Volume vs Total Offer Volume (10 points)
- **Question**: Overall, are there fewer bids than offers (counting all levels)?
- **Check**: `(all_bid_vol × 2) < all_offer_vol`
- **Meaning**: If YES → cumulative selling pressure

### Rule 6: Total Bid Frequency vs Total Offer Frequency (10 points)
- **Question**: Overall, are offers updated more often than bids (all levels)?
- **Check**: `(all_bid_freq × 2) < all_offer_freq`
- **Meaning**: If YES → continuous seller activity throughout the book

---

## Score Interpretation

```
100 Points    🚀 VERY STRONG BULLISH     Perfect selling pressure
90-99 Points  🚀 STRONG BULLISH          Excellent opportunity
85-89 Points  🟢 BULLISH                 Good entry signal
80-84 Points  🟢 MODERATE BULLISH        Wait for confirmation
70-79 Points  ⚫ WEAK BEARISH             Caution mode
0-69 Points   🔴 STRONG BEARISH          Avoid/Exit positions
```

---

## Example: Manual Calculation

### Scenario: PPRE Stock

**Order Book Data:**
```
Top 10 Bids:
Level 1: 875 IDR, Volume 515 lots, Freq 0
Level 2: 870 IDR, Volume 12836 lots, Freq 63
Level 3: 865 IDR, Volume 24618 lots, Freq 110
... (7 more levels)

Top 10 Offers:
Level 1: 880 IDR, Volume 47079 lots, Freq 0
Level 2: 885 IDR, Volume 29127 lots, Freq 202
Level 3: 890 IDR, Volume 73236 lots, Freq 204
... (7 more levels)
```

**Rule-by-Rule Calculation:**

1. **Rule 1**: Sum Bid Vol Top 10 = 388 lots
   - Check: 388 × 2 = 776 < 1,550? **YES** → +15 points ✓

2. **Rule 2**: Top Bid = 100, Top Offer = 250
   - Check: 100 × 1.8 = 180 < 250? **YES** → +20 points ✓

3. **Rule 3**: Top Offer = 10,000
   - Threshold: 10,000 × 0.8 = 8,000
   - Exclude: [10000, 8200]
   - Remaining: [2800, 2700, 2600, 2500, 2400, 2300, 1000, 900]
   - Average: 2,275
   - Above Average: 6 out of 8 = 75%
   - Check: 75% ≥ 75%? **YES** → +30 points ✓

4. **Rule 4**: Sum Bid Freq = 155, Sum Offer Freq = 775
   - Check: 155 × 2 = 310 < 775? **YES** → +15 points ✓

5. **Rule 5**: All Bid Vol = 5,000, All Offer Vol = 12,000
   - Check: 5,000 × 2 = 10,000 < 12,000? **YES** → +10 points ✓

6. **Rule 6**: All Bid Freq = 500, All Offer Freq = 1,200
   - Check: 500 × 2 = 1,000 < 1,200? **YES** → +10 points ✓

**Total: 100 points** → **🚀 BULLISH SIGNAL**

---

## Trading Strategy Based on Signals

### 🚀 BULLISH (≥80 points)
- **Price Action**: Sellers defending at higher prices
- **Market Meaning**: Buyers accumulating patiently, supply limited
- **Trading Action**: 
  - Entry signal: Buy on dips toward bid prices
  - Target: Expect upside breakout
  - Stop: Below support level

### 🔴 BEARISH (<80 points)
- **Price Action**: Buyers weak, insufficient bids
- **Market Meaning**: Sellers ready to dump, supply abundant
- **Trading Action**:
  - Exit signal: Close long positions
  - Avoid: New buy entries
  - Caution: Downside risk

---

## Implementation in Code

```python
from idx_momentum_indicator import IDXMomentumIndicator

# Initialize
indicator = IDXMomentumIndicator(thresholds={'bullish_threshold': 80})

# Analyze real order book data
result = indicator.analyze_sentiment(
    bid_prices=[1000, 999, 998, 997, 996, 995, 994, 993, 992, 991],
    bid_volumes=[100, 95, 90, 85, 80, 75, 70, 65, 60, 55],
    bid_freqs=[20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
    offer_prices=[1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    offer_volumes=[250, 240, 230, 220, 210, 200, 190, 180, 170, 160],
    offer_freqs=[100, 95, 90, 85, 80, 75, 70, 65, 60, 55]
)

# Get signal
print(result['summary']['signal'])  # 🚀 BULLISH (Confidence: XX/100)
print(result['sentiment'])          # BULLISH
print(result['confidence'])         # 85 (example)

# Check individual rules
for rule_key, rule_data in result['rules'].items():
    if rule_data['passed']:
        print(f"✓ {rule_key}: {rule_data['name']} (+{rule_data['points']} pts)")
    else:
        print(f"✗ {rule_key}: {rule_data['name']} (0 pts)")
```

---

## Tips for Using the Indicator

### Do's ✅
- Use REAL-TIME order book data (not EOD snapshots)
- Check all 6 rules for comprehensive picture
- Look for patterns over multiple timestamps
- Combine with price action and trend analysis
- Adjust threshold based on your risk tolerance

### Don'ts ❌
- Don't rely solely on single rule
- Don't use stale order book data (>1 minute old)
- Don't ignore Rule 3 (it has highest weight at 30 points)
- Don't trade against the broader trend
- Don't use confidence < 70 for entries

---

## Threshold Customization

```python
# Conservative: Only strongest signals (85+ points)
indicator = IDXMomentumIndicator(thresholds={'bullish_threshold': 85})

# Standard: Default setting (80 points)
indicator = IDXMomentumIndicator(thresholds={'bullish_threshold': 80})

# Aggressive: More trading opportunities (75 points)
indicator = IDXMomentumIndicator(thresholds={'bullish_threshold': 75})
```

---

## Data Requirements

To use this indicator, you need:

```
Bid Data (Top 10+ levels):
  - Bid prices
  - Bid volumes
  - Bid frequencies (order update count)

Ask/Offer Data (Top 10+ levels):
  - Offer prices
  - Offer volumes
  - Offer frequencies (order update count)
```

**Data Source**: `api.datasaham.io` or your broker's API

---

## Example Results

### Bullish Case:
```
Rule 1: ✓ PASS (+15) - Bids weak vs offers in top 10
Rule 2: ✓ PASS (+20) - Best bid weak vs best offer
Rule 3: ✓ PASS (+30) - Offers well-distributed (75%+)
Rule 4: ✓ PASS (+15) - Offer freq high in top 10
Rule 5: ✓ PASS (+10) - Total bids << offers
Rule 6: ✓ PASS (+10) - Offer freq high overall
------------------------
TOTAL: 100 points → 🚀 BULLISH
```

### Bearish Case:
```
Rule 1: ✗ FAIL  (0) - Bids strong vs offers
Rule 2: ✗ FAIL  (0) - Best bid strong vs offer
Rule 3: ✗ FAIL  (0) - Offers scattered (<75%)
Rule 4: ✗ FAIL  (0) - Bid freq high in top 10
Rule 5: ✗ FAIL  (0) - Total bids >> offers
Rule 6: ✗ FAIL  (0) - Bid freq high overall
------------------------
TOTAL: 0 points → 🔴 BEARISH
```

---

**Generated**: February 14, 2026  
**Indicator Version**: 6-Rule Trading Sentiment Analysis v1.0
