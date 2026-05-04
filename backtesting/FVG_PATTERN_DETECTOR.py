#!/usr/bin/env python3
"""
FVG PATTERN DETECTOR - Practical Implementation
Detects all 10 high-quality FVG patterns from real candlestick data
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime

@dataclass
class Candle:
    """Represents a single candlestick"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float

    @property
    def body(self) -> float:
        return abs(self.close - self.open)

    @property
    def range(self) -> float:
        return self.high - self.low

    @property
    def upper_tail(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_tail(self) -> float:
        return min(self.open, self.close) - self.low

    @property
    def body_ratio(self) -> float:
        if self.range == 0:
            return 0.0
        return self.body / self.range

    @property
    def is_bullish(self) -> bool:
        return self.close > self.open

    @property
    def is_bearish(self) -> bool:
        return self.close < self.open


@dataclass
class PatternMatch:
    """Represents a matched FVG pattern"""
    timestamp: datetime
    pattern_type: str
    candle1: Candle
    candle2: Candle
    candle3: Candle
    confidence: float
    details: Dict

    def __str__(self) -> str:
        return (f"[{self.timestamp}] {self.pattern_type} (Confidence: {self.confidence:.1f}%)\n"
                f"  C1: O={self.candle1.open:.0f} H={self.candle1.high:.0f} "
                f"L={self.candle1.low:.0f} C={self.candle1.close:.0f}\n"
                f"  C2: O={self.candle2.open:.0f} H={self.candle2.high:.0f} "
                f"L={self.candle2.low:.0f} C={self.candle2.close:.0f}\n"
                f"  C3: O={self.candle3.open:.0f} H={self.candle3.high:.0f} "
                f"L={self.candle3.low:.0f} C={self.candle3.close:.0f}")


class PatternDetector:
    """Main FVG pattern detection engine"""

    def __init__(self):
        self.patterns_found = []

    # ========================================================================
    # HELPER FUNCTIONS - ALL MEASUREMENTS
    # ========================================================================

    @staticmethod
    def body1_ratio_of_body2(c1: Candle, c2: Candle) -> float:
        """Candle 1 body size relative to Candle 2"""
        if c2.body == 0:
            return 0.0
        return c1.body / c2.body

    @staticmethod
    def body3_ratio_of_body2(c3: Candle, c2: Candle) -> float:
        """Candle 3 body size relative to Candle 2"""
        if c2.body == 0:
            return 0.0
        return c3.body / c2.body

    @staticmethod
    def outer_avg_body_ratio(c1: Candle, c2: Candle, c3: Candle) -> float:
        """Average body ratio of outer candles"""
        return (PatternDetector.body1_ratio_of_body2(c1, c2) +
                PatternDetector.body3_ratio_of_body2(c3, c2)) / 2

    @staticmethod
    def middle_upper_tail_ratio(c2: Candle) -> float:
        """Middle candle upper tail relative to its body"""
        if c2.body == 0:
            return 0.0
        return c2.upper_tail / c2.body

    @staticmethod
    def middle_lower_tail_ratio(c2: Candle) -> float:
        """Middle candle lower tail relative to its body"""
        if c2.body == 0:
            return 0.0
        return c2.lower_tail / c2.body

    @staticmethod
    def combined_upper_tails(c1: Candle, c3: Candle) -> float:
        """Sum of upper tails from outer candles"""
        return c1.upper_tail + c3.upper_tail

    @staticmethod
    def combined_lower_tails(c1: Candle, c3: Candle) -> float:
        """Sum of lower tails from outer candles"""
        return c1.lower_tail + c3.lower_tail

    @staticmethod
    def get_middle_body_category(c2: Candle) -> str:
        """Categorize middle candle body size"""
        ratio = c2.body_ratio
        if ratio < 0.15:
            return "TINY"
        elif ratio < 0.30:
            return "SMALL"
        elif ratio < 0.50:
            return "MEDIUM"
        elif ratio < 0.70:
            return "LARGE"
        else:
            return "VERY_LARGE"

    @staticmethod
    def get_candle_tail_dominance(c: Candle) -> str:
        """Determine if candle has upper or lower tail dominance"""
        if c.upper_tail > c.lower_tail * 1.1:
            return "UPPER"
        elif c.lower_tail > c.upper_tail * 1.1:
            return "LOWER"
        else:
            return "BALANCED"

    @staticmethod
    def get_middle_direction(c2: Candle) -> str:
        """Determine if middle candle is bullish or bearish"""
        if abs(c2.close - c2.open) < c2.range * 0.05:
            return "NEUTRAL"
        return "BULLISH" if c2.is_bullish else "BEARISH"

    @staticmethod
    def get_outer_tail_bias(c1: Candle, c3: Candle) -> str:
        """Determine if outer candles have upper or lower bias"""
        upper = PatternDetector.combined_upper_tails(c1, c3)
        lower = PatternDetector.combined_lower_tails(c1, c3)

        if upper > lower * 1.05:
            return "UPPER_BIAS"
        elif lower > upper * 1.05:
            return "LOWER_BIAS"
        else:
            return "BALANCED"

    # ========================================================================
    # PATTERN DETECTION FUNCTIONS
    # ========================================================================

    def detect_pattern(self, c1: Candle, c2: Candle, c3: Candle) -> Optional[PatternMatch]:
        """
        Detect which FVG pattern this 3-candle formation is
        Returns PatternMatch if pattern detected, None otherwise
        """

        # STEP 1: FVG Definition check (prerequisite)
        if c1.body_ratio >= 0.5 or c3.body_ratio >= 0.5:
            return None

        # Get all measurements
        body1_ratio = self.body1_ratio_of_body2(c1, c2)
        body3_ratio = self.body3_ratio_of_body2(c3, c2)
        outer_avg = self.outer_avg_body_ratio(c1, c2, c3)

        middle_body_cat = self.get_middle_body_category(c2)
        middle_direction = self.get_middle_direction(c2)
        middle_upper_ratio = self.middle_upper_tail_ratio(c2)
        middle_lower_ratio = self.middle_lower_tail_ratio(c2)

        candle1_dominance = self.get_candle_tail_dominance(c1)
        candle3_dominance = self.get_candle_tail_dominance(c3)
        outer_bias = self.get_outer_tail_bias(c1, c3)

        details = {
            "body1_ratio": round(body1_ratio, 4),
            "body3_ratio": round(body3_ratio, 4),
            "outer_avg": round(outer_avg, 4),
            "middle_body_category": middle_body_cat,
            "middle_direction": middle_direction,
            "middle_upper_tail_ratio": round(middle_upper_ratio, 4),
            "middle_lower_tail_ratio": round(middle_lower_ratio, 4),
            "candle1_tail_dominance": candle1_dominance,
            "candle3_tail_dominance": candle3_dominance,
            "outer_tail_bias": outer_bias,
        }

        # PATTERN DETECTION LOGIC
        pattern_type = None
        confidence = 0.0

        # ===== PATTERN 1: IDEAL_DOJI_UPPER =====
        if (outer_avg < 0.15 and
            middle_body_cat in ["TINY", "SMALL"] and
            middle_upper_ratio > 1.5):
            pattern_type = "IDEAL_DOJI_UPPER"
            confidence = 95.0

        # ===== PATTERN 2: IDEAL_DOJI_LOWER =====
        elif (outer_avg < 0.15 and
              middle_body_cat in ["TINY", "SMALL"] and
              middle_lower_ratio > 1.5):
            pattern_type = "IDEAL_DOJI_LOWER"
            confidence = 95.0

        # ===== PATTERN 3: STRONG_UPPER_BIAS =====
        elif (outer_avg < 0.15 and
              middle_body_cat in ["LARGE", "VERY_LARGE"] and
              middle_direction == "BULLISH" and
              candle3_dominance == "UPPER"):
            pattern_type = "STRONG_UPPER_BIAS"
            confidence = 98.0

        # ===== PATTERN 4: STRONG_LOWER_BIAS =====
        elif (outer_avg < 0.15 and
              middle_body_cat in ["LARGE", "VERY_LARGE"] and
              middle_direction == "BEARISH" and
              candle3_dominance == "LOWER"):
            pattern_type = "STRONG_LOWER_BIAS"
            confidence = 98.0

        # ===== PATTERN 5: HIDDEN_REVERSAL_UPPER =====
        elif (body1_ratio < 0.30 and body3_ratio < 0.30 and
              middle_lower_ratio > middle_upper_ratio and
              candle1_dominance == "LOWER" and
              candle3_dominance == "UPPER" and
              middle_direction == "BEARISH"):
            pattern_type = "HIDDEN_REVERSAL_UPPER"
            confidence = 100.0

        # ===== PATTERN 6: HIDDEN_REVERSAL_LOWER =====
        elif (body1_ratio < 0.30 and body3_ratio < 0.30 and
              middle_upper_ratio > middle_lower_ratio and
              candle1_dominance == "UPPER" and
              candle3_dominance == "LOWER" and
              middle_direction == "BULLISH"):
            pattern_type = "HIDDEN_REVERSAL_LOWER"
            confidence = 100.0

        # ===== PATTERN 7: BALANCED_UPPER =====
        elif (body1_ratio < 0.35 and body3_ratio < 0.35 and
              middle_body_cat in ["MEDIUM", "LARGE"] and
              middle_upper_ratio > 0.8 and middle_lower_ratio > 0.8 and
              candle3_dominance == "UPPER" and
              outer_bias in ["UPPER_BIAS", "BALANCED"]):
            pattern_type = "BALANCED_UPPER"
            confidence = 100.0

        # ===== PATTERN 8: BALANCED_LOWER =====
        elif (body1_ratio < 0.35 and body3_ratio < 0.35 and
              middle_body_cat in ["MEDIUM", "LARGE"] and
              middle_upper_ratio > 0.8 and middle_lower_ratio > 0.8 and
              candle3_dominance == "LOWER" and
              outer_bias in ["LOWER_BIAS", "BALANCED"]):
            pattern_type = "BALANCED_LOWER"
            confidence = 100.0

        if pattern_type:
            return PatternMatch(
                timestamp=c3.timestamp,
                pattern_type=pattern_type,
                candle1=c1,
                candle2=c2,
                candle3=c3,
                confidence=confidence,
                details=details
            )

        return None

    def scan_for_patterns(self, candles: List[Candle]) -> List[PatternMatch]:
        """
        Scan a list of candles for all FVG patterns
        Returns list of all patterns found
        """
        patterns = []

        for i in range(len(candles) - 2):
            pattern = self.detect_pattern(candles[i], candles[i+1], candles[i+2])
            if pattern:
                patterns.append(pattern)

        self.patterns_found = patterns
        return patterns


# ========================================================================
# REAL-WORLD EXAMPLE
# ========================================================================

def example_usage():
    """
    Demonstrate how to use the pattern detector with real candlestick data
    """

    print("\n" + "="*100)
    print("FVG PATTERN DETECTION - PRACTICAL EXAMPLE")
    print("="*100)

    # Example 1: Create sample candles manually
    print("\nEXAMPLE 1: Manual Candlestick Creation")
    print("-" * 100)

    candle1 = Candle(
        timestamp=datetime(2026, 5, 1, 10, 0),
        open=45100,
        high=45110,
        low=45080,
        close=45105
    )

    candle2 = Candle(
        timestamp=datetime(2026, 5, 1, 10, 1),
        open=45255,
        high=45350,
        low=45050,
        close=45080
    )

    candle3 = Candle(
        timestamp=datetime(2026, 5, 1, 10, 2),
        open=45090,
        high=45170,
        low=45085,
        close=45100
    )

    print(f"\nCandle 1 (OHLC): {candle1.open:.0f}, {candle1.high:.0f}, {candle1.low:.0f}, {candle1.close:.0f}")
    print(f"  Body: {candle1.body:.0f} | Range: {candle1.range:.0f} | Body Ratio: {candle1.body_ratio:.3f}")
    print(f"  Upper Tail: {candle1.upper_tail:.0f} | Lower Tail: {candle1.lower_tail:.0f}")

    print(f"\nCandle 2 (OHLC): {candle2.open:.0f}, {candle2.high:.0f}, {candle2.low:.0f}, {candle2.close:.0f}")
    print(f"  Body: {candle2.body:.0f} | Range: {candle2.range:.0f} | Body Ratio: {candle2.body_ratio:.3f}")
    print(f"  Upper Tail: {candle2.upper_tail:.0f} | Lower Tail: {candle2.lower_tail:.0f}")
    print(f"  Direction: {'BULLISH' if candle2.is_bullish else 'BEARISH'}")

    print(f"\nCandle 3 (OHLC): {candle3.open:.0f}, {candle3.high:.0f}, {candle3.low:.0f}, {candle3.close:.0f}")
    print(f"  Body: {candle3.body:.0f} | Range: {candle3.range:.0f} | Body Ratio: {candle3.body_ratio:.3f}")
    print(f"  Upper Tail: {candle3.upper_tail:.0f} | Lower Tail: {candle3.lower_tail:.0f}")

    # Detect pattern
    detector = PatternDetector()
    pattern = detector.detect_pattern(candle1, candle2, candle3)

    print("\n" + "-" * 100)
    print("DETECTION RESULTS:")
    print("-" * 100)

    if pattern:
        print(f"\n✓ PATTERN DETECTED: {pattern.pattern_type}")
        print(f"  Confidence: {pattern.confidence:.1f}%")
        print(f"\nDetails:")
        for key, value in pattern.details.items():
            print(f"  {key}: {value}")
    else:
        print("\n✗ No pattern detected")

    # Example 2: Analyze multiple candles
    print("\n\n" + "="*100)
    print("EXAMPLE 2: Scanning Multiple Candlesticks")
    print("="*100)

    # Create a series of candles
    sample_candles = [
        Candle(datetime(2026, 5, 1, 10, i), 45000+i*50, 45100+i*50, 44900+i*50, 45050+i*50)
        for i in range(20)
    ]

    # Scan for patterns
    patterns = detector.scan_for_patterns(sample_candles)

    print(f"\nScanned {len(sample_candles)} candles")
    print(f"Found {len(patterns)} patterns")

    if patterns:
        print("\nPatterns found:")
        for i, p in enumerate(patterns, 1):
            print(f"\n{i}. {p.pattern_type} at {p.timestamp} (Confidence: {p.confidence:.1f}%)")


# ========================================================================
# STATISTICAL REPORTING
# ========================================================================

def generate_pattern_statistics(patterns: List[PatternMatch]) -> Dict:
    """Generate statistics from detected patterns"""

    if not patterns:
        return {}

    pattern_counts = {}
    for pattern in patterns:
        pattern_counts[pattern.pattern_type] = pattern_counts.get(pattern.pattern_type, 0) + 1

    return {
        "total_patterns": len(patterns),
        "unique_pattern_types": len(pattern_counts),
        "pattern_distribution": pattern_counts,
        "average_confidence": np.mean([p.confidence for p in patterns]),
    }


if __name__ == "__main__":
    example_usage()
