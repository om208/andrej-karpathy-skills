"""
Unit tests for inside bar detection logic
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy_validator import StrategyValidator, StrategyConfig
from tests.test_fixtures import TestFixtures


class TestInsideBarDetection(unittest.TestCase):
    """Test inside bar pattern detection"""

    def setUp(self):
        self.validator = StrategyValidator()

    def test_inside_bar_detected(self):
        """Test that inside bar pattern is correctly detected"""
        # Bar where high < prev_high AND low > prev_low
        is_inside, compression = self.validator.detect_inside_bar(
            current_high=98.0,
            current_low=92.0,
            prev_high=100.0,
            prev_low=90.0
        )
        self.assertTrue(is_inside, "Inside bar should be detected")
        self.assertAlmostEqual(compression, 0.6, places=2)

    def test_not_inside_bar_high_breaks(self):
        """Test that inside bar is not detected when high breaks"""
        is_inside, _ = self.validator.detect_inside_bar(
            current_high=102.0,  # > prev_high
            current_low=92.0,
            prev_high=100.0,
            prev_low=90.0
        )
        self.assertFalse(is_inside, "Should not detect inside bar when high breaks")

    def test_not_inside_bar_low_breaks(self):
        """Test that inside bar is not detected when low breaks"""
        is_inside, _ = self.validator.detect_inside_bar(
            current_high=98.0,
            current_low=88.0,  # < prev_low
            prev_high=100.0,
            prev_low=90.0
        )
        self.assertFalse(is_inside, "Should not detect inside bar when low breaks")

    def test_compression_ratio_calculation(self):
        """Test compression ratio calculation"""
        _, compression = self.validator.detect_inside_bar(
            current_high=75.0,
            current_low=25.0,  # range=50
            prev_high=100.0,
            prev_low=0.0       # range=100
        )
        self.assertAlmostEqual(compression, 0.5, places=2)

    def test_compression_ratio_zero_prev_range(self):
        """Test compression ratio when previous range is zero"""
        _, compression = self.validator.detect_inside_bar(
            current_high=50.0,
            current_low=50.0,
            prev_high=50.0,
            prev_low=50.0
        )
        self.assertEqual(compression, 0.0)

    def test_very_tight_compression(self):
        """Test very tight compression detection (0.20-0.35)"""
        is_inside, compression = self.validator.detect_inside_bar(
            current_high=62.5,  # range=25
            current_low=37.5,
            prev_high=100.0,
            prev_low=0.0        # range=100
        )
        self.assertTrue(is_inside)
        self.assertAlmostEqual(compression, 0.25, places=2)
        self.assertTrue(0.20 <= compression < 0.35)

    def test_medium_compression(self):
        """Test medium compression detection (0.50-0.65)"""
        is_inside, compression = self.validator.detect_inside_bar(
            current_high=77.5,  # range=55
            current_low=22.5,
            prev_high=100.0,
            prev_low=0.0        # range=100
        )
        self.assertTrue(is_inside)
        self.assertAlmostEqual(compression, 0.55, places=2)
        self.assertTrue(0.50 <= compression <= 0.65)

    def test_fixture_inside_bar_data(self):
        """Test with fixture data"""
        df = TestFixtures.create_inside_bar_data()
        row_1 = df.iloc[1]
        row_0 = df.iloc[0]

        is_inside, compression = self.validator.detect_inside_bar(
            current_high=row_1['high'],
            current_low=row_1['low'],
            prev_high=row_0['high'],
            prev_low=row_0['low']
        )

        self.assertTrue(is_inside)
        self.assertAlmostEqual(compression, 0.6, places=1)

    def test_fixture_not_inside_bar_data(self):
        """Test with fixture data that is NOT inside bar"""
        df = TestFixtures.create_not_inside_bar_data()
        row_1 = df.iloc[1]
        row_0 = df.iloc[0]

        is_inside, _ = self.validator.detect_inside_bar(
            current_high=row_1['high'],
            current_low=row_1['low'],
            prev_high=row_0['high'],
            prev_low=row_0['low']
        )

        self.assertFalse(is_inside)


if __name__ == '__main__':
    unittest.main()
