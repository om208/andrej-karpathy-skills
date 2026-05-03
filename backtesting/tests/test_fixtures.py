"""
Test fixtures for strategy validation.
Contains known test data and expected results.
"""

from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict


class TestFixtures:
    """Known test data with expected outcomes"""

    @staticmethod
    def create_inside_bar_data() -> pd.DataFrame:
        """
        Create test data where:
        - Bar 0: prev_high=100, prev_low=90, range=10
        - Bar 1: current_high=98, current_low=92, range=6 (INSIDE BAR)
        - Compression: 6/10 = 0.60
        """
        data = [
            {
                'timestamp': datetime(2026, 5, 1, 10, 0),
                'open': 95.0,
                'high': 100.0,
                'low': 90.0,
                'close': 95.0
            },
            {
                'timestamp': datetime(2026, 5, 1, 10, 1),
                'open': 95.0,
                'high': 98.0,  # < prev_high (100)
                'low': 92.0,   # > prev_low (90)
                'close': 96.0
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def create_not_inside_bar_data() -> pd.DataFrame:
        """
        Create test data where bar does NOT form inside bar:
        - Bar 0: prev_high=100, prev_low=90
        - Bar 1: current_high=102 (> prev_high, BREAKS INSIDE)
        """
        data = [
            {
                'timestamp': datetime(2026, 5, 1, 10, 0),
                'open': 95.0,
                'high': 100.0,
                'low': 90.0,
                'close': 95.0
            },
            {
                'timestamp': datetime(2026, 5, 1, 10, 1),
                'open': 95.0,
                'high': 102.0,  # > prev_high (100) - NOT INSIDE
                'low': 92.0,
                'close': 96.0
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def create_sma_touch_data() -> pd.DataFrame:
        """
        Create data with SMA(3) that touches the candle:
        - Bars 0-2: build SMA base
        - Bar 3: SMA should be within 2% threshold of candle

        Close values: [100, 101, 102, 103]
        SMA(3) at bar 3: (100+101+102)/3 = 101
        Candle 3: high=104, low=100, range=4, threshold_2%=0.08
        SMA 101 is within [99.92, 104.08] = TOUCHES
        """
        closes = [100, 101, 102, 103]
        data = []
        for i, close in enumerate(closes):
            data.append({
                'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=i),
                'open': close - 0.5,
                'high': close + 2,
                'low': close - 2,
                'close': close
            })
        return pd.DataFrame(data)

    @staticmethod
    def create_sma_no_touch_data() -> pd.DataFrame:
        """
        Create data where SMA does NOT touch the candle:
        SMA is way above the candle.
        """
        closes = [100, 101, 102, 103]
        data = []
        for i, close in enumerate(closes):
            data.append({
                'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=i),
                'open': close - 0.5,
                'high': close - 5,  # Way below
                'low': close - 10,
                'close': close
            })
        return pd.DataFrame(data)

    @staticmethod
    def create_very_tight_compression_data() -> pd.DataFrame:
        """
        Create data with very tight compression (0.25):
        - Bar 0: prev_range=100
        - Bar 1: current_range=25 (compression=0.25, IN 0.20-0.35 range)
        """
        data = [
            {
                'timestamp': datetime(2026, 5, 1, 10, 0),
                'open': 50.0,
                'high': 100.0,
                'low': 0.0,
                'close': 50.0
            },
            {
                'timestamp': datetime(2026, 5, 1, 10, 1),
                'open': 50.0,
                'high': 62.5,  # 25 range
                'low': 37.5,
                'close': 50.0
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def create_medium_compression_data() -> pd.DataFrame:
        """
        Create data with medium compression (0.55):
        - Bar 0: prev_range=100
        - Bar 1: current_range=55 (compression=0.55, IN 0.50-0.65 range)
        """
        data = [
            {
                'timestamp': datetime(2026, 5, 1, 10, 0),
                'open': 50.0,
                'high': 100.0,
                'low': 0.0,
                'close': 50.0
            },
            {
                'timestamp': datetime(2026, 5, 1, 10, 1),
                'open': 50.0,
                'high': 77.5,  # 55 range
                'low': 22.5,
                'close': 50.0
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def create_good_compression_data() -> pd.DataFrame:
        """
        Create data with good compression (0.40):
        - Bar 0: prev_range=100
        - Bar 1: current_range=40 (compression=0.40, NOT in bad ranges)
        """
        data = [
            {
                'timestamp': datetime(2026, 5, 1, 10, 0),
                'open': 50.0,
                'high': 100.0,
                'low': 0.0,
                'close': 50.0
            },
            {
                'timestamp': datetime(2026, 5, 1, 10, 1),
                'open': 50.0,
                'high': 70.0,  # 40 range
                'low': 30.0,
                'close': 50.0
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def create_downward_momentum_data() -> pd.DataFrame:
        """
        Create data with downward post-entry momentum:
        - close < open
        - close near low (within 30% of range)
        """
        data = [
            {
                'timestamp': datetime(2026, 5, 1, 10, 0),
                'open': 50.0,
                'high': 55.0,
                'low': 45.0,
                'close': 50.0
            },
            {
                'timestamp': datetime(2026, 5, 1, 10, 1),
                'open': 50.0,
                'high': 51.0,
                'low': 47.0,
                'close': 47.3  # close < open, close near low
            }
        ]
        return pd.DataFrame(data)

    @staticmethod
    def create_complete_signal_sequence() -> pd.DataFrame:
        """
        Create a realistic sequence with:
        1. Inside bar pattern
        2. SMA touch
        3. Good compression (no risk score)
        Should produce a valid entry signal
        """
        # Build 196 candles for SMA to stabilize
        closes = list(range(100, 296))  # 100-295
        data = []

        for i, close in enumerate(closes):
            data.append({
                'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=i),
                'open': close - 0.5,
                'high': close + 2,
                'low': close - 2,
                'close': close
            })

        # Add inside bar at the end
        # Bar 195: prev_high=296, prev_low=292
        # Bar 196: inside bar with good compression
        data.append({
            'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=196),
            'open': 296.0,
            'high': 299.0,
            'low': 293.0,
            'close': 296.0
        })

        # Bar 197: inside bar (inside: high<299, low>293)
        data.append({
            'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=197),
            'open': 296.0,
            'high': 298.0,  # < 299
            'low': 294.0,   # > 293
            'close': 296.5
        })

        return pd.DataFrame(data)

    @staticmethod
    def create_entry_to_exit_sequence() -> pd.DataFrame:
        """
        Create sequence showing:
        1. Entry signal (inside bar + SMA touch + risk score 0)
        2. Lot 1 exits at +250 pips
        3. Lot 2 exits at 159 minutes

        Entry at 100, Lot 1 TP at 100.0250 (250 pips = 250*0.0001)
        """
        closes = list(range(100, 296))
        data = []

        for i, close in enumerate(closes):
            data.append({
                'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=i),
                'open': close - 0.5,
                'high': close + 0.5,
                'low': close - 0.5,
                'close': close
            })

        # Entry signal at bar 195
        data.append({
            'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=196),
            'open': 296.0,
            'high': 297.0,
            'low': 295.0,
            'close': 296.0
        })

        data.append({
            'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=197),
            'open': 296.0,
            'high': 297.0,
            'low': 295.0,
            'close': 296.5
        })

        # Lot 1 hits TP at +250 pips from 296 = 296.0250
        # Add bars until we reach that price
        for i in range(198, 250):
            data.append({
                'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=i),
                'open': 296.5,
                'high': 296.0250,  # TP hit here
                'low': 296.3,
                'close': 296.01
            })

        # After 159 minutes, Lot 2 exits
        # From entry bar (197) + 159 = bar 356
        for i in range(250, 356):
            data.append({
                'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=i),
                'open': 296.0,
                'high': 296.5,
                'low': 295.5,
                'close': 296.0
            })

        # Final exit at bar 356
        data.append({
            'timestamp': datetime(2026, 5, 1, 10, 0) + timedelta(minutes=356),
            'open': 296.0,
            'high': 297.0,
            'low': 295.0,
            'close': 296.2
        })

        return pd.DataFrame(data)


def load_test_fixtures() -> Dict[str, pd.DataFrame]:
    """Load all test fixtures"""
    fixtures = TestFixtures()
    return {
        'inside_bar': fixtures.create_inside_bar_data(),
        'not_inside_bar': fixtures.create_not_inside_bar_data(),
        'sma_touch': fixtures.create_sma_touch_data(),
        'sma_no_touch': fixtures.create_sma_no_touch_data(),
        'very_tight_compression': fixtures.create_very_tight_compression_data(),
        'medium_compression': fixtures.create_medium_compression_data(),
        'good_compression': fixtures.create_good_compression_data(),
        'downward_momentum': fixtures.create_downward_momentum_data(),
        'complete_signal_sequence': fixtures.create_complete_signal_sequence(),
        'entry_to_exit_sequence': fixtures.create_entry_to_exit_sequence(),
    }
