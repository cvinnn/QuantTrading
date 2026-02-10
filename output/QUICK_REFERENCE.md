# Quick Reference Guide - IDX Momentum API System

## Commands

### Single Stock Order Book
```bash
python3 db/orderbook_analyzer.py SYMBOL
```
Examples:
```bash
python3 db/orderbook_analyzer.py BBCA    # Bank Central Asia
python3 db/orderbook_analyzer.py PPRE    # PP Presisi
```

### Real-Time Momentum Analysis
```bash
python3 db/realtime_momentum_analyzer.py SYMBOL1 SYMBOL2 SYMBOL3
```
Example:
```bash
python3 db/realtime_momentum_analyzer.py BBCA PPRE ASII TLKM UNVR
```

### Multi-Stock Scanner (Automated)
```bash
python3 db/multi_stock_scanner.py [SYMBOLS...]
```
Examples:
```bash
# Scan top 10 stocks
python3 db/multi_stock_scanner.py

# Scan specific stocks
python3 db/multi_stock_scanner.py BBCA ASII TLKM JSMR HMSP
```

---

## Signal Interpretation

### Bullish Accumulation Confidence
| Confidence | Action | Signal |
|---|---|---|
| **≥ 85%** | **BUY_STRONG** | 🟢 Enter immediately |
| **75-84%** | **BUY** | 🟢 Enter with confirmation |
| **60-74%** | **WATCH** | 🟡 Monitor for strengthening |
| **< 60%** | **SKIP** | ⚫ Avoid entry |

### Bearish Distribution Confidence
| Confidence | Action | Signal |
|---|---|---|
| **≥ 90%** | **IMMEDIATE_EXIT** | 🔴 Close all positions NOW |
| **80-89%** | **CLOSE_POSITION** | 🔴 Exit within next bar |
| **60-79%** | **CAUTION** | 🟡 Tighten stops |
| **< 60%** | **MONITOR** | ⚫ Watch for confirmation |

### Overall Market Bias
| Condition | Bias | Action |
|---|---|---|
| Bullish > Bearish + 25 pts | 🟢 **BULLISH** | Look for entries |
| Bearish > Bullish + 25 pts | 🔴 **BEARISH** | Look for exits |
| Within 25 pts | ⚫ **NEUTRAL** | Wait for clarity |

---

## Pattern Details

### Bullish Accumulation (Pattern: BUY)
**Detected When:**
- ✓ Offer volume heavy (>1.5x bid) + freq high
- ✓ Bid volume light BUT frequency persistent
- ✓ Large HAKA volume (aggressive buying)
- ✓ Positive multi-day money flow

**Interpretation:**
Buyers patiently accumulating against resistance. Sellers defending hard. Supply will eventually exhaust → BREAK UP expected.

**Expected Move:** 0.5% - 2% over 1-5 days

---

### Bearish Distribution (Pattern: SELL)
**Detected When:**
- ✓ Offer volume light (<0.7x bid)
- ✓ Offer freq DROPPING (sellers losing confidence)
- ✓ Bid volume heavy + freq heavy (ready to dump)
- ✓ Red flag: bid < offer BUT bid_freq > offer_freq
- ✓ High HAKI volume (aggressive selling)

**Interpretation:**
Sellers distributing before crash. Imminent dump (GUYURAN) incoming.

**Expected Move:** -0.5% - 2% within minutes to hours

---

## Live Analysis from Today

### TLKM - BUY SIGNAL ✅
```
Price: IDR 3,380
Bullish: 85/100 → BUY_STRONG
Foreigners: BUYING
Setup: Buyers accumulating with conviction
Entry: Now @ bid or better
Stop: -0.8% (IDR 3,353)
Target1: +0.5% (IDR 3,397)
Target2: +1.0% (IDR 3,414)
Target3: +1.5% (IDR 3,431) with trailing stop
```

### BBCA - SELL SIGNAL 🔴
```
Price: IDR 7,500
Bearish: 95/100 → IMMEDIATE_EXIT
Foreigners: HEAVY SELLING (-IDR 714B)
Setup: Distribution with buyers losing control
Action: Close all long positions immediately
Avoid: New entries until pattern reverses
```

### PPRE - WATCH ⚫
```
Price: IDR 204
Bullish: 45/100 → WATCH (needs confirmation)
Foreigners: Slight buying (+IDR 2B)
Setup: Weak accumulation, too imbalanced
Action: Monitor for stronger signals
Wait for: Bullish > 60% or hold if already in
```

---

## Order Book Signals at a Glance

| Signal | Meaning | Action |
|--------|---------|--------|
| Volume Ratio (Ask/Bid) > 1.5 | Sellers pushing | CAUTION/SELL |
| Volume Ratio (Ask/Bid) < 0.7 | Buyers pushing | BULLISH/BUY |
| Volume Ratio (Ask/Bid) ≈ 1.0 | Balanced | NEUTRAL/WAIT |
| Queue Ratio Ask/Bid < 0.6 | Few sellers update | Sellers weak |
| Queue Ratio Ask/Bid > 1.5 | Frequent selling | Sellers aggressive |
| Spread < 5 pips | Tight spread | High liquidity |
| Spread > 20 pips | Wide spread | Low liquidity |
| Foreign Net POSITIVE | Foreigners buying | Bullish pressure |
| Foreign Net NEGATIVE | Foreigners selling | Bearish pressure |

---

## Decision Tree

```
                    ┌─ Score > 85%? ──→ BUY_STRONG ──→ ENTER
                    │
           BULLISH? ├─ Score 75-84%? ──→ BUY ──→ ENTER (wait confirmation)
                    │
                    ├─ Score 60-74%? ──→ WATCH ──→ MONITOR
                    │
                    └─ Score < 60%? ──→ SKIP ──→ NO ACTION
                    
                    ┌─ Score > 90%? ──→ IMMEDIATE_EXIT ──→ CLOSE NOW
                    │
           BEARISH? ├─ Score 80-89%? ──→ CLOSE_POSITION ──→ EXIT SOON
                    │
                    ├─ Score 60-79%? ──→ CAUTION ──→ TIGHTEN STOPS
                    │
                    └─ Score < 60%? ──→ MONITOR ──→ WATCH
```

---

## Risk Management Checklist

- [ ] Position size ≤ 2% of portfolio per trade
- [ ] Stop loss set before entry (usually -0.8%)
- [ ] Take profit levels pre-defined (usually +0.5%, +1.0%, +1.5%)
- [ ] Risk/Reward ratio ≥ 1:2 minimum
- [ ] Check news for earnings/events before entry
- [ ] Monitor for reversal of pattern (exit on opposite signal)
- [ ] Never add to losing position without new signal
- [ ] Scale out of winners instead of holding all

---

## Common Mistakes to Avoid

❌ **DON'T:**
- Enter on Neutral signals
- Ignore Bearish signals (always close if > 80%)
- Hold through Stop Loss
- Trade on rumors (wait for pattern confirmation)
- Risk > 2% per trade
- Revenge trade after loss
- Ignore technical levels (support/resistance)

✅ **DO:**
- Wait for signal confidence > 70% minimum
- Always use stop losses
- Scale entries on strong signals
- Take partial profits at targets
- Document every trade
- Review weekly performance
- Adjust thresholds based on results

---

## Troubleshooting

### No signal generated
- Check API connection: `curl -s "https://api.datasaham.io/api/emiten/BBCA/orderbook" --header 'x-api-key: sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92'`
- Verify stock symbol (case-sensitive)
- Check market hours (IDX trades 09:00-16:00 WIB)

### Slow analysis
- Reduce number of stocks scanned
- Increase wait time between requests (0.5s - 1.0s)
- Run during off-peak hours

### Inconsistent signals
- Refresh order book (live data changes frequently)
- Check for corporate actions or news
- Verify thresholds haven't drifted

---

## Support

**Files:**
- `/db/orderbook_analyzer.py` - Order book fetcher
- `/db/realtime_momentum_analyzer.py` - Momentum detector
- `/db/multi_stock_scanner.py` - Batch scanner
- `/docs/idx_momentum_indicator.py` - Core logic
- `/output/API_ORDERBOOK_INTEGRATION.md` - Full docs

**API Key:** `sbk_b0df044971dab991ddb075caf87b8df83ad0fbd2d67d3a92`

---

**Last Updated:** February 10, 2026, 14:30 UTC+7
