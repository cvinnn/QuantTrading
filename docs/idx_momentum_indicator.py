"""
IDX Momentum Indicator - Custom Indicator for Indonesian Stock Market Scalping
Based on Order Flow Analysis + Broker Action + Multi-day Accumulation

Key Patterns:
1. BULLISH ACCUMULATION: Offer tebal + freq jual tebal vs Bid tipis persistent + freq beli tipis
   → Buyers accumulating against resistance → Supply habis → BREAK NAIK
   
2. BEARISH DISTRIBUTION: Harga naik + Offer tipis + Bid tebal + Freq shift (offer down, bid up)
   → Imminent reversal → GUYURAN (dump)

Author: Research & Development
Date: February 2026
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class OrderBookSnapshot:
    """Real-time order book snapshot"""
    bid_prices: List[float]
    bid_volumes: List[float]
    bid_freqs: List[int]
    ask_prices: List[float]
    ask_volumes: List[float]
    ask_freqs: List[int]
    current_price: float
    timestamp: str


@dataclass
class BrokerAction:
    """Daily broker action summary"""
    date: str
    buy_value: float
    buy_lots: float
    buy_avg_price: float
    sell_value: float
    sell_lots: float
    sell_avg_price: float
    closing_price: float


class IDXMomentumIndicator:
    """
    Corrected indicator based on actual IDX market microstructure
    
    KEY INSIGHT: Frekuensi update order (bid freq vs offer freq) adalah 
    indikator conviction lebih penting daripada sekedar volume!
    """
    
    def __init__(self, thresholds: Optional[Dict] = None):
        """Initialize indicator with configurable thresholds"""
        self.thresholds = thresholds or {
            'large_volume': 50000,  # Large HAKA/HAKI volume threshold
            'accumulation_confidence': 75,
            'distribution_confidence': 80,
            'min_multi_day': 2,  # Minimum positive days for accumulation
        }
        self.price_history = []
        self.broker_history = []
    
    # ===== PATTERN 1: BULLISH ACCUMULATION =====
    def detect_bullish_accumulation(self, 
                                   bid_vols: List[float], 
                                   bid_freqs: List[int],
                                   offer_vols: List[float], 
                                   offer_freqs: List[int],
                                   haka_volume_recent: float,
                                   net_flow_3days: List[float]) -> Dict:
        """
        PATTERN BULLISH ACCUMULATION:
        
        1. OFFER TIPIS + freq jual TIPIS (sellers losing conviction, leaving market)
        2. BID TEBAL + freq beli TEBAL (ready to dump, high buying intent)
        3. RED FLAG SPECIAL: bid_volume > offer_volume AND bid_freq > offer_freq
           → Heavy buyers tapi TERUS-TERUS update bid → Accumulation ongoing
        4. HAKA volume tinggi (buyers aggressive buying)
        5. Net Money Flow POSITIF (2-3 hari accumulation)
        
        INTERPRETATION: Buyers strongly accumulating against weak offer resistance.
        Eventual outcome: Supply habis → harga BREAK NAIK
        
        Args:
            bid_vols: List of bid volumes (top 5 levels)
            bid_freqs: List of bid frequencies (top 5 levels)
            offer_vols: List of offer volumes (top 5 levels)
            offer_freqs: List of offer frequencies (top 5 levels)
            haka_volume_recent: Recent aggressive buy volume
            net_flow_3days: Net money flow for past 3 days
        
        Returns:
            Dict with pattern, confidence score, details, and action
        """
        
        confidence_score = 0
        details = {}
        
        # Calculate totals
        offer_total = sum(offer_vols[:5]) if offer_vols else 0
        bid_total = sum(bid_vols[:5]) if bid_vols else 0
        offer_freq_total = sum(offer_freqs[:5]) if offer_freqs else 0
        bid_freq_total = sum(bid_freqs[:5]) if bid_freqs else 0
        
        # Component 1: Offer tebal + freq jual tebal (sellers resisting)
        if offer_total > 0 and bid_total > 0:
            volume_ratio = offer_total / bid_total
            
            if volume_ratio > 1.3:  # Offer tebal
                confidence_score += 20
                details['offer_volume'] = f'TEBAL ({volume_ratio:.2f}x) ✓'
        
        if offer_freq_total > 0 and bid_freq_total > 0:
            freq_ratio = offer_freq_total / bid_freq_total
            
            if freq_ratio > 1.2:  # Freq jual tebal
                confidence_score += 15
                details['offer_frequency'] = f'TEBAL ({freq_ratio:.2f}x) ✓'
        
        # Component 2: Bid tipis + freq beli tipis (buyers patient/accumulating)
        if bid_total < offer_total * 0.8:  # Bid tipis
            confidence_score += 20
            details['bid_volume'] = f'TIPIS vs offer ✓'
        
        if bid_freq_total < offer_freq_total * 0.85:  # Freq beli tipis
            confidence_score += 20
            details['bid_frequency'] = f'TIPIS vs offer ✓'
        
        # Component 3: RED FLAG - offer > bid AND offer freq > bid freq
        if offer_total > bid_total and offer_freq_total > bid_freq_total:
            confidence_score += 25  # STRONG BULLISH FLAG
            details['RED_FLAG'] = 'offer>bid AND offer_freq>bid_freq ✓✓✓'
        
        # Component 4: High HAKA activity (buyers aggressive)
        if haka_volume_recent > self.thresholds['large_volume']:
            confidence_score += 15
            details['haka_activity'] = f'HIGH ({haka_volume_recent:,.0f}) ✓'
        
        # Component 5: Multi-day positive flow
        if net_flow_3days and len(net_flow_3days) >= 2:
            positive_days = sum(1 for flow in net_flow_3days if flow > 0)
            if positive_days >= self.thresholds['min_multi_day']:
                confidence_score += 5
                details['multi_day_flow'] = f'POSITIVE ({positive_days}/{len(net_flow_3days)} days) ✓'
        
        return {
            'pattern': 'BULLISH_ACCUMULATION',
            'confidence': min(confidence_score, 100),
            'details': details,
            'action': self._get_action_bullish(confidence_score),
            'description': 'Buyers strong accumulation - breakup incoming'
        }
    
    # ===== PATTERN 2: BEARISH DISTRIBUTION/RED FLAG =====
    def detect_bearish_distribution(self, 
                                   price_momentum: float,
                                   bid_vols: List[float], 
                                   bid_freqs: List[int],
                                   offer_vols: List[float], 
                                   offer_freqs: List[int],
                                   haki_volume_recent: float,
                                   haka_volume_recent: float = None,
                                   net_flow_3days: List[float] = None) -> Dict:
        """
        PATTERN BEARISH DISTRIBUTION = IMMINENT GUYURAN!
        
        NOTE: Trend/price momentum is NOT a requirement anymore!
        Pattern can be detected at any price level based on PURE ORDER BOOK microstructure
        
        Key Signals (ADJUSTED LOGIC):
        1. bid vol per tick < offer vol per tick (at least 3-4 out of top 5 levels)
        2. bid vol sum * 1.75 < offer vol sum (top 10 summed)
        3. bid freq per tick < offer freq per tick (at least 3-4 out of top 5 levels)
        4. bid freq sum * 1.75 < offer freq sum (top 10 summed)
        5. HAKI > HAKA (sellers more aggressive than buyers)
        6. Negative net flow 3-day trend (sellers accumulating, distribution phase)
        
        Result: STRONG BEARISH SIGNAL (sellers dominating)
        
        Args:
            price_momentum: Price momentum indicator (not used as requirement)
            bid_vols: List of bid volumes (top 10 levels)
            bid_freqs: List of bid frequencies (top 10 levels)
            offer_vols: List of offer volumes (top 10 levels)
            offer_freqs: List of offer frequencies (top 10 levels)
            haki_volume_recent: Recent aggressive sell volume
            haka_volume_recent: Recent aggressive buy volume
            net_flow_3days: Net flow for past 3 days
        
        Returns:
            Dict with pattern, confidence score, details, and action
        """
        
        confidence_score = 0
        details = {}
        
        # Calculate totals (using top 10 levels for summed checks)
        offer_total = sum(offer_vols[:10]) if offer_vols else 0
        bid_total = sum(bid_vols[:10]) if bid_vols else 0
        offer_freq_total = sum(offer_freqs[:10]) if offer_freqs else 0
        bid_freq_total = sum(bid_freqs[:10]) if bid_freqs else 0
        
        # Component 1: Check bid vol per tick > offer vol per tick (at least 3-4 out of top 5)
        bid_vol_stronger_count = sum(
            1 for i in range(min(5, len(bid_vols), len(offer_vols)))
            if bid_vols[i] > offer_vols[i]
        )
        
        if bid_vol_stronger_count >= 3:  # At least 3 out of 5
            confidence_score += 20
            details['bid_vol_per_tick'] = f'TOP 5: {bid_vol_stronger_count}/5 levels bid > offer ✓'
        
        # Component 2: Check bid vol sum * 1.75 > offer vol sum (TOP 10 SUMMED)
        if bid_total > 0 and offer_total > 0:
            if bid_total * 1.75 > offer_total:
                confidence_score += 25
                details['bid_vol_strength'] = f'bid*1.75 > offer (ratio: {bid_total/offer_total:.2f}x) ✓'
        
        # Component 3: Check bid freq per tick > offer freq per tick (at least 3-4 out of top 5)
        bid_freq_stronger_count = sum(
            1 for i in range(min(5, len(bid_freqs), len(offer_freqs)))
            if bid_freqs[i] > offer_freqs[i]
        )
        
        if bid_freq_stronger_count >= 3:  # At least 3 out of 5
            confidence_score += 20
            details['bid_freq_per_tick'] = f'TOP 5: {bid_freq_stronger_count}/5 levels bid_freq > offer_freq ✓'
        
        # Component 4: Check bid freq sum * 1.75 > offer freq sum (TOP 10 SUMMED)
        if bid_freq_total > 0 and offer_freq_total > 0:
            if bid_freq_total * 1.75 > offer_freq_total:
                confidence_score += 25
                details['bid_freq_strength'] = f'bid_freq*1.75 > offer_freq (ratio: {bid_freq_total/offer_freq_total:.2f}x) ✓'
        
        # Component 5: HAKA > HAKI (buyers more aggressive than sellers in bearish - dump incoming)
        if haka_volume_recent and haki_volume_recent:
            if haka_volume_recent > haki_volume_recent:
                haka_ratio = haka_volume_recent / haki_volume_recent if haki_volume_recent > 0 else 0
                confidence_score += 15
                details['haka_dominance'] = f'HAKA > HAKI ({haka_ratio:.2f}x) ✓'
        elif haka_volume_recent and haka_volume_recent > self.thresholds['large_volume']:
            confidence_score += 10
            details['haka_activity'] = f'HIGH ({haka_volume_recent:,.0f}) ✓'
        
        # Component 6: Negative net flow (3-day trend shows selling pressure)
        if net_flow_3days and len(net_flow_3days) >= 2:
            negative_days = sum(1 for flow in net_flow_3days if flow < 0)
            if negative_days >= 2:  # At least 2 days negative
                confidence_score += 15
                details['net_flow'] = f'NEGATIVE ({negative_days}/{len(net_flow_3days)} days) ✓'
        
        return {
            'pattern': 'BEARISH_DISTRIBUTION',
            'confidence': min(confidence_score, 100),
            'details': details,
            'action': self._get_action_bearish(confidence_score),
            'description': 'Sellers dominating - strong bearish pressure detected'
        }
    
    # ===== UTILITY: Frequency analysis =====
    def analyze_frequency_dynamics(self, 
                                  bid_freqs: List[int], 
                                  offer_freqs: List[int]) -> Dict:
        """
        Track frequency shift over time
        
        Useful for detecting:
        - Bid persistence (accumulation phase)
        - Freq shift indicator (distribution phase)
        """
        
        bid_freq_recent = sum(bid_freqs[-3:]) if len(bid_freqs) >= 3 else sum(bid_freqs)
        offer_freq_recent = sum(offer_freqs[-3:]) if len(offer_freqs) >= 3 else sum(offer_freqs)
        
        # Trend comparison (last 3 vs before last 3)
        if len(bid_freqs) >= 6:
            bid_freq_trend = bid_freq_recent - sum(bid_freqs[-6:-3])
            offer_freq_trend = offer_freq_recent - sum(offer_freqs[-6:-3])
        else:
            bid_freq_trend = 0
            offer_freq_trend = 0
        
        return {
            'bid_freq_recent': bid_freq_recent,
            'offer_freq_recent': offer_freq_recent,
            'bid_freq_trend': 'INCREASING' if bid_freq_trend > 0 else 'DECREASING' if bid_freq_trend < 0 else 'STABLE',
            'offer_freq_trend': 'INCREASING' if offer_freq_trend > 0 else 'DECREASING' if offer_freq_trend < 0 else 'STABLE'
        }
    
    # ===== ENTRY LOGIC: STAGED BUYING =====
    def generate_staged_entries(self, 
                               confidence: float,
                               bid_vols: List[float],
                               bid_prices: List[float],
                               position_size: float = 100) -> List[Dict]:
        """
        Generate staged entry orders based on confidence level
        
        Entry logic:
        - Confidence 70-80: Entry 30% @ bid level 1
        - Confidence 80-90: Entry 40% @ bid level 2-3
        - Confidence 90+:   Entry 30% @ bid level 4-5
        """
        
        entries = []
        total_allocation = position_size
        
        if confidence < 70:
            return entries
        
        if confidence >= 70:
            # Stage 1: Bid level 1 (deepest, most aggressive)
            entry_size_1 = total_allocation * 0.30
            if len(bid_prices) > 0:
                entries.append({
                    'stage': 1,
                    'size': entry_size_1,
                    'price': bid_prices[0],
                    'volume_available': bid_vols[0] if len(bid_vols) > 0 else 0,
                    'description': 'Aggressive entry at deepest bid'
                })
        
        if confidence >= 80:
            # Stage 2: Bid level 2-3
            entry_size_2 = total_allocation * 0.40
            if len(bid_prices) >= 3:
                avg_price = (bid_prices[1] + bid_prices[2]) / 2
                avg_vol = (bid_vols[1] + bid_vols[2]) / 2 if len(bid_vols) >= 3 else 0
                entries.append({
                    'stage': 2,
                    'size': entry_size_2,
                    'price': avg_price,
                    'volume_available': avg_vol,
                    'description': 'Medium entry at bid level 2-3'
                })
        
        if confidence >= 90:
            # Stage 3: Bid level 4-5
            entry_size_3 = total_allocation * 0.30
            if len(bid_prices) >= 5:
                avg_price = (bid_prices[3] + bid_prices[4]) / 2
                avg_vol = (bid_vols[3] + bid_vols[4]) / 2 if len(bid_vols) >= 5 else 0
                entries.append({
                    'stage': 3,
                    'size': entry_size_3,
                    'price': avg_price,
                    'volume_available': avg_vol,
                    'description': 'Conservative entry at bid level 4-5'
                })
        
        return entries
    
    # ===== EXIT LOGIC: PROFIT TAKING & TRAILING STOP =====
    def generate_exit_strategy(self,
                              entry_price: float,
                              current_price: float,
                              atr: float,
                              position_size: float) -> Dict:
        """
        Generate exit strategy: profit targets + trailing stops
        
        Conservative approach:
        - First target: +0.5% profit (take 30%)
        - Second target: +1% profit (take 40%)
        - Third target: +1.5% profit (take 30%, use trailing stop)
        - Stop loss: Below support or -0.8% from entry
        """
        
        profit_pct = ((current_price - entry_price) / entry_price) * 100
        
        targets = [
            {
                'target_level': entry_price * 1.005,
                'target_pct': 0.5,
                'take_profit': position_size * 0.30,
                'description': 'First target - light profit taking'
            },
            {
                'target_level': entry_price * 1.01,
                'target_pct': 1.0,
                'take_profit': position_size * 0.40,
                'description': 'Second target - partial profit'
            },
            {
                'target_level': entry_price * 1.015,
                'target_pct': 1.5,
                'take_profit': position_size * 0.30,
                'description': 'Third target - remaining with trailing stop'
            }
        ]
        
        stop_loss = entry_price * 0.992  # -0.8%
        trailing_stop = current_price - (atr * 2)  # 2x ATR trailing
        
        return {
            'entry_price': entry_price,
            'current_price': current_price,
            'current_profit_pct': profit_pct,
            'targets': targets,
            'stop_loss': stop_loss,
            'trailing_stop': trailing_stop,
            'active_trailing_stop': max(stop_loss, trailing_stop)
        }
    
    # ===== HELPER METHODS =====
    def _get_action_bullish(self, confidence: float) -> str:
        """Determine action for bullish pattern"""
        if confidence >= 85:
            return 'BUY_STRONG'
        elif confidence >= 75:
            return 'BUY'
        elif confidence >= 60:
            return 'WATCH'
        else:
            return 'SKIP'
    
    def _get_action_bearish(self, confidence: float) -> str:
        """Determine action for bearish pattern"""
        if confidence >= 90:
            return 'IMMEDIATE_EXIT'
        elif confidence >= 80:
            return 'CLOSE_POSITION'
        elif confidence >= 60:
            return 'CAUTION'
        else:
            return 'MONITOR'


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    """
    Example: Analyzing HMSP screenshot data
    """
    
    indicator = IDXMomentumIndicator()
    
    # HMSP Order Book Data (from screenshot)
    bid_vols_hmsp = [515, 12836, 24618, 50627, 16426]
    bid_freqs_hmsp = [0, 63, 110, 138, 133]
    ask_vols_hmsp = [47079, 29127, 73236, 82845, 88305]
    ask_freqs_hmsp = [0, 202, 204, 377, 704]
    
    # Broker Action (from broker summary)
    net_flow_3days = [1.5, 1.2, 0.9]  # Positive money flows (in billions)
    haka_volume = 75000  # Large volume
    
    # Analyze bullish pattern
    print("=" * 80)
    print("HMSP - BULLISH ACCUMULATION ANALYSIS")
    print("=" * 80)
    
    result_bullish = indicator.detect_bullish_accumulation(
        bid_vols=bid_vols_hmsp,
        bid_freqs=bid_freqs_hmsp,
        offer_vols=ask_vols_hmsp,
        offer_freqs=ask_freqs_hmsp,
        haka_volume_recent=haka_volume,
        net_flow_3days=net_flow_3days
    )
    
    print(f"\nPattern: {result_bullish['pattern']}")
    print(f"Confidence: {result_bullish['confidence']}/100")
    print(f"Action: {result_bullish['action']}")
    print(f"\nDetails:")
    for key, value in result_bullish['details'].items():
        print(f"  {key}: {value}")
    
    # Generate staged entries
    print("\n" + "=" * 80)
    print("STAGED ENTRY STRATEGY")
    print("=" * 80)
    
    bid_prices_hmsp = [875, 870, 865, 860, 855]
    entries = indicator.generate_staged_entries(
        confidence=result_bullish['confidence'],
        bid_vols=bid_vols_hmsp,
        bid_prices=bid_prices_hmsp,
        position_size=100
    )
    
    for entry in entries:
        print(f"\nStage {entry['stage']}:")
        print(f"  Size: {entry['size']:.1f}% of position")
        print(f"  Price: Rp {entry['price']:.0f}")
        print(f"  Available Volume: {entry['volume_available']:,.0f} lots")
        print(f"  → {entry['description']}")
    
    # Example exit strategy
    print("\n" + "=" * 80)
    print("EXIT STRATEGY")
    print("=" * 80)
    
    entry_price = 872
    current_price = 880
    atr = 8  # Average True Range
    
    exit_strategy = indicator.generate_exit_strategy(
        entry_price=entry_price,
        current_price=current_price,
        atr=atr,
        position_size=100
    )
    
    print(f"\nEntry Price: Rp {exit_strategy['entry_price']:.0f}")
    print(f"Current Price: Rp {exit_strategy['current_price']:.0f}")
    print(f"Current Profit: {exit_strategy['current_profit_pct']:.2f}%")
    print(f"Stop Loss: Rp {exit_strategy['stop_loss']:.0f}")
    print(f"Trailing Stop: Rp {exit_strategy['trailing_stop']:.0f}")
    
    print(f"\nProfit Targets:")
    for target in exit_strategy['targets']:
        print(f"  {target['target_pct']:.1f}% → Rp {target['target_level']:.0f} | Take {target['take_profit']:.0f}%")
        print(f"      {target['description']}")
