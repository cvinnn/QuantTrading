#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/cevin/Documents/QuantResearch/docs')
from idx_momentum_indicator import IDXMomentumIndicator

# Initialize indicator
indicator = IDXMomentumIndicator()

# PPRE Data
ppre_bid_volumes = [2631, 15000, 22152, 49512, 34344]
ppre_bid_freqs = [24, 56, 107, 283, 58]
ppre_ask_volumes = [12184, 15670, 27443, 20969, 33015]
ppre_ask_freqs = [72, 55, 80, 73, 106]
ppre_haka_volume = 54586384
ppre_haki_volume = 34339318
ppre_net_flow_3days = [20.247, 16.198, 12.148]

# Run patterns (price_momentum no longer critical for bearish detection)
bullish_result = indicator.detect_bullish_accumulation(
    bid_vols=ppre_bid_volumes,
    bid_freqs=ppre_bid_freqs,
    offer_vols=ppre_ask_volumes,
    offer_freqs=ppre_ask_freqs,
    haka_volume_recent=ppre_haka_volume,
    net_flow_3days=ppre_net_flow_3days
)

bearish_result = indicator.detect_bearish_distribution(
    price_momentum=0.02,  # Low trend - but will still check for bearish pattern
    bid_vols=ppre_bid_volumes,
    bid_freqs=ppre_bid_freqs,
    offer_vols=ppre_ask_volumes,
    offer_freqs=ppre_ask_freqs,
    haki_volume_recent=ppre_haki_volume
)

# Determine dominant pattern
dominant_confidence = max(bullish_result['confidence'], bearish_result['confidence'])
if bullish_result['confidence'] > bearish_result['confidence']:
    dominant_pattern = "BULLISH_ACCUMULATION"
elif bearish_result['confidence'] > bullish_result['confidence']:
    dominant_pattern = "BEARISH_DISTRIBUTION"
else:
    dominant_pattern = "NEUTRAL"

print("=" * 80)
print("FINAL ANALYSIS SUMMARY - PPRE USING IDX MOMENTUM INDICATOR")
print("=" * 80)

print(f"\n🎯 IDX MOMENTUM INDICATOR - PATTERN DETECTION:")
print(f"   Bullish Accumulation: {bullish_result['confidence']}/100")
print(f"   Bearish Distribution: {bearish_result['confidence']}/100")
print(f"   Dominant Pattern: {dominant_pattern} ({dominant_confidence}/100)")

print(f"\n📋 TRADING RECOMMENDATION (Based on Pure Order Book Microstructure):")
print(f"   (Trend/Price momentum NOT a requirement anymore)")

# Check both patterns - whichever is higher takes precedence
if bearish_result['confidence'] >= bullish_result['confidence'] and bearish_result['confidence'] >= 50:
    print(f"\n   🔴 BEARISH DISTRIBUTION PATTERN DETECTED")
    print(f"      ACTION: {'IMMEDIATE_EXIT' if bearish_result['confidence'] >= 90 else 'CLOSE_POSITION' if bearish_result['confidence'] >= 80 else 'CAUTION' if bearish_result['confidence'] >= 60 else 'MONITOR'} ({bearish_result['confidence']}/100)")
    print(f"      Current Pattern Components:")
    for comp, val in bearish_result['details'].items():
        print(f"         ✓ {comp}: {val}")
    print(f"      Pattern Interpretation:")
    print(f"      • OFFER TIPIS: Sellers losing conviction")
    print(f"      • BID TEBAL: Remaining buyers heavy volume")
    print(f"      • HAKI HIGH: Aggressive sellers taking bids ({int(ppre_haki_volume):,} lots)")
    print(f"      → Imminent reversal → GUYURAN (dump) expected")

elif bullish_result['confidence'] >= 75:
    print(f"\n   🟢 BULLISH ACCUMULATION PATTERN DETECTED")
    print(f"      ACTION: {'BUY_STRONG' if bullish_result['confidence'] >= 85 else 'BUY'} ({bullish_result['confidence']}/100)")
    print(f"      Pattern Components:")
    for comp, val in bullish_result['details'].items():
        print(f"         ✓ {comp}: {val}")
    print(f"      Pattern Interpretation:")
    print(f"      • OFFER TEBAL: Sellers defending resistance heavily")
    print(f"      • BID PERSISTENT: Buyers patiently accumulating")
    print(f"      • HAKA LARGE: Aggressive buyers attacking offer ({int(ppre_haka_volume):,} lots)")
    print(f"      • NET FLOW: Positive multi-day accumulation")
    print(f"      → Supply exhaustion expected → BREAKUP incoming")

elif bullish_result['confidence'] >= 50:
    print(f"\n   🟡 WEAK BULLISH SIGNALS ({bullish_result['confidence']}/100)")
    print(f"      Current Pattern Components:")
    for comp, val in bullish_result['details'].items():
        print(f"         ✓ {comp}: {val}")
    print(f"      Missing Components:")
    print(f"         ✗ Offer volume NOT tebal enough (Ask/Bid ratio: {sum(ppre_ask_volumes)/sum(ppre_bid_volumes):.2f}x)")
    print(f"         ✗ Bid frequency NOT high enough vs Offer")
    freq_ratio = sum(ppre_bid_freqs) / sum(ppre_ask_freqs)
    print(f"         ✗ Bid/Offer Freq Ratio: {freq_ratio:.2f}x (need >1.2 for strong signal)")
    print(f"      ACTION: WAIT - Need stronger bid persistence and/or offer resistance")

else:
    print(f"\n   ⚫ NO CLEAR SIGNAL ({max(bullish_result['confidence'], bearish_result['confidence'])}/100)")
    print(f"      ACTION: MONITOR for pattern development")

print(f"\n💼 ORDER BOOK MICROSTRUCTURE:")
print(f"   Total Bid Volume: {int(sum(ppre_bid_volumes)):,} lots")
print(f"   Total Ask Volume: {int(sum(ppre_ask_volumes)):,} lots")
print(f"   Volume Ratio (Ask/Bid): {sum(ppre_ask_volumes)/sum(ppre_bid_volumes):.2f}x")

print(f"\n🔥 BROKER FLOW ACTIVITY:")
print(f"   HAKA (Aggressive Buy): {int(ppre_haka_volume):,} lots")
print(f"   HAKI (Aggressive Sell): {int(ppre_haki_volume):,} lots")
print(f"   Net: {'BUYING' if ppre_haka_volume > ppre_haki_volume else 'SELLING'}")

print(f"\n✅ SIGNAL QUALITY:")
if dominant_confidence >= 85:
    print(f"   🟢 STRONG - High conviction pattern")
elif dominant_confidence >= 75:
    print(f"   🟢 GOOD - Clear pattern formation")
elif dominant_confidence >= 60:
    print(f"   🟡 MODERATE - Developing pattern")
else:
    print(f"   ⚫ WEAK - Unclear signals, wait for confirmation")

print(f"\n⚠️ KEY INSIGHT:")
print(f"   Queue frequency is MORE important than volume alone!")
print(f"   Bid Frequency: {sum(ppre_bid_freqs)} updates")
print(f"   Offer Frequency: {sum(ppre_ask_freqs)} updates")
freq_ratio = sum(ppre_bid_freqs) / sum(ppre_ask_freqs)
print(f"   Ratio (Bid/Offer): {freq_ratio:.2f}x")
if freq_ratio > 1.2:
    print(f"   → Buyers MORE persistent (bullish)")
elif freq_ratio < 0.8:
    print(f"   → Sellers MORE persistent (bearish)")
else:
    print(f"   → Balanced market")

print("\n" + "=" * 80)

