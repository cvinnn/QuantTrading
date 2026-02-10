# PPRE Stock Analysis Using IDX Momentum Indicator
**Date:** February 10, 2026

## Executive Summary
PPRE has been analyzed using the IDX Momentum Indicator, which combines order flow analysis, broker action patterns, and multi-day accumulation signals to identify trading opportunities in the Indonesian stock market.

## Key Findings

### Current Market Status
- **Current Price:** IDR 204
- **52-Week High:** IDR 402
- **52-Week Low:** IDR 50
- **All-time Performance:** -45.8% (severe downtrend)
- **Bid-Ask Spread:** 1 IDR (0.50%) - very tight
- **Volume Ratio (Ask/Bid):** 1.12x

### Pattern Analysis Results

#### 1. Bullish Accumulation Pattern
- **Confidence Score:** 70/100
- **Action:** WATCH
- **Components Detected:**
  - ✓ Bid Persistence: PERSISTENT (468 total frequency updates)
  - ✓ HAKA Activity: LARGE (65,000 lots aggressive buying)
  - ✓ Multi-day Flow: POSITIVE (3 consecutive days of net buying)

**Interpretation:** Buyers are accumulating with patience despite lower volumes. Aggressive buyer activity (HAKA) suggests conviction. Three days of positive money flow indicate accumulation phase.

#### 2. Bearish Distribution Pattern
- **Confidence Score:** 0/100
- **Action:** NOT_APPLICABLE
- **Reason:** Price momentum too low for distribution pattern

**Interpretation:** No imminent reversal signals detected. Market is not in a strong enough uptrend to form the bearish distribution pattern.

### Market Microstructure

**Order Book Analysis:**
- Balanced frequency between bids and offers (0.95x ratio)
- Sellers maintaining presence with 493 total update frequency
- Buyers persistent with 468 total update frequency
- Market phase: TRANSITION/CONSOLIDATION

**Aggressive Volume Activity:**
- Buyer Activity (HAKA): 65,000 lots (bullish)
- Seller Activity (HAKI): 55,000 lots
- **Net Aggressive:** BULLISH (+10,000 lots favor buyers)

### Trading Recommendation

#### Entry Strategy
**Status:** ✓ Staged Entry AVAILABLE

**Entry Stage 1 (of 1):**
- Position Size: 300 lots (30% of 1,000 lot allocation)
- Entry Price: IDR 200 (bid level 1)
- Available Volume: 45,000 lots
- Strategy: Aggressive entry at deepest bid
- Order Type: LIMIT BUY @ IDR 200

#### Exit Strategy (3-Tier Approach)

| Target | Price | Profit | Size | Description |
|--------|-------|--------|------|-------------|
| T1 | IDR 201 | +0.5% | 300 lots (30%) | Light profit taking |
| T2 | IDR 202 | +1.0% | 400 lots (40%) | Partial profit |
| T3 | IDR 203 | +1.5% | 300 lots (30%) | Trailing stop |

#### Risk Management
- **Hard Stop Loss:** IDR 198 (-0.80%)
- **Trailing Stop:** IDR 151 (2x ATR)
- **Active Stop Level:** IDR 198
- **Risk per Trade:** IDR 2
- **Risk/Reward Ratio:** 1:1.87

### Overall Assessment
- **Overall Bias:** 🟢 BULLISH
- **Risk Level:** MODERATE
- **Confidence:** WATCH (70/100 - needs confirmation)

## Key Insights

1. **Accumulation Phase:** The stock shows classic accumulation patterns with buyer persistence despite heavy seller resistance.

2. **High Volume Activity:** HAKA (aggressive buyer) volume of 65,000 lots exceeds HAKI (seller) volume, indicating buyer conviction.

3. **Positive Broker Flow:** Three consecutive days of positive net money flow supports accumulation thesis.

4. **Support Level:** Stock trading near support (only IDR 50 away from 52-week low) - potential reversal zone.

5. **Risk Warning:** -45.8% all-time decline means stock is severely depressed. Use tight stops.

## Trading Action Plan

### For Buyers/Long Positions:
1. ✓ Pattern analysis supports entry at current levels
2. Place limit buy order @ IDR 200 (bid level 1)
3. Scale entry: Start with 30% allocation, add on confirmation
4. Take profits according to 3-tier strategy
5. **CRITICAL:** Use hard stop loss @ IDR 198

### For Existing Holders:
1. Monitor for bearish distribution signals (currently absent)
2. Consider taking partial profits at T1 (IDR 201)
3. Set trailing stops after profit targets hit
4. Watch for volume acceleration as confirmation signal

### Risk Warnings:
- Stock in severe downtrend; accumulation may fail
- No guarantee pattern will complete
- Use position sizing appropriate for risk tolerance
- Always use stop losses
- Monitor news/announcements that could trigger gap moves

---

**Analysis Tool:** IDX Momentum Indicator v1.0
**Notebook Location:** `/notebooks/03_PPRE_IDX_Momentum_Analysis.ipynb`
**Data Source:** yfinance (PPRE.JK)
