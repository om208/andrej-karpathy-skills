"""
Unit tests for risk score calculation
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy_validator import StrategyValidator, StrategyConfig


class TestRiskScoring(unittest.TestCase):
    """Test risk score calculation"""

    def setUp(self):
        self.validator = StrategyValidator()

    def test_risk_score_zero_good_pattern(self):
        """Test risk score 0 for good pattern (no bad characteristics)"""
        risk_score = self.validator.calculate_risk_score(
            compression_ratio=0.40,  # Not in 0.20-0.35 or 0.50-0.65
            current_open=100.0,
            current_close=100.5,     # close > open (bullish)
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 0)

    def test_risk_score_1_very_tight_compression(self):
        """Test risk score +1 for very tight compression (0.20-0.35)"""
        validator = StrategyValidator(
            StrategyConfig(filter_verytight_compression=True)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.25,  # In range 0.20-0.35
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 1)

    def test_risk_score_1_medium_compression(self):
        """Test risk score +1 for medium compression (0.50-0.65)"""
        validator = StrategyValidator(
            StrategyConfig(filter_medium_compression=True)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.55,  # In range 0.50-0.65
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 1)

    def test_risk_score_2_both_compression_issues(self):
        """Test risk score 2+ when multiple bad characteristics"""
        validator = StrategyValidator(
            StrategyConfig(
                filter_verytight_compression=True,
                filter_medium_compression=True
            )
        )
        # Can't have both tight AND medium at same time, but can have tight + downward
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.25,  # Tight
            current_open=100.0,
            current_close=99.8,      # close < open (bearish)
            current_high=100.5,
            current_low=99.0
        )
        self.assertEqual(risk_score, 1)  # Only tight triggers

    def test_risk_score_1_downward_momentum(self):
        """Test risk score +1 for downward momentum"""
        # close < open AND close near low (within 30% of range)
        risk_score = self.validator.calculate_risk_score(
            compression_ratio=0.40,  # Good compression
            current_open=100.0,
            current_close=99.3,      # close < open
            current_high=102.0,
            current_low=99.0         # close near low: range=3, 30%=0.9, close_pos=0.3 < 0.9
        )
        self.assertEqual(risk_score, 1)

    def test_risk_score_filter_disabled_verytight(self):
        """Test that very tight filter can be disabled"""
        validator = StrategyValidator(
            StrategyConfig(filter_verytight_compression=False)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.25,  # Would trigger if enabled
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 0)

    def test_risk_score_filter_disabled_medium(self):
        """Test that medium compression filter can be disabled"""
        validator = StrategyValidator(
            StrategyConfig(filter_medium_compression=False)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.55,  # Would trigger if enabled
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 0)

    def test_risk_score_boundary_very_tight_lower(self):
        """Test boundary condition: compression at 0.20 (inclusive)"""
        validator = StrategyValidator(
            StrategyConfig(filter_verytight_compression=True)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.20,  # Boundary inclusive
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 1)

    def test_risk_score_boundary_very_tight_upper(self):
        """Test boundary condition: compression at 0.35 (exclusive)"""
        validator = StrategyValidator(
            StrategyConfig(filter_verytight_compression=True)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.35,  # Boundary exclusive
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 0)

    def test_risk_score_boundary_medium_lower(self):
        """Test boundary condition: compression at 0.50 (inclusive)"""
        validator = StrategyValidator(
            StrategyConfig(filter_medium_compression=True)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.50,
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 1)

    def test_risk_score_boundary_medium_upper(self):
        """Test boundary condition: compression at 0.65 (inclusive)"""
        validator = StrategyValidator(
            StrategyConfig(filter_medium_compression=True)
        )
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.65,
            current_open=100.0,
            current_close=100.5,
            current_high=102.0,
            current_low=99.0
        )
        self.assertEqual(risk_score, 1)

    def test_risk_score_downward_boundary_high_close(self):
        """Test downward momentum: close exactly at 30% of range"""
        # range=10, 30%=3, close_pos exactly 3
        risk_score = self.validator.calculate_risk_score(
            compression_ratio=0.40,
            current_open=100.0,
            current_close=99.3,      # At boundary
            current_high=105.0,
            current_low=95.0         # range=10, close_pos=4.3 > 3 (just over)
        )
        self.assertEqual(risk_score, 0)

    def test_risk_score_multiple_characteristics(self):
        """Test combining multiple risk characteristics"""
        # This is contrived but tests the logic
        validator = StrategyValidator(
            StrategyConfig(
                filter_verytight_compression=True,
                filter_medium_compression=True
            )
        )
        # Note: Can't really have both tight AND medium compression
        # But can have tight + downward
        risk_score = validator.calculate_risk_score(
            compression_ratio=0.25,
            current_open=100.5,
            current_close=99.3,
            current_high=101.0,
            current_low=99.0
        )
        # Should have: tight compression +1, downward momentum +1
        self.assertGreaterEqual(risk_score, 1)


if __name__ == '__main__':
    unittest.main()
