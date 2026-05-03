"""
Unit tests for SMA(196) calculation and touch detection
"""

import unittest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy_validator import StrategyValidator, StrategyConfig
from tests.test_fixtures import TestFixtures


class TestSMACalculation(unittest.TestCase):
    """Test SMA calculation"""

    def setUp(self):
        self.validator = StrategyValidator()

    def test_sma_calculation_simple(self):
        """Test SMA calculation with simple data"""
        closes = np.array([100, 101, 102, 103, 104])
        sma = self.validator.calculate_sma(closes, period=3, bar_index=4)
        expected = (102 + 103 + 104) / 3
        self.assertAlmostEqual(sma, expected, places=2)

    def test_sma_insufficient_data(self):
        """Test SMA when insufficient data available"""
        closes = np.array([100, 101])
        sma = self.validator.calculate_sma(closes, period=3, bar_index=1)
        self.assertIsNone(sma)

    def test_sma_exact_period(self):
        """Test SMA when bar_index equals period-1"""
        closes = np.array([100, 101, 102])
        sma = self.validator.calculate_sma(closes, period=3, bar_index=2)
        expected = (100 + 101 + 102) / 3
        self.assertAlmostEqual(sma, expected, places=2)

    def test_sma_196_period(self):
        """Test SMA(196) with 196-period data"""
        # Create 196 candles with incrementing closes
        closes = np.array(list(range(100, 296)))
        sma = self.validator.calculate_sma(closes, period=196, bar_index=195)
        # SMA should be average of bars 0-195
        expected = np.mean(closes[0:196])
        self.assertAlmostEqual(sma, expected, places=2)

    def test_sma_touches_candle(self):
        """Test SMA touch detection - SMA touches candle"""
        # SMA = 101, candle high=104, low=100, range=4, threshold 2%=0.08
        sma_touches = self.validator.detect_sma_touch(
            sma_value=101.0,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=2.0
        )
        self.assertTrue(sma_touches, "SMA should touch candle")

    def test_sma_touches_at_high(self):
        """Test SMA touch when SMA equals high"""
        sma_touches = self.validator.detect_sma_touch(
            sma_value=104.0,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=2.0
        )
        self.assertTrue(sma_touches)

    def test_sma_touches_at_low(self):
        """Test SMA touch when SMA equals low"""
        sma_touches = self.validator.detect_sma_touch(
            sma_value=100.0,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=2.0
        )
        self.assertTrue(sma_touches)

    def test_sma_no_touch_above(self):
        """Test SMA does not touch when above threshold"""
        # High=104, low=100, range=4, threshold 2%=0.08
        # Above high: 104 + 0.08 = 104.08
        # SMA at 105 should not touch
        sma_touches = self.validator.detect_sma_touch(
            sma_value=105.0,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=2.0
        )
        self.assertFalse(sma_touches)

    def test_sma_no_touch_below(self):
        """Test SMA does not touch when below threshold"""
        # Low=100, range=4, threshold 2%=0.08
        # Below low: 100 - 0.08 = 99.92
        # SMA at 99 should not touch
        sma_touches = self.validator.detect_sma_touch(
            sma_value=99.0,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=2.0
        )
        self.assertFalse(sma_touches)

    def test_sma_touch_different_threshold(self):
        """Test SMA touch with different threshold"""
        sma_touches = self.validator.detect_sma_touch(
            sma_value=105.0,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=5.0  # 5% = 0.20
        )
        # High + threshold = 104 + 0.20 = 104.20
        # SMA at 105 is still outside
        self.assertFalse(sma_touches)

    def test_sma_touch_with_small_range(self):
        """Test SMA touch with small candle range"""
        # Range=0.10, threshold 2%=0.002
        sma_touches = self.validator.detect_sma_touch(
            sma_value=100.0010,
            current_high=100.10,
            current_low=100.00,
            threshold_pct=2.0
        )
        self.assertTrue(sma_touches)

    def test_sma_none_value(self):
        """Test SMA touch detection with None SMA"""
        sma_touches = self.validator.detect_sma_touch(
            sma_value=None,
            current_high=104.0,
            current_low=100.0,
            threshold_pct=2.0
        )
        self.assertFalse(sma_touches)

    def test_fixture_sma_touch(self):
        """Test with fixture data - SMA touches"""
        df = TestFixtures.create_sma_touch_data()
        validator = StrategyValidator(StrategyConfig(sma_period=3))

        closes = df['close'].values
        bar_index = 3

        sma = validator.calculate_sma(closes, 3, bar_index)
        self.assertIsNotNone(sma)
        # SMA(3) at bar 3: average of closes[1:4] = [101,102,103] = 102
        self.assertAlmostEqual(sma, 102.0, places=1)

        row = df.iloc[bar_index]
        sma_touches = validator.detect_sma_touch(
            sma,
            row['high'],
            row['low'],
            threshold_pct=2.0
        )
        self.assertTrue(sma_touches)


if __name__ == '__main__':
    unittest.main()
