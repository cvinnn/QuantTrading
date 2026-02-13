# Notebook Updates - Visual Guide

**Last Updated**: February 14, 2026

---

## 📊 New Feature: 10-Day Net Foreign Flow Analysis

### Display Format:

```
================================================================================
NET FOREIGN FLOW ANALYSIS - LAST 10 DAYS (BRMS)
================================================================================

📊 Flow Statistics:
   Positive Days: 5 days (BUY pressure)
   Negative Days: 5 days (SELL pressure)
   Neutral Days: 0 days

💰 Net Values:
   Total Net Flow: IDR 773 Million
   Average Daily: IDR 77 Million

📋 Daily Breakdown:
 Date  Net Flow (Juta IDR)
02/05                  360         🟢 BUY
02/06                  595         🟢 BUY
02/07                  544         🟢 BUY
02/08                 -379         🔴 SELL
02/09                  -34         🔴 SELL
02/10                 -170         🔴 SELL
02/11                 -413         🔴 SELL
02/12                  371         🟢 BUY
02/13                 -370         🔴 SELL
02/14                  269         🟢 BUY

[BAR CHART]:
595 |     ████     ████
544 |     ████     ████
360 |     ████     ████
    |_____|_____|_____|_____|_____|_____|_____|_____|_____|_____
    | 02/05 02/06 02/07 02/08 02/09 02/10 02/11 02/12 02/13 02/14
    |_____|_____|_____|_____|_____|_____|_____|_____|_____|_____
                    ████ ████ ████ ████
                   -379 -170 -413 -370

================================================================================
INTERPRETATION:
⚪ NEUTRAL: Equal positive and negative days (5 vs 5)
📈 Net accumulation over 10 days: IDR 773 Million (BULLISH)
================================================================================
```

---

## ✨ Updated Feature: Simplified Sentiment Analysis

### Before (Old Format - Verbose):

```
================================================================================
DETAILED RULE ANALYSIS:
================================================================================

rule_1: Top 10 Summed Bid Volume vs Offer Volume
   Status: ✗ FAIL | Points: 0/100
   Condition: (sum_bid_vol_top10 * 2) < sum_offer_vol_top10
   Details:
      sum_bid_vol_top10: 243252
      sum_offer_vol_top10: 531181
   → 243252 * 2 = 486504 < 531181? False

rule_2: Top Bid Volume vs Top Offer Volume
   Status: ✓ PASS | Points: 20/100
   Condition: (top_bid_vol * 1.8) < top_offer_vol
   Details:
      top_bid_vol: 14794
      top_offer_vol: 33295
   → 14794 * 1.8 = 26629.2 < 33295? True

[... 4 more rules with full details ...]

TOTAL CONFIDENCE: 20/100
```

### After (New Format - Concise):

```
================================================================================
TRADING SENTIMENT ANALYSIS (6-RULE SYSTEM) - BRMS
================================================================================

🎯 FINAL SIGNAL: ⬇️ BEARISH (Confidence: 20/100)
📊 Confidence Score: 20/100
📍 Sentiment: BEARISH

================================================================================
RULES PASSED:
================================================================================
✓ rule_2 (20 pts): Top Bid Volume vs Top Offer Volume

────────────────────────────────────────────────────────────────────────────────
TOTAL: 1/6 rules passed | 20/100 points
================================================================================

📊 SIGNAL INTERPRETATION:
⚫ BEARISH - Avoid entries, buyers weak
================================================================================
```

---

## Flow Chart: What Gets Displayed

```
NOTEBOOK FLOW
═════════════════════════════════════════════════════════════

Section 1: Data Loading
├─ Import libraries
├─ Fetch historical data
└─ Initialize indicator

Section 2: Live Order Book (from API)
├─ Fetch bid/ask prices, volumes, frequencies
├─ Display order book table
└─ Show aggressive volumes

    ↓

Section 3: 10-DAY FOREIGN FLOW (NEW) ← THIS IS NEW!
├─ Display 10-day flow table
│  ├─ Dates
│  ├─ Net flow values  
│  ├─ Day counts (positive/negative/neutral)
│  └─ Total & average
├─ Show BAR CHART (green for +, red for -)
└─ Interpretation (buying vs selling pressure)

    ↓

Section 4: 6-RULE SENTIMENT (SIMPLIFIED) ← UPDATED!
├─ Show final signal (🚀 BULLISH or 🔴 BEARISH)
├─ Show confidence score (0-100)
├─ Show ONLY PASSING RULES ← KEY CHANGE
│  └─ (Skip failed rules to reduce clutter)
├─ Show total rules passed
└─ Show interpretation

    ↓

Section 5: Additional Analysis (if needed)
└─ Staged entry strategy, exit strategy, etc.
```

---

## Data Interpretation Guide

### Green Bars = Positive Flow (Foreign Buyers)
- Shows net inflow of capital
- Indicates accumulation
- Bullish sentiment from foreign investors

### Red Bars = Negative Flow (Foreign Sellers)
- Shows net outflow of capital
- Indicates distribution
- Bearish sentiment from foreign investors

### Bar Chart Insights:
```
Pattern 1: Mostly GREEN → Buyers accumulating → BULLISH
    ▓▓▓
    ▓▓▓
    ▓▓▓
    ▓▓▓

Pattern 2: Mostly RED → Sellers dumping → BEARISH
        ▓▓▓
        ▓▓▓
        ▓▓▓
        ▓▓▓

Pattern 3: Mixed → Indecision → NEUTRAL
    ▓▓▓
        ▓▓▓
    ▓▓▓
        ▓▓▓
```

---

## Sentiment Analysis Quick Reference

### If RULES PASSED = 5-6:
- Confidence: 75-100 points
- Signal: 🚀 STRONG BULLISH
- Action: BUY or Aggressive Entry
- Interpretation: Sellers massively dominating

### If RULES PASSED = 3-4:
- Confidence: 45-70 points
- Signal: 🟡 MODERATE
- Action: WAIT for confirmation
- Interpretation: Mixed signals

### If RULES PASSED = 1-2:
- Confidence: 10-40 points
- Signal: 🔴 BEARISH
- Action: AVOID entries or EXIT
- Interpretation: Buyers dominating, sellers weak

### If RULES PASSED = 0:
- Confidence: 0 points
- Signal: 🔴 STRONG BEARISH
- Action: EXIT and AVOID
- Interpretation: Buyers extremely strong, sellers totally weak

---

## Key Improvements

### Foreign Flow Section:
✅ Shows what institutional investors (foreign funds) are doing  
✅ Bar chart makes trends immediately visible  
✅ 10-day history provides context  
✅ Positive/negative breakdown is clear  

### Sentiment Section:
✅ Shows only the important info (rules that passed)  
✅ Removes "noise" from failed rules  
✅ Faster to read and understand  
✅ Action-oriented interpretation  

---

## Example: Reading Both Sections Together

### Scenario 1: BULLISH on Both

```
FOREIGN FLOW:
📈 8 positive days, 2 negative days
→ Foreigners are BUYING (accumulating)

SENTIMENT:
✓ 5/6 rules passed (85 points)
🚀 VERY STRONG BULLISH
→ Order book shows SELLING PRESSURE

CONCLUSION:
🟢 STRONG BUY SIGNAL - Both confirm bullish
   • Foreign investors accumulating
   • Order book shows supply scarcity
   • Action: AGGRESSIVE ENTRY
```

### Scenario 2: BEARISH on Both

```
FOREIGN FLOW:
📉 2 positive days, 8 negative days
→ Foreigners are SELLING (distributing)

SENTIMENT:
✓ 0-1 rules passed (0-20 points)
🔴 STRONG BEARISH
→ Order book shows BUYING WEAKNESS

CONCLUSION:
🔴 STRONG SELL SIGNAL - Both confirm bearish
   • Foreign investors dumping
   • Order book shows weak demand
   • Action: EXIT or AVOID
```

### Scenario 3: Mixed (Divergence)

```
FOREIGN FLOW:
📈 6 positive days, 4 negative days
→ Foreigners slightly BULLISH

SENTIMENT:
✓ 1/6 rules passed (20 points)
🔴 BEARISH
→ Order book shows BUYING PRESSURE

CONCLUSION:
⚠️ MIXED SIGNALS - Divergence detected
   • Foreigners want to buy
   • But order book shows buyers weak
   • Action: WAIT for clarification
```

---

## Next Steps

1. **Review**: Look at the bar chart for 10-day trend
2. **Check**: How many foreign flow days are positive?
3. **Read**: How many rules passed in sentiment analysis?
4. **Decide**: Are foreign flows and sentiment aligned?
5. **Act**: Based on the combination of signals

---

**Updated**: February 14, 2026  
**Status**: ✅ Ready for Use
