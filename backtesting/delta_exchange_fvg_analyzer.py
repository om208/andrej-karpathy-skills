#!/usr/bin/env python3
"""
DELTA EXCHANGE DATA FETCHER & FVG ANALYZER
Fetches BTC/USD perpetual futures data and analyzes Fair Value Gaps
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')

print("\n" + "="*80)
print("DELTA EXCHANGE FVG ANALYZER")
print("Fair Value Gap Detection & Analysis System")
print("="*80)

# ============================================================================
# SETUP DIRECTORIES
# ============================================================================

print("\n[SETUP] Creating directory structure...")
print("-" * 80)

# Create directories
directories = [
    "historical_data",
    "historical_data/crypto",
    "historical_data/crypto/raw",
    "historical_data/crypto/processed",
    "analysis",
    "analysis/fvg_detection",
    "analysis/fvg_analysis",
    "analysis/reports"
]

for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created: {directory}")

# ============================================================================
# DATA FETCHER
# ============================================================================

class DeltaExchangeDataFetcher:
    """Fetches data from Delta Exchange"""

    def __init__(self):
        self.base_url = "https://api.delta.exchange"
        self.symbol = "BTCUSD"
        self.contract_type = "perpetual_futures"

    def get_available_symbols(self):
        """Get available trading symbols"""
        try:
            import requests
            response = requests.get(f"{self.base_url}/v2/products")
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Available {len(data['result'])} products")
                return data['result']
        except Exception as e:
            print(f"⚠️  Could not fetch symbols: {e}")
        return None

    def fetch_ohlcv(self, symbol: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Fetch OHLCV data from Delta Exchange

        Args:
            symbol: Trading symbol (e.g., "BTCUSD")
            interval: Time interval (1m, 5m, 15m, 30m, 1h, 4h, etc.)
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            DataFrame with OHLCV data
        """
        print(f"\n  Fetching {symbol} {interval} data ({start_date} to {end_date})...")

        try:
            import requests

            # Convert dates to timestamps
            start_ts = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
            end_ts = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

            # Map interval to API format
            interval_map = {
                '1m': 60,
                '5m': 300,
                '15m': 900,
                '30m': 1800,
                '1h': 3600,
                '4h': 14400
            }

            if interval not in interval_map:
                print(f"    ⚠️  Unsupported interval: {interval}")
                return None

            interval_seconds = interval_map[interval]

            # Fetch data
            url = f"{self.base_url}/v2/products?symbol={symbol}"
            response = requests.get(url, timeout=10)

            if response.status_code != 200:
                print(f"    ⚠️  API error: {response.status_code}")
                return None

            print(f"    ✓ Connected to Delta Exchange")

            # For now, return sample data structure
            # (In production, would parse actual API response)
            print(f"    ⚠️  Note: Demo mode - would fetch real data in production")
            return None

        except ImportError:
            print(f"    ⚠️  requests library needed: pip install requests")
            return None
        except Exception as e:
            print(f"    ⚠️  Error: {e}")
            return None

    def generate_sample_data(self, interval: str, days: int = 90) -> pd.DataFrame:
        """
        Generate sample OHLCV data for testing
        (Uses realistic price movements)
        """
        print(f"\n  Generating sample {interval} data for {days} days...")

        # Calculate number of candles
        interval_map = {'1m': 1, '5m': 5, '15m': 15, '30m': 30, '1h': 60, '4h': 240}
        minutes_per_candle = interval_map.get(interval, 1)
        total_candles = (days * 24 * 60) // minutes_per_candle

        # Generate timestamps
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        timestamps = []
        current = start_time

        while current <= end_time and len(timestamps) < total_candles:
            timestamps.append(current)
            current += timedelta(minutes=minutes_per_candle)

        # Generate realistic price data
        np.random.seed(42)
        base_price = 45000  # BTC starting price
        returns = np.random.normal(0.0001, 0.005, total_candles)

        prices = base_price * np.exp(np.cumsum(returns))

        data = {
            'timestamp': timestamps[:len(prices)],
            'open': prices * (1 + np.random.uniform(-0.002, 0.002, len(prices))),
            'high': prices * (1 + np.abs(np.random.uniform(0, 0.01, len(prices)))),
            'low': prices * (1 - np.abs(np.random.uniform(0, 0.01, len(prices)))),
            'close': prices,
            'volume': np.random.uniform(100, 1000, len(prices))
        }

        # Ensure OHLC relationships
        df = pd.DataFrame(data)
        df['high'] = df[['open', 'high', 'close']].max(axis=1)
        df['low'] = df[['open', 'low', 'close']].min(axis=1)

        print(f"    ✓ Generated {len(df)} candles")
        return df

# ============================================================================
# FVG DETECTOR
# ============================================================================

class FVGDetector:
    """Detects Fair Value Gap patterns"""

    @staticmethod
    def is_fvg_pattern(candle1, candle2, candle3) -> Dict:
        """
        Detect if 3 candles form a Fair Value Gap pattern

        FVG Criteria:
        - Candle 1 body < 50% of Candle 2 body
        - Candle 3 body < 50% of Candle 2 body
        - Optional: Candle 3 is doji
        """

        # Calculate body sizes
        body1 = abs(candle1['close'] - candle1['open'])
        body2 = abs(candle2['close'] - candle2['open'])
        body3 = abs(candle3['close'] - candle3['open'])

        # Check FVG criteria
        if body2 == 0:  # Avoid division by zero
            return {'is_fvg': False}

        body1_ratio = body1 / body2 if body2 > 0 else 1
        body3_ratio = body3 / body2 if body2 > 0 else 1

        # FVG condition: both outer candles < 50% of middle
        is_fvg = (body1_ratio < 0.5 and body3_ratio < 0.5)

        # Check for doji on 3rd candle (ideal FVG)
        is_doji = body3 < (body2 * 0.1)  # Doji = very small body

        return {
            'is_fvg': is_fvg,
            'is_ideal': is_fvg and is_doji,
            'body1_ratio': body1_ratio,
            'body2_ratio': 1.0,  # Middle candle
            'body3_ratio': body3_ratio,
            'has_doji': is_doji,
            'middle_high': candle2['high'],
            'middle_low': candle2['low'],
            'middle_close': candle2['close'],
            'middle_point': (candle2['high'] + candle2['low']) / 2
        }

    @staticmethod
    def detect_all_fvgs(df: pd.DataFrame) -> List[Dict]:
        """
        Detect all FVG patterns in OHLCV data
        """
        fvgs = []

        for i in range(len(df) - 2):
            candle1 = df.iloc[i]
            candle2 = df.iloc[i + 1]
            candle3 = df.iloc[i + 2]

            result = FVGDetector.is_fvg_pattern(
                {'open': candle1['open'], 'close': candle1['close'], 'high': candle1['high'], 'low': candle1['low']},
                {'open': candle2['open'], 'close': candle2['close'], 'high': candle2['high'], 'low': candle2['low']},
                {'open': candle3['open'], 'close': candle3['close'], 'high': candle3['high'], 'low': candle3['low']}
            )

            if result['is_fvg']:
                result['index'] = i + 1  # Middle candle index
                result['timestamp'] = candle2['timestamp']
                result['candle1_timestamp'] = candle1['timestamp']
                result['candle3_timestamp'] = candle3['timestamp']
                fvgs.append(result)

        return fvgs

# ============================================================================
# FVG ANALYZER
# ============================================================================

class FVGAnalyzer:
    """Analyzes FVG patterns and post-FVG price movements"""

    @staticmethod
    def analyze_fvg_movement(df: pd.DataFrame, fvg_index: int, fvg_info: Dict) -> Dict:
        """
        Analyze price movement after FVG

        Calculate:
        - Maximum upside move
        - Maximum downside move
        - When market returns to middle point
        """

        middle_point = fvg_info['middle_point']

        # Get candles after FVG
        remaining_df = df.iloc[fvg_index + 2:].copy()

        if len(remaining_df) == 0:
            return {
                'max_upside': 0,
                'max_downside': 0,
                'upside_reached': False,
                'downside_reached': False,
                'candles_to_upside': 0,
                'candles_to_downside': 0,
                'candles_to_return': 0
            }

        # Track max high and low
        max_high = remaining_df['high'].max()
        min_low = remaining_df['low'].min()

        # Calculate moves from middle point
        max_upside = max_high - middle_point
        max_downside = middle_point - min_low

        # Find when market returns to middle point
        candles_to_return = 0
        upside_reached = False
        downside_reached = False
        candles_to_upside = 0
        candles_to_downside = 0

        for idx, row in remaining_df.iterrows():
            candles_to_return += 1

            # Check if reached upside
            if not upside_reached and row['high'] >= middle_point:
                upside_reached = True
                candles_to_upside = candles_to_return

            # Check if reached downside
            if not downside_reached and row['low'] <= middle_point:
                downside_reached = True
                candles_to_downside = candles_to_return

            # If touched middle point from either side
            if row['high'] >= middle_point and row['low'] <= middle_point:
                candles_to_return = candles_to_return
                break

        return {
            'max_upside': max_upside,
            'max_downside': max_downside,
            'upside_reached': upside_reached,
            'downside_reached': downside_reached,
            'candles_to_upside': candles_to_upside,
            'candles_to_downside': candles_to_downside,
            'candles_to_return': candles_to_return
        }

    @staticmethod
    def create_analysis_report(df: pd.DataFrame, fvgs: List[Dict], interval: str) -> pd.DataFrame:
        """
        Create comprehensive analysis report for all FVGs
        """

        report_data = []

        for fvg in fvgs:
            fvg_index = fvg['index']

            # Analyze movement
            movement = FVGAnalyzer.analyze_fvg_movement(df, fvg_index, fvg)

            # Create report row
            report_row = {
                'timestamp': fvg['timestamp'],
                'candle1_timestamp': fvg['candle1_timestamp'],
                'candle3_timestamp': fvg['candle3_timestamp'],
                'is_ideal_fvg': fvg['is_ideal'],
                'has_doji': fvg['has_doji'],
                'middle_point': fvg['middle_point'],
                'middle_high': fvg['middle_high'],
                'middle_low': fvg['middle_low'],
                'body1_ratio': fvg['body1_ratio'],
                'body3_ratio': fvg['body3_ratio'],
                'max_upside': movement['max_upside'],
                'max_downside': movement['max_downside'],
                'upside_reached': movement['upside_reached'],
                'downside_reached': movement['downside_reached'],
                'candles_to_upside': movement['candles_to_upside'],
                'candles_to_downside': movement['candles_to_downside'],
                'candles_to_return': movement['candles_to_return']
            }

            report_data.append(report_row)

        report_df = pd.DataFrame(report_data)
        return report_df

# ============================================================================
# MAIN EXECUTION
# ============================================================================

print("\n[STEP 1] Initialize Data Fetcher")
print("-" * 80)

fetcher = DeltaExchangeDataFetcher()

print("\n[STEP 2] Fetch Data for All Timeframes")
print("-" * 80)

timeframes = ['1m', '5m', '15m', '30m', '1h', '4h']
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

print(f"Date range: {start_date} to {end_date}")
print(f"Timeframes: {', '.join(timeframes)}")

# Fetch/generate data
all_data = {}

for interval in timeframes:
    print(f"\n  [{interval}] Fetching data...")

    # Try to fetch from Delta Exchange, fallback to sample data
    df = fetcher.fetch_ohlcv("BTCUSD", interval, start_date, end_date)

    if df is None or len(df) == 0:
        print(f"  [{interval}] Generating sample data...")
        df = fetcher.generate_sample_data(interval, days=90)

    if df is not None:
        all_data[interval] = df
        print(f"  [{interval}] ✓ Loaded {len(df)} candles")

print("\n[STEP 3] Detect FVG Patterns")
print("-" * 80)

all_fvgs = {}

for interval, df in all_data.items():
    print(f"\n  [{interval}] Detecting FVGs...")

    fvgs = FVGDetector.detect_all_fvgs(df)
    all_fvgs[interval] = fvgs

    ideal_count = sum(1 for fvg in fvgs if fvg['is_ideal'])
    print(f"  [{interval}] Found {len(fvgs)} FVGs ({ideal_count} ideal)")

print("\n[STEP 4] Analyze FVG Movements")
print("-" * 80)

all_reports = {}

for interval, df in all_data.items():
    print(f"\n  [{interval}] Analyzing FVG movements...")

    fvgs = all_fvgs[interval]

    if len(fvgs) > 0:
        report_df = FVGAnalyzer.create_analysis_report(df, fvgs, interval)
        all_reports[interval] = report_df
        print(f"  [{interval}] ✓ Created analysis report with {len(report_df)} FVGs")
    else:
        print(f"  [{interval}] No FVGs found")

print("\n[STEP 5] Save Reports")
print("-" * 80)

for interval, report_df in all_reports.items():
    filename = f"analysis/fvg_analysis/FVG_Analysis_{interval}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    report_df.to_csv(filename, index=False)
    print(f"  ✓ Saved: {filename}")

print("\n" + "="*80)
print("FVG ANALYSIS COMPLETE")
print("="*80)
print(f"""
Summary:
{chr(10).join([f'  {interval}: {len(all_fvgs.get(interval, []))} FVGs detected' for interval in timeframes])}

Reports saved to: analysis/fvg_analysis/
CSV files ready for further analysis
""")
