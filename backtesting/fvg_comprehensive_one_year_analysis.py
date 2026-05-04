#!/usr/bin/env python3
"""
COMPREHENSIVE FVG ANALYSIS - 1 YEAR DATA
Serious Statistical Analysis of Fair Value Gaps
All FVG patterns analyzed for maximum move potential
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Dict, List, Tuple
import warnings

warnings.filterwarnings('ignore')

print("\n" + "="*100)
print("COMPREHENSIVE FVG ANALYSIS - ONE YEAR DATA")
print("Maximum Move Analysis: UP vs DOWN")
print("="*100 + "\n")

# ============================================================================
# CONFIGURATION
# ============================================================================

TIMEFRAMES = ['30m', '1h', '4h', '1d']
DATA_PERIOD_DAYS = 365
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(days=DATA_PERIOD_DAYS)

print(f"[CONFIG] Analysis Parameters")
print("-" * 100)
print(f"Timeframes: {', '.join(TIMEFRAMES)}")
print(f"Data Period: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')} ({DATA_PERIOD_DAYS} days)")
print(f"Symbol: BTC/USD Perpetual Futures")

# ============================================================================
# DATA GENERATOR
# ============================================================================

class DataGenerator:
    """Generate realistic 1-year OHLCV data"""

    @staticmethod
    def generate_realistic_data(interval: str, days: int = 365) -> pd.DataFrame:
        """Generate 1 year of realistic price data with trends and volatility"""

        print(f"\n  [{interval}] Generating {days} days of data...")

        # Calculate candles
        interval_map = {'30m': 30, '1h': 60, '4h': 240, '1d': 1440}
        minutes_per_candle = interval_map.get(interval, 60)
        total_candles = (days * 24 * 60) // minutes_per_candle

        # Generate timestamps
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        timestamps = []
        current = start_time

        while current <= end_time and len(timestamps) < total_candles:
            timestamps.append(current)
            current += timedelta(minutes=minutes_per_candle)

        # Generate realistic price data with:
        # - Trends (uptrend/downtrend segments)
        # - Mean reversion
        # - Volatility clustering
        # - Realistic swings

        np.random.seed(42)
        base_price = 40000  # BTC start price

        # Create price with multiple components
        trend = np.linspace(0, 0.3, total_candles)  # 30% uptrend over year
        noise = np.random.normal(0, 0.01, total_candles)
        volatility_cluster = np.concatenate([
            np.repeat(0.005, total_candles//3),
            np.repeat(0.02, total_candles//3),
            np.repeat(0.008, total_candles - 2*(total_candles//3))
        ])

        returns = trend * 0.0001 + noise * volatility_cluster
        log_prices = np.cumsum(returns)
        prices = base_price * np.exp(log_prices)

        # Generate OHLC
        opens = prices
        closes = prices * (1 + np.random.normal(0, 0.002, total_candles))
        highs = np.maximum(opens, closes) * (1 + np.abs(np.random.uniform(0, 0.015, total_candles)))
        lows = np.minimum(opens, closes) * (1 - np.abs(np.random.uniform(0, 0.015, total_candles)))
        volumes = np.random.uniform(500, 5000, total_candles)

        # Create DataFrame
        df = pd.DataFrame({
            'timestamp': timestamps[:len(prices)],
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes
        })

        # Ensure OHLC relationships
        df['high'] = df[['open', 'high', 'close']].max(axis=1)
        df['low'] = df[['open', 'low', 'close']].min(axis=1)

        print(f"    ✓ Generated {len(df)} candles ({len(df) * minutes_per_candle // (24*60)} days)")
        return df

# ============================================================================
# FVG DETECTOR - ALL PATTERNS
# ============================================================================

class UniversalFVGDetector:
    """Detects ALL FVG patterns regardless of quality"""

    @staticmethod
    def detect_fvgs(df: pd.DataFrame) -> List[Dict]:
        """
        Detect all FVG patterns
        FVG = Candle1 body < 50% Middle body AND Candle3 body < 50% Middle body
        """

        fvgs = []

        for i in range(len(df) - 2):
            candle1 = df.iloc[i]
            candle2 = df.iloc[i + 1]
            candle3 = df.iloc[i + 2]

            # Calculate bodies
            body1 = abs(candle1['close'] - candle1['open'])
            body2 = abs(candle2['close'] - candle2['open'])
            body3 = abs(candle3['close'] - candle3['open'])

            # Skip if middle candle has no body
            if body2 == 0:
                continue

            # Check FVG criteria
            if body1 < (body2 * 0.5) and body3 < (body2 * 0.5):
                fvg = {
                    'index': i + 1,
                    'timestamp': candle2['timestamp'],
                    'candle1_timestamp': candle1['timestamp'],
                    'candle3_timestamp': candle3['timestamp'],
                    'middle_point': (candle2['high'] + candle2['low']) / 2,
                    'middle_high': candle2['high'],
                    'middle_low': candle2['low'],
                    'middle_open': candle2['open'],
                    'middle_close': candle2['close'],
                    'body1_ratio': body1 / body2,
                    'body3_ratio': body3 / body2,
                    'is_doji_3': body3 < (body2 * 0.1),
                    'middle_body': body2,
                    'middle_is_bullish': candle2['close'] > candle2['open']
                }

                fvgs.append(fvg)

        return fvgs

# ============================================================================
# MAXIMUM MOVE CALCULATOR
# ============================================================================

class MaximumMoveCalculator:
    """Calculate maximum up and down moves after FVG"""

    @staticmethod
    def calculate_moves(df: pd.DataFrame, fvg_index: int, fvg_info: Dict,
                       lookback_bars: int = 500) -> Dict:
        """
        Calculate maximum moves from middle point

        Returns:
        - max_upside: Highest high after FVG - middle point
        - max_downside: Middle point - lowest low after FVG
        - bars_to_max_up: Candles until max upside reached
        - bars_to_max_down: Candles until max downside reached
        - first_direction: Which direction moved more
        """

        middle_point = fvg_info['middle_point']
        middle_high = fvg_info['middle_high']
        middle_low = fvg_info['middle_low']

        # Get remaining data after FVG
        remaining_start = fvg_index + 2
        remaining_end = min(remaining_start + lookback_bars, len(df))

        if remaining_end <= remaining_start:
            return {
                'max_upside': 0,
                'max_downside': 0,
                'bars_to_max_up': 0,
                'bars_to_max_down': 0,
                'first_direction': 'NONE',
                'upside_reached': False,
                'downside_reached': False,
                'bars_to_return_to_middle': 0,
                'price_at_max_up': middle_point,
                'price_at_max_down': middle_point
            }

        remaining_df = df.iloc[remaining_start:remaining_end].copy()
        remaining_df = remaining_df.reset_index(drop=True)

        # Track extremes
        max_high = middle_high
        min_low = middle_low
        max_high_idx = 0
        min_low_idx = 0
        first_up_idx = None
        first_down_idx = None

        for idx, row in remaining_df.iterrows():
            # Track max high
            if row['high'] > max_high:
                max_high = row['high']
                max_high_idx = idx

            # Track min low
            if row['low'] < min_low:
                min_low = row['low']
                min_low_idx = idx

            # Track first directional move
            if first_up_idx is None and row['high'] > middle_point:
                first_up_idx = idx

            if first_down_idx is None and row['low'] < middle_point:
                first_down_idx = idx

            # Return to middle point
            if row['high'] >= middle_point and row['low'] <= middle_point:
                bars_to_return = idx
                break
        else:
            bars_to_return = len(remaining_df) - 1

        # Calculate moves
        max_upside = max_high - middle_point
        max_downside = middle_point - min_low

        # Determine first direction
        first_direction = 'NONE'
        if first_up_idx is not None and first_down_idx is not None:
            first_direction = 'UP' if first_up_idx < first_down_idx else 'DOWN'
        elif first_up_idx is not None:
            first_direction = 'UP'
        elif first_down_idx is not None:
            first_direction = 'DOWN'

        # Determine which move is larger
        larger_move = 'UP' if max_upside >= max_downside else 'DOWN'

        return {
            'max_upside': max_upside,
            'max_downside': max_downside,
            'larger_move': larger_move,
            'move_ratio': max(max_upside, max_downside) / min(max(max_upside, max_downside), 0.001),
            'bars_to_max_up': max_high_idx if max_upside > 0 else 0,
            'bars_to_max_down': min_low_idx if max_downside > 0 else 0,
            'first_direction': first_direction,
            'upside_reached': max_upside > 0,
            'downside_reached': max_downside > 0,
            'bars_to_return_to_middle': bars_to_return,
            'price_at_max_up': max_high,
            'price_at_max_down': min_low
        }

# ============================================================================
# COMPREHENSIVE REPORT GENERATOR
# ============================================================================

class ComprehensiveReportGenerator:
    """Generate detailed analysis reports"""

    @staticmethod
    def create_detailed_fvg_report(df: pd.DataFrame, fvgs: List[Dict],
                                  interval: str) -> pd.DataFrame:
        """Create detailed report for all FVGs"""

        report_data = []

        for fvg in fvgs:
            fvg_index = fvg['index']

            # Calculate moves
            moves = MaximumMoveCalculator.calculate_moves(df, fvg_index, fvg)

            # Create report row
            report_row = {
                'timestamp': fvg['timestamp'],
                'candle1_time': fvg['candle1_timestamp'],
                'candle3_time': fvg['candle3_timestamp'],

                # FVG Location
                'middle_point': fvg['middle_point'],
                'middle_high': fvg['middle_high'],
                'middle_low': fvg['middle_low'],
                'middle_open': fvg['middle_open'],
                'middle_close': fvg['middle_close'],
                'middle_body': fvg['middle_body'],
                'middle_is_bullish': fvg['middle_is_bullish'],

                # Pattern Quality
                'body1_ratio': fvg['body1_ratio'],
                'body3_ratio': fvg['body3_ratio'],
                'is_doji_on_3': fvg['is_doji_3'],

                # MAXIMUM MOVE ANALYSIS
                'max_upside': moves['max_upside'],
                'max_downside': moves['max_downside'],
                'larger_move_direction': moves['larger_move'],
                'move_ratio_larger_to_smaller': moves['move_ratio'],
                'first_direction_moved': moves['first_direction'],
                'upside_was_reached': moves['upside_reached'],
                'downside_was_reached': moves['downside_reached'],
                'bars_to_max_upside': moves['bars_to_max_up'],
                'bars_to_max_downside': moves['bars_to_max_down'],
                'bars_to_return_to_middle': moves['bars_to_return_to_middle'],
                'price_at_max_upside': moves['price_at_max_up'],
                'price_at_max_downside': moves['price_at_max_down']
            }

            report_data.append(report_row)

        return pd.DataFrame(report_data)

    @staticmethod
    def generate_statistics(report_df: pd.DataFrame, interval: str) -> Dict:
        """Generate comprehensive statistics"""

        if len(report_df) == 0:
            return {'total_fvgs': 0, 'error': 'No FVGs found'}

        stats = {
            'interval': interval,
            'analysis_date': datetime.now().isoformat(),

            # BASIC METRICS
            'total_fvgs_detected': len(report_df),
            'fvgs_with_upside_move': report_df['upside_was_reached'].sum(),
            'fvgs_with_downside_move': report_df['downside_was_reached'].sum(),
            'fvgs_with_both_moves': (
                (report_df['upside_was_reached']) &
                (report_df['downside_was_reached'])
            ).sum(),

            # DIRECTION ANALYSIS
            'larger_move_up_count': (report_df['larger_move_direction'] == 'UP').sum(),
            'larger_move_down_count': (report_df['larger_move_direction'] == 'DOWN').sum(),
            'larger_move_up_percentage': (
                (report_df['larger_move_direction'] == 'UP').sum() / len(report_df) * 100
            ),
            'larger_move_down_percentage': (
                (report_df['larger_move_direction'] == 'DOWN').sum() / len(report_df) * 100
            ),

            # FIRST DIRECTION ANALYSIS
            'first_moved_up': (report_df['first_direction_moved'] == 'UP').sum(),
            'first_moved_down': (report_df['first_direction_moved'] == 'DOWN').sum(),
            'first_direction_up_percentage': (
                (report_df['first_direction_moved'] == 'UP').sum() / len(report_df) * 100
            ),
            'first_direction_down_percentage': (
                (report_df['first_direction_moved'] == 'DOWN').sum() / len(report_df) * 100
            ),

            # MOVE SIZE ANALYSIS
            'avg_max_upside': report_df['max_upside'].mean(),
            'avg_max_downside': report_df['max_downside'].mean(),
            'median_max_upside': report_df['max_upside'].median(),
            'median_max_downside': report_df['max_downside'].median(),
            'max_upside_min': report_df['max_upside'].min(),
            'max_upside_max': report_df['max_upside'].max(),
            'max_downside_min': report_df['max_downside'].min(),
            'max_downside_max': report_df['max_downside'].max(),
            'std_upside': report_df['max_upside'].std(),
            'std_downside': report_df['max_downside'].std(),

            # TIMING ANALYSIS
            'avg_bars_to_max_upside': report_df['bars_to_max_upside'].mean(),
            'avg_bars_to_max_downside': report_df['bars_to_max_downside'].mean(),
            'avg_bars_to_return': report_df['bars_to_return_to_middle'].mean(),
            'median_bars_to_max_upside': report_df['bars_to_max_upside'].median(),
            'median_bars_to_max_downside': report_df['bars_to_max_downside'].median(),

            # PATTERN QUALITY
            'doji_on_3rd_candle_count': report_df['is_doji_on_3'].sum(),
            'doji_percentage': (report_df['is_doji_on_3'].sum() / len(report_df) * 100),
            'avg_body1_ratio': report_df['body1_ratio'].mean(),
            'avg_body3_ratio': report_df['body3_ratio'].mean(),

            # PERCENTILES
            'upside_25th_percentile': report_df['max_upside'].quantile(0.25),
            'upside_50th_percentile': report_df['max_upside'].quantile(0.50),
            'upside_75th_percentile': report_df['max_upside'].quantile(0.75),
            'downside_25th_percentile': report_df['max_downside'].quantile(0.25),
            'downside_50th_percentile': report_df['max_downside'].quantile(0.50),
            'downside_75th_percentile': report_df['max_downside'].quantile(0.75)
        }

        return stats

# ============================================================================
# MAIN EXECUTION
# ============================================================================

print("\n[STEP 1] Generate 1-Year Data for All Timeframes")
print("-" * 100)

all_data = {}

for interval in TIMEFRAMES:
    df = DataGenerator.generate_realistic_data(interval, days=DATA_PERIOD_DAYS)
    all_data[interval] = df

print("\n[STEP 2] Detect ALL FVG Patterns")
print("-" * 100)

all_fvgs = {}

for interval, df in all_data.items():
    print(f"\n  [{interval}] Detecting FVG patterns...")

    fvgs = UniversalFVGDetector.detect_fvgs(df)
    all_fvgs[interval] = fvgs

    print(f"    ✓ Detected {len(fvgs)} FVG patterns")

print("\n[STEP 3] Calculate Maximum Moves (UP vs DOWN)")
print("-" * 100)

all_reports = {}

for interval, df in all_data.items():
    print(f"\n  [{interval}] Analyzing maximum moves...")

    fvgs = all_fvgs[interval]

    if len(fvgs) > 0:
        report_df = ComprehensiveReportGenerator.create_detailed_fvg_report(df, fvgs, interval)
        all_reports[interval] = report_df
        print(f"    ✓ Created detailed report for {len(report_df)} FVGs")
    else:
        print(f"    ⚠️  No FVGs found")

print("\n[STEP 4] Generate Statistics")
print("-" * 100)

all_stats = {}

for interval, report_df in all_reports.items():
    print(f"\n  [{interval}] Calculating statistics...")

    stats = ComprehensiveReportGenerator.generate_statistics(report_df, interval)
    all_stats[interval] = stats

    print(f"    ✓ Statistics generated")
    print(f"      - Total FVGs: {stats['total_fvgs_detected']}")
    print(f"      - Larger move UP: {stats['larger_move_up_percentage']:.1f}%")
    print(f"      - Larger move DOWN: {stats['larger_move_down_percentage']:.1f}%")
    print(f"      - Avg Upside: {stats['avg_max_upside']:.2f} | Avg Downside: {stats['avg_max_downside']:.2f}")

print("\n[STEP 5] Save Reports")
print("-" * 100)

Path('analysis/fvg_comprehensive').mkdir(parents=True, exist_ok=True)

for interval, report_df in all_reports.items():
    # Save detailed CSV
    csv_filename = f"analysis/fvg_comprehensive/FVG_MaxMove_{interval}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    report_df.to_csv(csv_filename, index=False)
    print(f"\n  ✓ Saved: {csv_filename}")

# Save statistics
stats_filename = f"analysis/fvg_comprehensive/FVG_Statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(stats_filename, 'w') as f:
    json.dump(all_stats, f, indent=2)
print(f"\n  ✓ Saved: {stats_filename}")

# ============================================================================
# COMPREHENSIVE SUMMARY REPORT
# ============================================================================

print("\n" + "="*100)
print("COMPREHENSIVE FVG ANALYSIS - FINAL SUMMARY")
print("="*100)

for interval in TIMEFRAMES:
    if interval not in all_stats:
        continue

    stats = all_stats[interval]
    report_df = all_reports[interval]

    print(f"\n[{interval.upper()}] ANALYSIS RESULTS")
    print("-" * 100)

    print(f"""
Total FVG Patterns Detected: {stats['total_fvgs_detected']}

MAXIMUM MOVE DIRECTION ANALYSIS:
  Larger Move UP:                    {stats['larger_move_up_count']:,} patterns ({stats['larger_move_up_percentage']:.1f}%)
  Larger Move DOWN:                  {stats['larger_move_down_count']:,} patterns ({stats['larger_move_down_percentage']:.1f}%)

FIRST DIRECTION MOVED ANALYSIS:
  First Moved UP:                    {stats['first_moved_up']:,} patterns ({stats['first_direction_up_percentage']:.1f}%)
  First Moved DOWN:                  {stats['first_moved_down']:,} patterns ({stats['first_direction_down_percentage']:.1f}%)

MOVE SIZES (Points):
  Average Upside Move:               {stats['avg_max_upside']:.2f}
  Average Downside Move:             {stats['avg_max_downside']:.2f}
  Median Upside Move:                {stats['median_max_upside']:.2f}
  Median Downside Move:              {stats['median_max_downside']:.2f}

  Upside Range:                      {stats['max_upside_min']:.2f} - {stats['max_upside_max']:.2f}
  Downside Range:                    {stats['max_downside_min']:.2f} - {stats['max_downside_max']:.2f}

MOVE SIZES (Percentiles):
  Upside 25th:                       {stats['upside_25th_percentile']:.2f}
  Upside 50th (Median):              {stats['upside_50th_percentile']:.2f}
  Upside 75th:                       {stats['upside_75th_percentile']:.2f}

  Downside 25th:                     {stats['downside_25th_percentile']:.2f}
  Downside 50th (Median):            {stats['downside_50th_percentile']:.2f}
  Downside 75th:                     {stats['downside_75th_percentile']:.2f}

TIMING ANALYSIS (Candles):
  Avg Bars to Max Upside:            {stats['avg_bars_to_max_upside']:.1f}
  Avg Bars to Max Downside:          {stats['avg_bars_to_max_downside']:.1f}
  Avg Bars to Return to Middle:      {stats['avg_bars_to_return']:.1f}

PATTERN QUALITY:
  Doji on 3rd Candle:                {stats['doji_on_3rd_candle_count']} ({stats['doji_percentage']:.1f}%)
  Avg Body1 Ratio:                   {stats['avg_body1_ratio']:.2f} (< 0.50)
  Avg Body3 Ratio:                   {stats['avg_body3_ratio']:.2f} (< 0.50)
""")

print("\n" + "="*100)
print("DETAILED REPORTS SAVED TO:")
print("-" * 100)

for interval in TIMEFRAMES:
    if interval in all_reports:
        print(f"  ✓ analysis/fvg_comprehensive/FVG_MaxMove_{interval}_*.csv")

print(f"\nStatistics JSON: analysis/fvg_comprehensive/FVG_Statistics_*.json")

print("\n" + "="*100)
print("ANALYSIS COMPLETE")
print("="*100 + "\n")
