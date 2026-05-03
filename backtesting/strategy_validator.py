"""
Pine Script Strategy Validator - Python Implementation
Inside Bar + SMA(196) with Inverse Filtering - 85% Win Rate

This module replicates the exact logic of the TradingView Pine Script strategy
in Python for offline testing and validation.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta


@dataclass
class StrategyConfig:
    """Strategy parameters - must match TradingView settings exactly"""
    initial_capital: float = 100.0
    risk_per_trade: float = 7.0
    lot_size_percent: float = 0.35

    sma_period: int = 196
    sma_touch_threshold_pct: float = 2.0

    lot1_tp_pips: int = 250
    lot2_hold_minutes: int = 159

    enable_risk_filtering: bool = True
    filter_verytight_compression: bool = True
    filter_medium_compression: bool = True
    max_acceptable_risk_score: int = 0

    min_compression_ratio: float = 0.0
    max_compression_ratio: float = 1.0


@dataclass
class Signal:
    """Signal detection result"""
    bar_index: int
    timestamp: datetime
    inside_bar: bool
    compression_ratio: float
    sma_value: float
    sma_touches: bool
    signal_detected: bool
    risk_score: int
    entry_decision: bool


@dataclass
class Position:
    """Active position tracking"""
    entry_bar: int
    entry_time: datetime
    entry_price: float
    lot1_active: bool = True
    lot2_active: bool = True
    lot1_closed: bool = False
    lot2_closed: bool = False
    lot1_exit_price: Optional[float] = None
    lot2_exit_price: Optional[float] = None
    lot1_exit_reason: str = ""
    lot2_exit_reason: str = ""
    lot1_pnl: float = 0.0
    lot2_pnl: float = 0.0

    @property
    def total_pnl(self) -> float:
        return self.lot1_pnl + self.lot2_pnl

    @property
    def is_closed(self) -> bool:
        return self.lot1_closed and self.lot2_closed


@dataclass
class Trade:
    """Completed trade record"""
    entry_bar: int
    entry_time: datetime
    entry_price: float
    lot1_exit_bar: int
    lot1_exit_time: datetime
    lot1_exit_price: float
    lot1_exit_reason: str
    lot2_exit_bar: int
    lot2_exit_time: datetime
    lot2_exit_price: float
    lot2_exit_reason: str
    lot1_pnl: float
    lot2_pnl: float
    total_pnl: float
    is_win: bool


class StrategyValidator:
    """
    Validates the Inside Bar + SMA(196) strategy logic.
    Replicates Pine Script behavior exactly.
    """

    def __init__(self, config: StrategyConfig = None):
        self.config = config or StrategyConfig()
        self.signals: List[Signal] = []
        self.positions: List[Position] = []
        self.trades: List[Trade] = []
        self.current_position: Optional[Position] = None

    def calculate_sma(self, closes: np.ndarray, period: int, bar_index: int) -> Optional[float]:
        """Calculate SMA(period) at bar_index"""
        if bar_index < period - 1:
            return None
        return np.mean(closes[bar_index - period + 1:bar_index + 1])

    def detect_inside_bar(self, current_high: float, current_low: float,
                         prev_high: float, prev_low: float) -> Tuple[bool, float]:
        """
        Detect inside bar pattern.
        Inside bar: current_high < prev_high AND current_low > prev_low

        Returns: (is_inside_bar, compression_ratio)
        """
        is_inside = (current_high < prev_high) and (current_low > prev_low)

        current_range = current_high - current_low
        prev_range = prev_high - prev_low

        compression = current_range / prev_range if prev_range > 0 else 0.0

        return is_inside, compression

    def detect_sma_touch(self, sma_value: float, current_high: float,
                        current_low: float, threshold_pct: float) -> bool:
        """
        Detect if SMA touches the candle.
        Touch: SMA is within threshold_pct of candle range
        """
        if sma_value is None:
            return False

        candle_range = current_high - current_low
        threshold = candle_range * (threshold_pct / 100.0)

        sma_touches = (sma_value >= current_low - threshold) and \
                      (sma_value <= current_high + threshold)

        return sma_touches

    def calculate_risk_score(self, compression_ratio: float, current_open: float,
                            current_close: float, current_high: float,
                            current_low: float) -> int:
        """
        Calculate risk score based on pattern characteristics.

        Characteristics:
        1. Very tight compression (0.20-0.35) → +1 point
        2. Medium compression (0.50-0.65) → +1 point
        3. Downward post-entry movement → +1 point

        Score 0 = SAFE (85% win rate)
        Score >= 1 = RISKY (skip)
        """
        risk_score = 0

        # Characteristic 1: Very tight compression
        if self.config.filter_verytight_compression:
            if 0.20 <= compression_ratio < 0.35:
                risk_score += 1

        # Characteristic 2: Medium compression
        if self.config.filter_medium_compression:
            if 0.50 <= compression_ratio <= 0.65:
                risk_score += 1

        # Characteristic 3: Downward post-entry movement heuristic
        # If close < open and close near low, indicates downward pressure
        candle_range = current_high - current_low
        if candle_range > 0:
            close_position = current_close - current_low
            if (current_close < current_open) and (close_position < candle_range * 0.3):
                risk_score += 1

        return risk_score

    def process_candle(self, bar_index: int, timestamp: datetime,
                      open_: float, high: float, low: float, close: float,
                      closes: np.ndarray) -> Signal:
        """
        Process a single candle for signal detection.
        """
        # Get previous candle values
        if bar_index == 0:
            prev_high, prev_low = high, low
        else:
            prev_high = closes.index.get_level_values('high')[bar_index - 1] if hasattr(closes, 'index') else high
            prev_low = closes.index.get_level_values('low')[bar_index - 1] if hasattr(closes, 'index') else low

        # Inside bar detection
        is_inside_bar, compression_ratio = self.detect_inside_bar(high, low, prev_high, prev_low)

        # SMA calculation
        sma_value = self.calculate_sma(closes, self.config.sma_period, bar_index)

        # SMA touch detection
        sma_touches = self.detect_sma_touch(sma_value, high, low,
                                           self.config.sma_touch_threshold_pct)

        # Signal generation (both conditions required)
        signal_detected = is_inside_bar and sma_touches

        # Risk score calculation
        risk_score = 0
        if signal_detected:
            risk_score = self.calculate_risk_score(compression_ratio, open_, close, high, low)

        # Entry decision
        entry_decision = signal_detected and (risk_score <= self.config.max_acceptable_risk_score)

        signal = Signal(
            bar_index=bar_index,
            timestamp=timestamp,
            inside_bar=is_inside_bar,
            compression_ratio=compression_ratio,
            sma_value=sma_value or 0.0,
            sma_touches=sma_touches,
            signal_detected=signal_detected,
            risk_score=risk_score,
            entry_decision=entry_decision
        )

        return signal

    def process_position_exits(self, bar_index: int, timestamp: datetime,
                              high: float, low: float, close: float,
                              timeframe_minutes: int = 1) -> None:
        """
        Check for position exits (Lot 1 and Lot 2).
        """
        if self.current_position is None:
            return

        bars_held = bar_index - self.current_position.entry_bar
        time_held_minutes = bars_held * timeframe_minutes

        # Lot 1 exit conditions
        if self.current_position.lot1_active and not self.current_position.lot1_closed:
            # Condition A: Take profit (+250 pips)
            tp_price = self.current_position.entry_price + (self.config.lot1_tp_pips * 0.0001)

            if high >= tp_price:
                self.current_position.lot1_exit_price = tp_price
                self.current_position.lot1_exit_reason = f"TP +{self.config.lot1_tp_pips}pips"
                self.current_position.lot1_pnl = (tp_price - self.current_position.entry_price) * self.config.lot_size_percent * 100000
                self.current_position.lot1_closed = True

            # Condition B: Time exit (159 minutes)
            elif time_held_minutes >= self.config.lot2_hold_minutes:
                self.current_position.lot1_exit_price = close
                self.current_position.lot1_exit_reason = f"Time {self.config.lot2_hold_minutes}min"
                self.current_position.lot1_pnl = (close - self.current_position.entry_price) * self.config.lot_size_percent * 100000
                self.current_position.lot1_closed = True

        # Lot 2 exit condition (time only)
        if self.current_position.lot2_active and not self.current_position.lot2_closed:
            if time_held_minutes >= self.config.lot2_hold_minutes:
                self.current_position.lot2_exit_price = close
                self.current_position.lot2_exit_reason = f"Time {self.config.lot2_hold_minutes}min"
                self.current_position.lot2_pnl = (close - self.current_position.entry_price) * self.config.lot_size_percent * 100000
                self.current_position.lot2_closed = True

        # If both lots closed, record trade and clear position
        if self.current_position.is_closed:
            self._record_trade(bar_index, timestamp)
            self.current_position = None

    def _record_trade(self, exit_bar: int, exit_time: datetime) -> None:
        """Record a completed trade"""
        pos = self.current_position
        trade = Trade(
            entry_bar=pos.entry_bar,
            entry_time=pos.entry_time,
            entry_price=pos.entry_price,
            lot1_exit_bar=exit_bar,
            lot1_exit_time=exit_time,
            lot1_exit_price=pos.lot1_exit_price or 0.0,
            lot1_exit_reason=pos.lot1_exit_reason,
            lot2_exit_bar=exit_bar,
            lot2_exit_time=exit_time,
            lot2_exit_price=pos.lot2_exit_price or 0.0,
            lot2_exit_reason=pos.lot2_exit_reason,
            lot1_pnl=pos.lot1_pnl,
            lot2_pnl=pos.lot2_pnl,
            total_pnl=pos.total_pnl,
            is_win=pos.total_pnl > 0
        )
        self.trades.append(trade)

    def backtest(self, df: pd.DataFrame, timeframe_minutes: int = 1) -> Dict:
        """
        Run complete backtest on OHLC data.

        Args:
            df: DataFrame with columns [timestamp, open, high, low, close]
            timeframe_minutes: Candle timeframe in minutes (1, 5, 15, etc.)

        Returns:
            Dict with backtest results
        """
        self.signals = []
        self.trades = []
        self.current_position = None

        closes = df['close'].values

        for bar_index in range(len(df)):
            row = df.iloc[bar_index]
            timestamp = row['timestamp'] if 'timestamp' in df.columns else datetime.now()

            # Process candle for signal
            signal = self.process_candle(
                bar_index, timestamp,
                row['open'], row['high'], row['low'], row['close'],
                closes
            )
            self.signals.append(signal)

            # Handle entry
            if signal.entry_decision and self.current_position is None:
                self.current_position = Position(
                    entry_bar=bar_index,
                    entry_time=timestamp,
                    entry_price=row['close']
                )

            # Handle exits
            if self.current_position is not None:
                self.process_position_exits(bar_index, timestamp,
                                           row['high'], row['low'], row['close'],
                                           timeframe_minutes)

        return self._generate_results()

    def _generate_results(self) -> Dict:
        """Generate backtest results summary"""
        if not self.trades:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0.0,
                'avg_pnl': 0.0,
                'total_pnl': 0.0,
                'trades': [],
                'signals': self.signals
            }

        total_trades = len(self.trades)
        winning_trades = sum(1 for t in self.trades if t.is_win)
        losing_trades = total_trades - winning_trades
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        total_pnl = sum(t.total_pnl for t in self.trades)
        avg_pnl = total_pnl / total_trades if total_trades > 0 else 0.0

        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_pnl': avg_pnl,
            'total_pnl': total_pnl,
            'trades': self.trades,
            'signals': self.signals
        }

    def get_detailed_report(self) -> str:
        """Generate human-readable detailed report"""
        results = self._generate_results()

        report = f"""
================================================================================
STRATEGY VALIDATOR - DETAILED REPORT
================================================================================

CONFIGURATION:
  SMA Period: {self.config.sma_period}
  SMA Touch Threshold: {self.config.sma_touch_threshold_pct}%
  Lot 1 Take Profit: {self.config.lot1_tp_pips} pips
  Lot 2 Hold Time: {self.config.lot2_hold_minutes} minutes
  Risk Filtering: {self.config.enable_risk_filtering}
  Max Risk Score: {self.config.max_acceptable_risk_score}

RESULTS:
  Total Signals Detected: {len(self.signals)}
  Total Signals Entering: {sum(1 for s in self.signals if s.entry_decision)}
  Total Trades: {results['total_trades']}
  Winning Trades: {results['winning_trades']}
  Losing Trades: {results['losing_trades']}
  Win Rate: {results['win_rate']:.2f}%
  Total P&L: ${results['total_pnl']:.2f}
  Avg P&L per Trade: ${results['avg_pnl']:.2f}

================================================================================
"""
        return report


def create_test_dataframe(ohlc_data: List[Dict]) -> pd.DataFrame:
    """Create DataFrame from OHLC data for testing"""
    df = pd.DataFrame(ohlc_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df[['timestamp', 'open', 'high', 'low', 'close']]
