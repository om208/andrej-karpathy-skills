#!/usr/bin/env python3
"""
ADVANCED FVG PATTERN ANALYZER
Analyzes FVG patterns with body size, tail size, and volume metrics
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from pathlib import Path
from datetime import datetime

print("\n" + "="*80)
print("ADVANCED FVG PATTERN ANALYZER")
print("Body Size, Tail Size, Volume Analysis")
print("="*80)

# ============================================================================
# PATTERN ANALYZER
# ============================================================================

class AdvancedPatternAnalyzer:
    """Analyzes candle patterns with detailed metrics"""

    @staticmethod
    def calculate_candle_metrics(candle: Dict) -> Dict:
        """
        Calculate detailed candle metrics:
        - Body size (open-close)
        - Upper tail (high - max(open,close))
        - Lower tail (min(open,close) - low)
        - Body ratio (body / total range)
        - Tail ratio
        """

        open_price = candle['open']
        close_price = candle['close']
        high_price = candle['high']
        low_price = candle['low']
        volume = candle.get('volume', 0)

        # Body calculation
        body = abs(close_price - open_price)
        is_bullish = close_price > open_price

        # Tails
        upper_tail = high_price - max(open_price, close_price)
        lower_tail = min(open_price, close_price) - low_price

        # Range
        total_range = high_price - low_price

        # Ratios
        body_ratio = body / total_range if total_range > 0 else 0
        upper_tail_ratio = upper_tail / total_range if total_range > 0 else 0
        lower_tail_ratio = lower_tail / total_range if total_range > 0 else 0

        # Is doji
        is_doji = body < (total_range * 0.1)

        # Is long upper tail
        is_long_upper_tail = upper_tail > (body * 2)

        # Is long lower tail
        is_long_lower_tail = lower_tail > (body * 2)

        return {
            'body': body,
            'upper_tail': upper_tail,
            'lower_tail': lower_tail,
            'total_range': total_range,
            'body_ratio': body_ratio,
            'upper_tail_ratio': upper_tail_ratio,
            'lower_tail_ratio': lower_tail_ratio,
            'is_bullish': is_bullish,
            'is_doji': is_doji,
            'is_long_upper_tail': is_long_upper_tail,
            'is_long_lower_tail': is_long_lower_tail,
            'volume': volume
        }

    @staticmethod
    def classify_fvg_pattern(candle1_metrics: Dict, candle2_metrics: Dict,
                            candle3_metrics: Dict) -> Dict:
        """
        Classify FVG pattern based on candle characteristics
        """

        classification = {
            'pattern_type': '',
            'strength': 0,  # 1-10 scale
            'quality_factors': [],
            'risk_factors': []
        }

        # Analyze middle candle
        middle_body_ratio = candle2_metrics['body_ratio']
        middle_is_bullish = candle2_metrics['is_bullish']

        # Analyze outer candles
        candle1_body_ratio = candle1_metrics['body_ratio']
        candle3_body_ratio = candle3_metrics['body_ratio']

        # Pattern classification

        # 1. IDEAL DOJI FVG
        if (candle1_metrics['is_doji'] or candle3_metrics['is_doji']) and \
           candle1_body_ratio < 0.3 and candle3_body_ratio < 0.3:
            classification['pattern_type'] = 'IDEAL_DOJI_FVG'
            classification['strength'] = 9
            classification['quality_factors'].append('Doji on outer candle')
            classification['quality_factors'].append('Small body outer candles')

        # 2. STRONG FVG
        elif middle_body_ratio > 0.7 and \
             candle1_body_ratio < 0.3 and candle3_body_ratio < 0.3:
            classification['pattern_type'] = 'STRONG_FVG'
            classification['strength'] = 8
            classification['quality_factors'].append('Strong middle candle body')
            classification['quality_factors'].append('Very small outer bodies')

        # 3. STANDARD FVG
        elif middle_body_ratio > 0.5 and \
             candle1_body_ratio < 0.45 and candle3_body_ratio < 0.45:
            classification['pattern_type'] = 'STANDARD_FVG'
            classification['strength'] = 6
            classification['quality_factors'].append('Good middle candle')

        # 4. WEAK FVG
        else:
            classification['pattern_type'] = 'WEAK_FVG'
            classification['strength'] = 3

        # Risk factors
        if candle1_metrics['is_long_upper_tail'] or candle3_metrics['is_long_upper_tail']:
            classification['risk_factors'].append('Long upper tail on outer candle')

        if candle1_metrics['is_long_lower_tail'] or candle3_metrics['is_long_lower_tail']:
            classification['risk_factors'].append('Long lower tail on outer candle')

        if candle2_metrics['body_ratio'] < 0.4:
            classification['risk_factors'].append('Weak middle candle body')

        return classification

    @staticmethod
    def analyze_volume_confirmation(candle1: Dict, candle2: Dict,
                                   candle3: Dict, avg_volume: float) -> Dict:
        """
        Analyze volume confirmation of FVG pattern
        """

        volume_analysis = {
            'middle_volume_ratio': candle2.get('volume', 0) / avg_volume if avg_volume > 0 else 0,
            'outer_volume_avg': (candle1.get('volume', 0) + candle3.get('volume', 0)) / 2,
            'has_volume_spike': False,
            'volume_strength': ''
        }

        # Analyze volume
        if volume_analysis['middle_volume_ratio'] > 1.5:
            volume_analysis['has_volume_spike'] = True
            volume_analysis['volume_strength'] = 'STRONG'
        elif volume_analysis['middle_volume_ratio'] > 1.0:
            volume_analysis['volume_strength'] = 'NORMAL'
        else:
            volume_analysis['volume_strength'] = 'WEAK'

        return volume_analysis

# ============================================================================
# COMPREHENSIVE PATTERN REPORT GENERATOR
# ============================================================================

class ComprehensiveReportGenerator:
    """Generates detailed pattern analysis reports"""

    @staticmethod
    def create_enhanced_fvg_report(df: pd.DataFrame, fvgs: List[Dict],
                                  interval: str) -> pd.DataFrame:
        """
        Create enhanced FVG report with pattern classification
        """

        report_data = []
        avg_volume = df['volume'].mean()

        for fvg in fvgs:
            fvg_index = fvg['index']

            # Get the three candles
            candle1 = df.iloc[fvg_index - 1]
            candle2 = df.iloc[fvg_index]
            candle3 = df.iloc[fvg_index + 1]

            # Calculate metrics
            metrics1 = AdvancedPatternAnalyzer.calculate_candle_metrics({
                'open': candle1['open'],
                'close': candle1['close'],
                'high': candle1['high'],
                'low': candle1['low'],
                'volume': candle1['volume']
            })

            metrics2 = AdvancedPatternAnalyzer.calculate_candle_metrics({
                'open': candle2['open'],
                'close': candle2['close'],
                'high': candle2['high'],
                'low': candle2['low'],
                'volume': candle2['volume']
            })

            metrics3 = AdvancedPatternAnalyzer.calculate_candle_metrics({
                'open': candle3['open'],
                'close': candle3['close'],
                'high': candle3['high'],
                'low': candle3['low'],
                'volume': candle3['volume']
            })

            # Classify pattern
            classification = AdvancedPatternAnalyzer.classify_fvg_pattern(
                metrics1, metrics2, metrics3
            )

            # Analyze volume
            volume_analysis = AdvancedPatternAnalyzer.analyze_volume_confirmation(
                {'volume': candle1['volume']},
                {'volume': candle2['volume']},
                {'volume': candle3['volume']},
                avg_volume
            )

            # Create report row
            report_row = {
                # Timestamps
                'timestamp': fvg['timestamp'],
                'candle1_time': fvg['candle1_timestamp'],
                'candle3_time': fvg['candle3_timestamp'],

                # Pattern Type
                'pattern_type': classification['pattern_type'],
                'pattern_strength': classification['strength'],
                'has_quality_factors': len(classification['quality_factors']) > 0,
                'quality_factors': '|'.join(classification['quality_factors']),
                'has_risk_factors': len(classification['risk_factors']) > 0,
                'risk_factors': '|'.join(classification['risk_factors']),

                # Middle Point (FVG location)
                'middle_point': fvg['middle_point'],
                'middle_high': fvg['middle_high'],
                'middle_low': fvg['middle_low'],

                # Candle 1 Metrics
                'c1_body': metrics1['body'],
                'c1_body_ratio': metrics1['body_ratio'],
                'c1_upper_tail': metrics1['upper_tail'],
                'c1_lower_tail': metrics1['lower_tail'],
                'c1_is_doji': metrics1['is_doji'],
                'c1_is_bullish': metrics1['is_bullish'],

                # Candle 2 (Middle) Metrics
                'c2_body': metrics2['body'],
                'c2_body_ratio': metrics2['body_ratio'],
                'c2_upper_tail': metrics2['upper_tail'],
                'c2_lower_tail': metrics2['lower_tail'],
                'c2_is_doji': metrics2['is_doji'],
                'c2_is_bullish': metrics2['is_bullish'],

                # Candle 3 Metrics
                'c3_body': metrics3['body'],
                'c3_body_ratio': metrics3['body_ratio'],
                'c3_upper_tail': metrics3['upper_tail'],
                'c3_lower_tail': metrics3['lower_tail'],
                'c3_is_doji': metrics3['is_doji'],
                'c3_is_bullish': metrics3['is_bullish'],

                # Volume Analysis
                'middle_volume_ratio': volume_analysis['middle_volume_ratio'],
                'has_volume_spike': volume_analysis['has_volume_spike'],
                'volume_strength': volume_analysis['volume_strength'],

                # Post-FVG Movement (if available from earlier analysis)
                'max_upside': fvg.get('max_upside', 0),
                'max_downside': fvg.get('max_downside', 0),
                'candles_to_return': fvg.get('candles_to_return', 0)
            }

            report_data.append(report_row)

        return pd.DataFrame(report_data)

    @staticmethod
    def generate_pattern_statistics(report_df: pd.DataFrame, interval: str) -> Dict:
        """
        Generate statistics about pattern distribution
        """

        stats = {
            'interval': interval,
            'total_fvgs': len(report_df),
            'pattern_distribution': {},
            'quality_metrics': {
                'fvgs_with_quality_factors': 0,
                'fvgs_with_risk_factors': 0
            },
            'volume_metrics': {
                'fvgs_with_volume_spike': 0,
                'avg_middle_volume_ratio': 0
            },
            'movement_metrics': {
                'avg_upside_move': 0,
                'avg_downside_move': 0,
                'avg_candles_to_return': 0
            }
        }

        # Pattern distribution
        pattern_counts = report_df['pattern_type'].value_counts().to_dict()
        stats['pattern_distribution'] = pattern_counts

        # Quality metrics
        stats['quality_metrics']['fvgs_with_quality_factors'] = \
            report_df['has_quality_factors'].sum()
        stats['quality_metrics']['fvgs_with_risk_factors'] = \
            report_df['has_risk_factors'].sum()

        # Volume metrics
        stats['volume_metrics']['fvgs_with_volume_spike'] = \
            report_df['has_volume_spike'].sum()
        stats['volume_metrics']['avg_middle_volume_ratio'] = \
            report_df['middle_volume_ratio'].mean()

        # Movement metrics
        stats['movement_metrics']['avg_upside_move'] = \
            report_df['max_upside'].mean() if 'max_upside' in report_df.columns else 0
        stats['movement_metrics']['avg_downside_move'] = \
            report_df['max_downside'].mean() if 'max_downside' in report_df.columns else 0
        stats['movement_metrics']['avg_candles_to_return'] = \
            report_df['candles_to_return'].mean() if 'candles_to_return' in report_df.columns else 0

        return stats

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("ADVANCED PATTERN ANALYZER - READY")
print("="*80)
print("""
This module provides:

✅ Candle Metrics Analysis:
   - Body size and ratios
   - Upper/lower tail analysis
   - Doji detection
   - Long tail identification

✅ FVG Pattern Classification:
   - IDEAL_DOJI_FVG (strength 9)
   - STRONG_FVG (strength 8)
   - STANDARD_FVG (strength 6)
   - WEAK_FVG (strength 3)

✅ Pattern Quality Assessment:
   - Quality factors identification
   - Risk factors detection

✅ Volume Analysis:
   - Volume spike detection
   - Volume strength classification
   - Middle candle volume ratio

✅ Comprehensive Reporting:
   - Pattern distribution statistics
   - Quality metrics analysis
   - Volume metrics summary
   - Movement metrics aggregation

Usage:
    from fvg_pattern_analyzer import ComprehensiveReportGenerator
    report_df = ComprehensiveReportGenerator.create_enhanced_fvg_report(df, fvgs, interval)
    stats = ComprehensiveReportGenerator.generate_pattern_statistics(report_df, interval)
""")

print("\nModule ready for integration with FVG detection system!")
