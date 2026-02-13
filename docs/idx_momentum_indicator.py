"""
IDX Momentum Indicator - Trading Sentiment Analysis (6-Rule System)
Indonesian Stock Market Scalping Strategy

LOGIC: 6 Rules totaling 100 points
Target: confidence ≥ 80 points = BULLISH, else BEARISH

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
    Trading Sentiment Analysis Indicator (6-Rule System)
    
    Target: confidence ≥ 80 points = BULLISH, else BEARISH
    Total maksimal points: 100 points
    
    Rules:
    1. Top 10 Summed Bid Volume vs Offer Volume (15 points)
    2. Top Bid Volume vs Top Offer Volume (20 points)
    3. Distribusi Offer Volume - Kerapian Tick (30 points)
    4. Top 10 Summed Bid Freq vs Offer Freq (15 points)
    5. All Bid Volume vs All Offer Volume (10 points)
    6. All Bid Freq vs All Offer Freq (10 points)
    """
    
    def __init__(self, thresholds: Optional[Dict] = None):
        """Initialize indicator with configurable thresholds"""
        self.thresholds = thresholds or {
            'bullish_threshold': 80,  # Confidence needed for BULLISH signal
            'bearish_threshold': 20,  # Confidence needed for BEARISH signal (sellers dominate)
        }
        self.price_history = []
        self.broker_history = []
    
    # ===== TRADING SENTIMENT ANALYSIS - 6 RULE SYSTEM =====
    def analyze_sentiment(self,
                         bid_prices: List[float],
                         bid_volumes: List[float],
                         bid_freqs: List[int],
                         offer_prices: List[float],
                         offer_volumes: List[float],
                         offer_freqs: List[int]) -> Dict:
        """
        Trading Sentiment Analysis using 6 rules - Dual Direction
        
        This method calculates TWO scores:
        1. BULLISH SCORE: How much sellers are dominating (0-100)
           - Bullish if score >= 80
        2. BEARISH SCORE: How much buyers are dominating (0-100)
           - Bearish if score >= 80
        
        Sentiment Categories:
        - BULLISH: Bullish score >= 80 (sellers weak, buyers dominating)
        - BEARISH: Bearish score >= 80 (buyers weak, sellers dominating)
        - NEUTRAL: Both scores < 80 (balanced market)
        
        Args:
            bid_prices: List of bid prices (all levels)
            bid_volumes: List of bid volumes (all levels)
            bid_freqs: List of bid frequencies (all levels)
            offer_prices: List of offer prices (all levels)
            offer_volumes: List of offer volumes (all levels)
            offer_freqs: List of offer frequencies (all levels)
        
        Returns:
            Dict with confidence scores, sentiment, and rule details
        """
        
        bullish_confidence = 0
        bearish_confidence = 0
        bullish_rules = {}
        bearish_rules = {}
        
        # ===== BULLISH RULES (Sellers dominating) =====
        # RULE 1 BULLISH: Top 10 Summed Bid Volume vs Offer Volume (15 points)
        # Bullish if: bid*2 < offer (strictly less than)
        rule1_bullish_passed = False
        if len(bid_volumes) > 0 and len(offer_volumes) > 0:
            sum_bid_vol_top10 = sum(bid_volumes[:10])
            sum_offer_vol_top10 = sum(offer_volumes[:10])
            
            if (sum_bid_vol_top10 * 2) < sum_offer_vol_top10:
                bullish_confidence += 15
                rule1_bullish_passed = True
            
            bullish_rules['rule_1'] = {
                'name': 'Top 10 Summed Bid Volume vs Offer Volume',
                'passed': rule1_bullish_passed,
                'points': 15 if rule1_bullish_passed else 0,
                'condition': '(sum_bid_vol_top10 * 2) < sum_offer_vol_top10',
                'interpretation': 'Sellers massive (offers weak buyers)',
                'values': {
                    'sum_bid_vol_top10': sum_bid_vol_top10,
                    'sum_offer_vol_top10': sum_offer_vol_top10,
                    'calculation': f'{sum_bid_vol_top10} * 2 = {sum_bid_vol_top10 * 2} < {sum_offer_vol_top10}? {rule1_bullish_passed}'
                }
            }
        
        # RULE 2 BULLISH: Top Bid Volume vs Top Offer Volume (20 points)
        rule2_bullish_passed = False
        if len(bid_volumes) > 0 and len(offer_volumes) > 0:
            top_bid_vol = bid_volumes[0]
            top_offer_vol = offer_volumes[0]
            
            if (top_bid_vol * 1.8) < top_offer_vol:
                bullish_confidence += 20
                rule2_bullish_passed = True
            
            bullish_rules['rule_2'] = {
                'name': 'Top Bid Volume vs Top Offer Volume',
                'passed': rule2_bullish_passed,
                'points': 20 if rule2_bullish_passed else 0,
                'condition': '(top_bid_vol * 1.8) < top_offer_vol',
                'interpretation': 'Top seller massive vs top buyer',
                'values': {
                    'top_bid_vol': top_bid_vol,
                    'top_offer_vol': top_offer_vol,
                    'calculation': f'{top_bid_vol} * 1.8 = {top_bid_vol * 1.8} < {top_offer_vol}? {rule2_bullish_passed}'
                }
            }
        
        # RULE 3 BULLISH: Distribusi Offer Volume - Kerapian Tick (30 points)
        rule3_bullish_passed = False
        if len(offer_volumes) >= 10:
            top_offer = offer_volumes[0]
            threshold = top_offer * 0.8
            
            # Exclude offers > threshold
            remaining_offers = [v for v in offer_volumes[:10] if v <= threshold]
            
            if len(remaining_offers) > 0:
                average = sum(remaining_offers) / len(remaining_offers)
                count_above_avg = sum(1 for v in remaining_offers if v > average)
                percentage_above_avg = count_above_avg / len(remaining_offers)
                
                if percentage_above_avg >= 0.75:
                    bullish_confidence += 30
                    rule3_bullish_passed = True
                
                bullish_rules['rule_3'] = {
                    'name': 'Distribusi Offer Volume - Kerapian Tick',
                    'passed': rule3_bullish_passed,
                    'points': 30 if rule3_bullish_passed else 0,
                    'condition': '(count_above_avg / count(remaining_offers)) >= 0.75',
                    'interpretation': 'Seller supply consistent & strong',
                    'values': {
                        'top_offer': top_offer,
                        'threshold_80_percent': threshold,
                        'all_top_10_offers': offer_volumes[:10],
                        'remaining_after_exclude': remaining_offers,
                        'average': average,
                        'count_above_avg': count_above_avg,
                        'percentage_above_avg': percentage_above_avg,
                        'calculation': f'{count_above_avg}/{len(remaining_offers)} = {percentage_above_avg:.2%} >= 75%? {rule3_bullish_passed}'
                    }
                }
        elif len(offer_volumes) >= 5:
            # Fallback for when we have less than 10 offers - use available data
            top_offer = offer_volumes[0]
            threshold = top_offer * 0.8
            
            # Exclude offers > threshold
            remaining_offers = [v for v in offer_volumes if v <= threshold]
            
            if len(remaining_offers) > 0:
                average = sum(remaining_offers) / len(remaining_offers)
                count_above_avg = sum(1 for v in remaining_offers if v > average)
                percentage_above_avg = count_above_avg / len(remaining_offers)
                
                if percentage_above_avg >= 0.75:
                    bullish_confidence += 30
                    rule3_bullish_passed = True
                
                bullish_rules['rule_3'] = {
                    'name': 'Distribusi Offer Volume - Kerapian Tick',
                    'passed': rule3_bullish_passed,
                    'points': 30 if rule3_bullish_passed else 0,
                    'condition': '(count_above_avg / count(remaining_offers)) >= 0.75',
                    'interpretation': 'Seller supply consistent & strong',
                    'values': {
                        'top_offer': top_offer,
                        'threshold_80_percent': threshold,
                        'all_top_10_offers': offer_volumes[:10] if len(offer_volumes) >= 10 else offer_volumes,
                        'remaining_after_exclude': remaining_offers,
                        'average': average,
                        'count_above_avg': count_above_avg,
                        'percentage_above_avg': percentage_above_avg,
                        'calculation': f'{count_above_avg}/{len(remaining_offers)} = {percentage_above_avg:.2%} >= 75%? {rule3_bullish_passed}'
                    }
                }
        
        # RULE 4 BULLISH: Top 10 Summed Bid Freq vs Offer Freq (15 points)
        # Bullish if: bid*2 < offer (strictly less than)
        rule4_bullish_passed = False
        if len(bid_freqs) > 0 and len(offer_freqs) > 0:
            sum_bid_freq_top10 = sum(bid_freqs[:10])
            sum_offer_freq_top10 = sum(offer_freqs[:10])
            
            if (sum_bid_freq_top10 * 2) < sum_offer_freq_top10:
                bullish_confidence += 15
                rule4_bullish_passed = True
            
            bullish_rules['rule_4'] = {
                'name': 'Top 10 Summed Bid Freq vs Offer Freq',
                'passed': rule4_bullish_passed,
                'points': 15 if rule4_bullish_passed else 0,
                'condition': '(sum_bid_freq_top10 * 2) < sum_offer_freq_top10',
                'interpretation': 'Sellers hitting multiple times',
                'values': {
                    'sum_bid_freq_top10': sum_bid_freq_top10,
                    'sum_offer_freq_top10': sum_offer_freq_top10,
                    'calculation': f'{sum_bid_freq_top10} * 2 = {sum_bid_freq_top10 * 2} < {sum_offer_freq_top10}? {rule4_bullish_passed}'
                }
            }
        
        # RULE 5 BULLISH: All Bid Volume vs All Offer Volume (10 points)
        # Bullish if: bid*2 < offer (strictly less than)
        rule5_bullish_passed = False
        if len(bid_volumes) > 0 and len(offer_volumes) > 0:
            all_bid_vol = sum(bid_volumes)
            all_offer_vol = sum(offer_volumes)
            
            if (all_bid_vol * 2) < all_offer_vol:
                bullish_confidence += 10
                rule5_bullish_passed = True
            
            bullish_rules['rule_5'] = {
                'name': 'All Bid Volume vs All Offer Volume',
                'passed': rule5_bullish_passed,
                'points': 10 if rule5_bullish_passed else 0,
                'condition': '(all_bid_vol * 2) < all_offer_vol',
                'interpretation': 'Total sellers >> total buyers',
                'values': {
                    'all_bid_vol': all_bid_vol,
                    'all_offer_vol': all_offer_vol,
                    'calculation': f'{all_bid_vol} * 2 = {all_bid_vol * 2} < {all_offer_vol}? {rule5_bullish_passed}'
                }
            }
        
        # RULE 6 BULLISH: All Bid Freq vs All Offer Freq (10 points)
        # Bullish if: bid*2 < offer (strictly less than)
        rule6_bullish_passed = False
        if len(bid_freqs) > 0 and len(offer_freqs) > 0:
            all_bid_freq = sum(bid_freqs)
            all_offer_freq = sum(offer_freqs)
            
            if (all_bid_freq * 2) < all_offer_freq:
                bullish_confidence += 10
                rule6_bullish_passed = True
            
            bullish_rules['rule_6'] = {
                'name': 'All Bid Freq vs All Offer Freq',
                'passed': rule6_bullish_passed,
                'points': 10 if rule6_bullish_passed else 0,
                'condition': '(all_bid_freq * 2) < all_offer_freq',
                'interpretation': 'Sellers >> buyers in frequency',
                'values': {
                    'all_bid_freq': all_bid_freq,
                    'all_offer_freq': all_offer_freq,
                    'calculation': f'{all_bid_freq} * 2 = {all_bid_freq * 2} < {all_offer_freq}? {rule6_bullish_passed}'
                }
            }
        
        # ===== BEARISH RULES (Strong SELLER dominating) - offer much bigger =====
        # RULE 1 BEARISH: Top 10 Summed Offer Volume vs Bid Volume (15 points)
        # Bearish if: bid < offer*2 (strictly less than)
        rule1_bearish_passed = False
        if len(bid_volumes) > 0 and len(offer_volumes) > 0:
            sum_bid_vol_top10 = sum(bid_volumes[:10])
            sum_offer_vol_top10 = sum(offer_volumes[:10])
            
            if sum_bid_vol_top10 < (sum_offer_vol_top10 * 2):
                bearish_confidence += 15
                rule1_bearish_passed = True
            
            bearish_rules['rule_1'] = {
                'name': 'Top 10 Summed Offer Volume vs Bid Volume',
                'passed': rule1_bearish_passed,
                'points': 15 if rule1_bearish_passed else 0,
                'condition': '(sum_offer_vol_top10 * 2) < sum_bid_vol_top10',
                'interpretation': 'Buyers massive (bids weak sellers)',
                'values': {
                    'sum_bid_vol_top10': sum_bid_vol_top10,
                    'sum_offer_vol_top10': sum_offer_vol_top10,
                    'calculation': f'{sum_offer_vol_top10} * 2 = {sum_offer_vol_top10 * 2} < {sum_bid_vol_top10}? {rule1_bearish_passed}'
                }
            }
        
        # RULE 2 BEARISH: Top Offer Volume vs Top Bid Volume (20 points)
        rule2_bearish_passed = False
        if len(bid_volumes) > 0 and len(offer_volumes) > 0:
            top_bid_vol = bid_volumes[0]
            top_offer_vol = offer_volumes[0]
            
            if (top_offer_vol * 1.8) < top_bid_vol:
                bearish_confidence += 20
                rule2_bearish_passed = True
            
            bearish_rules['rule_2'] = {
                'name': 'Top Offer Volume vs Top Bid Volume',
                'passed': rule2_bearish_passed,
                'points': 20 if rule2_bearish_passed else 0,
                'condition': '(top_offer_vol * 1.8) < top_bid_vol',
                'interpretation': 'Top buyer massive vs top seller',
                'values': {
                    'top_bid_vol': top_bid_vol,
                    'top_offer_vol': top_offer_vol,
                    'calculation': f'{top_offer_vol} * 1.8 = {top_offer_vol * 1.8} < {top_bid_vol}? {rule2_bearish_passed}'
                }
            }
        
        # RULE 3 BEARISH: Distribusi Bid Volume - Kerapian Tick (30 points)
        rule3_bearish_passed = False
        if len(bid_volumes) >= 10:
            top_bid = bid_volumes[0]
            threshold = top_bid * 0.8
            
            # Exclude bids > threshold
            remaining_bids = [v for v in bid_volumes[:10] if v <= threshold]
            
            if len(remaining_bids) > 0:
                average = sum(remaining_bids) / len(remaining_bids)
                count_above_avg = sum(1 for v in remaining_bids if v > average)
                percentage_above_avg = count_above_avg / len(remaining_bids)
                
                if percentage_above_avg >= 0.75:
                    bearish_confidence += 30
                    rule3_bearish_passed = True
                
                bearish_rules['rule_3'] = {
                    'name': 'Distribusi Bid Volume - Kerapian Tick',
                    'passed': rule3_bearish_passed,
                    'points': 30 if rule3_bearish_passed else 0,
                    'condition': '(count_above_avg / count(remaining_bids)) >= 0.75',
                    'interpretation': 'Buyer demand consistent & strong',
                    'values': {
                        'top_bid': top_bid,
                        'threshold_80_percent': threshold,
                        'all_top_10_bids': bid_volumes[:10],
                        'remaining_after_exclude': remaining_bids,
                        'average': average,
                        'count_above_avg': count_above_avg,
                        'percentage_above_avg': percentage_above_avg,
                        'calculation': f'{count_above_avg}/{len(remaining_bids)} = {percentage_above_avg:.2%} >= 75%? {rule3_bearish_passed}'
                    }
                }
        elif len(bid_volumes) >= 5:
            # Fallback for when we have less than 10 bids - use available data
            top_bid = bid_volumes[0]
            threshold = top_bid * 0.8
            
            # Exclude bids > threshold
            remaining_bids = [v for v in bid_volumes if v <= threshold]
            
            if len(remaining_bids) > 0:
                average = sum(remaining_bids) / len(remaining_bids)
                count_above_avg = sum(1 for v in remaining_bids if v > average)
                percentage_above_avg = count_above_avg / len(remaining_bids)
                
                if percentage_above_avg >= 0.75:
                    bearish_confidence += 30
                    rule3_bearish_passed = True
                
                bearish_rules['rule_3'] = {
                    'name': 'Distribusi Bid Volume - Kerapian Tick',
                    'passed': rule3_bearish_passed,
                    'points': 30 if rule3_bearish_passed else 0,
                    'condition': '(count_above_avg / count(remaining_bids)) >= 0.75',
                    'interpretation': 'Buyer demand consistent & strong',
                    'values': {
                        'top_bid': top_bid,
                        'threshold_80_percent': threshold,
                        'all_top_10_bids': bid_volumes[:10] if len(bid_volumes) >= 10 else bid_volumes,
                        'remaining_after_exclude': remaining_bids,
                        'average': average,
                        'count_above_avg': count_above_avg,
                        'percentage_above_avg': percentage_above_avg,
                        'calculation': f'{count_above_avg}/{len(remaining_bids)} = {percentage_above_avg:.2%} >= 75%? {rule3_bearish_passed}'
                    }
                }
        
        # RULE 4 BEARISH: Top 10 Summed Offer Freq vs Bid Freq (15 points)
        # Bearish if: bid < offer*2 (strictly less than)
        rule4_bearish_passed = False
        if len(bid_freqs) > 0 and len(offer_freqs) > 0:
            sum_bid_freq_top10 = sum(bid_freqs[:10])
            sum_offer_freq_top10 = sum(offer_freqs[:10])
            
            if sum_bid_freq_top10 < (sum_offer_freq_top10 * 2):
                bearish_confidence += 15
                rule4_bearish_passed = True
            
            bearish_rules['rule_4'] = {
                'name': 'Top 10 Summed Offer Freq vs Bid Freq',
                'passed': rule4_bearish_passed,
                'points': 15 if rule4_bearish_passed else 0,
                'condition': '(sum_offer_freq_top10 * 2) < sum_bid_freq_top10',
                'interpretation': 'Buyers hitting multiple times',
                'values': {
                    'sum_bid_freq_top10': sum_bid_freq_top10,
                    'sum_offer_freq_top10': sum_offer_freq_top10,
                    'calculation': f'{sum_offer_freq_top10} * 2 = {sum_offer_freq_top10 * 2} < {sum_bid_freq_top10}? {rule4_bearish_passed}'
                }
            }
        
        # RULE 5 BEARISH: All Offer Volume vs All Bid Volume (10 points)
        # Bearish if: bid < offer*2 (strictly less than)
        rule5_bearish_passed = False
        if len(bid_volumes) > 0 and len(offer_volumes) > 0:
            all_bid_vol = sum(bid_volumes)
            all_offer_vol = sum(offer_volumes)
            
            if all_bid_vol < (all_offer_vol * 2):
                bearish_confidence += 10
                rule5_bearish_passed = True
            
            bearish_rules['rule_5'] = {
                'name': 'All Offer Volume vs All Bid Volume',
                'passed': rule5_bearish_passed,
                'points': 10 if rule5_bearish_passed else 0,
                'condition': '(all_offer_vol * 2) < all_bid_vol',
                'interpretation': 'Total buyers >> total sellers',
                'values': {
                    'all_bid_vol': all_bid_vol,
                    'all_offer_vol': all_offer_vol,
                    'calculation': f'{all_offer_vol} * 2 = {all_offer_vol * 2} < {all_bid_vol}? {rule5_bearish_passed}'
                }
            }
        
        # RULE 6 BEARISH: All Offer Freq vs All Bid Freq (10 points)
        # Bearish if: bid < offer*2 (strictly less than)
        rule6_bearish_passed = False
        if len(bid_freqs) > 0 and len(offer_freqs) > 0:
            all_bid_freq = sum(bid_freqs)
            all_offer_freq = sum(offer_freqs)
            
            if all_bid_freq < (all_offer_freq * 2):
                bearish_confidence += 10
                rule6_bearish_passed = True
            
            bearish_rules['rule_6'] = {
                'name': 'All Offer Freq vs All Bid Freq',
                'passed': rule6_bearish_passed,
                'points': 10 if rule6_bearish_passed else 0,
                'condition': '(all_offer_freq * 2) < all_bid_freq',
                'interpretation': 'Buyers >> sellers in frequency',
                'values': {
                    'all_bid_freq': all_bid_freq,
                    'all_offer_freq': all_offer_freq,
                    'calculation': f'{all_offer_freq} * 2 = {all_offer_freq * 2} < {all_bid_freq}? {rule6_bearish_passed}'
                }
            }
        
        # Determine sentiment - 3 categories: NEUTRAL, BULLISH, BEARISH
        if bullish_confidence >= self.thresholds['bullish_threshold']:
            sentiment = 'BULLISH'
            confidence = bullish_confidence
            signal_rules = bullish_rules
        elif bearish_confidence >= self.thresholds['bearish_threshold']:
            sentiment = 'BEARISH'
            confidence = bearish_confidence
            signal_rules = bearish_rules
        else:
            sentiment = 'NEUTRAL'
            confidence = max(bullish_confidence, bearish_confidence)
            signal_rules = bullish_rules if bullish_confidence >= bearish_confidence else bearish_rules
        
        # Signal emoji mapping
        signal_map = {
            'BULLISH': '🚀',
            'BEARISH': '⬇️',
            'NEUTRAL': '⚪'
        }
        
        return {
            'confidence': confidence,
            'bullish_confidence': bullish_confidence,
            'bearish_confidence': bearish_confidence,
            'sentiment': sentiment,
            'threshold': self.thresholds['bullish_threshold'],
            'rules': signal_rules,
            'all_rules': {
                'bullish': bullish_rules,
                'bearish': bearish_rules
            },
            'summary': {
                'total_points': confidence,
                'max_points': 100,
                'signal': f"{signal_map[sentiment]} {sentiment} (Confidence: {confidence}/100)"
            }
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
    
    # ===== FREQUENCY DYNAMICS ANALYSIS =====
    def analyze_frequency_dynamics(self,
                                   bid_freqs: List[int],
                                   offer_freqs: List[int]) -> Dict:
        """
        Analyze frequency dynamics to identify market phases
        
        Returns:
            Dict with frequency trends and dynamics analysis
        """
        
        if not bid_freqs or not offer_freqs:
            return {
                'bid_freq_recent': 0,
                'offer_freq_recent': 0,
                'bid_freq_trend': 'STABLE',
                'offer_freq_trend': 'STABLE',
                'phase': 'UNKNOWN'
            }
        
        # Get recent frequencies (first 3 levels)
        bid_freq_recent = sum(bid_freqs[:3]) if len(bid_freqs) >= 3 else sum(bid_freqs)
        offer_freq_recent = sum(offer_freqs[:3]) if len(offer_freqs) >= 3 else sum(offer_freqs)
        
        # Determine trends (based on available data)
        bid_freq_trend = 'STABLE'
        if len(bid_freqs) >= 2:
            if bid_freqs[0] > bid_freqs[-1]:
                bid_freq_trend = 'DECREASING'
            elif bid_freqs[0] < bid_freqs[-1]:
                bid_freq_trend = 'INCREASING'
        
        offer_freq_trend = 'STABLE'
        if len(offer_freqs) >= 2:
            if offer_freqs[0] > offer_freqs[-1]:
                offer_freq_trend = 'DECREASING'
            elif offer_freqs[0] < offer_freqs[-1]:
                offer_freq_trend = 'INCREASING'
        
        # Identify phase
        phase = 'CONSOLIDATION'
        if bid_freq_trend == 'INCREASING' and offer_freq_trend in ['STABLE', 'DECREASING']:
            phase = 'ACCUMULATION'
        elif offer_freq_trend == 'INCREASING' and bid_freq_trend in ['STABLE', 'DECREASING']:
            phase = 'DISTRIBUTION'
        
        return {
            'bid_freq_recent': bid_freq_recent,
            'offer_freq_recent': offer_freq_recent,
            'bid_freq_trend': bid_freq_trend,
            'offer_freq_trend': offer_freq_trend,
            'phase': phase,
            'bid_freqs': bid_freqs,
            'offer_freqs': offer_freqs
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


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    """
    Example: Testing the 6-Rule Trading Sentiment Analysis
    """
    
    indicator = IDXMomentumIndicator(thresholds={'bullish_threshold': 80})
    
    # Example 1: PASS scenario (all rules pass)
    print("=" * 80)
    print("EXAMPLE 1: ALL RULES PASS (Expected: BULLISH)")
    print("=" * 80)
    
    # Example 1: PASS scenario (optimized for all rules passing)
    # Rule 3 requires: 75% of remaining offers > average
    # Strategy: Create tight distribution around middle values
    bid_vols_pass = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55]
    bid_freqs_pass = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
    
    # Offer volumes: [top=10000] -> exclude >8000 -> [2800, 2700, 2600, 2500, 2400, 2300, 1000, 900]
    # Average = 2275, then 6/8 = 75% > average PASS!
    offer_vols_pass = [10000, 8200, 2800, 2700, 2600, 2500, 2400, 2300, 1000, 900]
    offer_freqs_pass = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55]
    
    bid_prices_pass = [1000, 999, 998, 997, 996, 995, 994, 993, 992, 991]
    offer_prices_pass = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
    
    result_pass = indicator.analyze_sentiment(
        bid_prices=bid_prices_pass,
        bid_volumes=bid_vols_pass,
        bid_freqs=bid_freqs_pass,
        offer_prices=offer_prices_pass,
        offer_volumes=offer_vols_pass,
        offer_freqs=offer_freqs_pass
    )
    
    print(f"\nResult: {result_pass['summary']['signal']}")
    print(f"Confidence: {result_pass['confidence']}/100")
    print(f"Sentiment: {result_pass['sentiment']}\n")
    
    for rule_key, rule_data in result_pass['rules'].items():
        status = "✓ PASS" if rule_data['passed'] else "✗ FAIL"
        print(f"{rule_key} - {rule_data['name']}: {status} ({rule_data['points']} points)")
        print(f"   Calculation: {rule_data['values']['calculation']}")
    
    # Example 2: FAIL scenario (all rules fail)
    print("\n" + "=" * 80)
    print("EXAMPLE 2: ALL RULES FAIL (Expected: BEARISH)")
    print("=" * 80)
    
    # Example 2: TRUE BEARISH scenario (strong selling pressure)
    # This scenario has STRONG bid compared to weak offer
    # In this 6-rule system: high bid volume = BEARISH signal
    bid_vols_fail = [300, 280, 260, 240, 220, 200, 180, 160, 140, 120]
    bid_freqs_fail = [40, 38, 36, 34, 32, 30, 28, 26, 24, 22]
    
    # Offer volumes: weak and scattered (not meeting Rule 3)
    offer_vols_fail = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55]
    offer_freqs_fail = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
    
    bid_prices_fail = [1000, 999, 998, 997, 996, 995, 994, 993, 992, 991]
    offer_prices_fail = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010]
    
    result_fail = indicator.analyze_sentiment(
        bid_prices=bid_prices_fail,
        bid_volumes=bid_vols_fail,
        bid_freqs=bid_freqs_fail,
        offer_prices=offer_prices_fail,
        offer_volumes=offer_vols_fail,
        offer_freqs=offer_freqs_fail
    )
    
    print(f"\nResult: {result_fail['summary']['signal']}")
    print(f"Confidence: {result_fail['confidence']}/100")
    print(f"Sentiment: {result_fail['sentiment']}\n")
    
    for rule_key, rule_data in result_fail['rules'].items():
        status = "✓ PASS" if rule_data['passed'] else "✗ FAIL"
        print(f"{rule_key} - {rule_data['name']}: {status} ({rule_data['points']} points)")
        print(f"   Calculation: {rule_data['values']['calculation']}")
