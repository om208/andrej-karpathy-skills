"""
Configuration Manager for TradingView Strategy Testing
Manages all settings, parameters, and expected results
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class StrategySettings:
    """Pine Script strategy configuration"""
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

    show_debug_logs: bool = True
    highlight_entry_signals: bool = True
    highlight_exit_points: bool = True
    show_compression_ratio: bool = True


@dataclass
class BacktestConfig:
    """Backtest parameters"""
    instrument: str = "BTCUSD"
    timeframe: str = "1"  # 1-minute
    start_date: str = "2026-02-26"
    end_date: str = "2026-03-10"
    description: str = "BTC/USD 1-minute candles"


@dataclass
class ExpectedResults:
    """Expected backtest results for validation"""
    # Without filtering
    baseline_win_rate: float = 50.96
    baseline_trades: int = 104
    baseline_total_pnl: float = -1058.57
    baseline_avg_pnl: float = -10.18

    # With filtering (Risk Score = 0)
    filtered_win_rate: float = 85.19
    filtered_trades: int = 27
    filtered_total_pnl: float = 4108.12
    filtered_avg_pnl: float = 152.15

    # Tolerance levels for validation
    win_rate_tolerance_pct: float = 1.0  # ±1%
    trade_count_tolerance: int = 2       # ±2 trades
    pnl_tolerance: float = 50.0          # ±$50


@dataclass
class CompressionAnalysis:
    """Expected compression ratio analysis"""
    very_tight_min: float = 0.20
    very_tight_max: float = 0.35
    very_tight_label: str = "Very Tight (BAD)"
    very_tight_expected_wr: float = 61.5

    tight_min: float = 0.35
    tight_max: float = 0.50
    tight_label: str = "Tight (GOOD)"
    tight_expected_wr: float = 58.6

    medium_min: float = 0.50
    medium_max: float = 0.65
    medium_label: str = "Medium (BAD)"
    medium_expected_wr: float = 41.4


class Config:
    """Central configuration manager"""

    # Strategy settings
    STRATEGY = StrategySettings()

    # Backtest configuration
    BACKTEST = BacktestConfig()

    # Expected results for validation
    EXPECTED = ExpectedResults()

    # Compression analysis
    COMPRESSION = CompressionAnalysis()

    # TradingView URLs
    TRADINGVIEW_BASE_URL = "https://www.tradingview.com"
    TRADINGVIEW_CHART_URL = "https://www.tradingview.com/chart/?symbol=BTCUSD"
    PINE_EDITOR_URL = "https://www.tradingview.com/pine-editor/"

    # Element selectors (CSS/XPath for browser automation)
    SELECTORS = {
        # Authentication
        "email_input": "input[type='email']",
        "password_input": "input[type='password']",
        "login_button": "button:contains('Sign In')",

        # Pine Editor
        "new_script_button": "button:contains('New')",
        "script_title_input": "input[placeholder*='Script name']",
        "script_content_area": "div.editor-content",
        "save_button": "button:contains('Save')",

        # Chart
        "add_to_chart_button": "button:contains('Add to Chart')",
        "strategy_settings": "button:contains('Settings')",

        # Backtest
        "backtest_tab": "button:contains('Backtest')",
        "run_backtest_button": "button:contains('Run')",
        "date_range_start": "input[placeholder*='From']",
        "date_range_end": "input[placeholder*='To']",

        # Results
        "win_rate_display": "span:contains('Win Rate')",
        "total_trades_display": "span:contains('Total Trades')",
        "pnl_display": "span:contains('Net Profit')",
    }

    # Timeouts (seconds)
    TIMEOUTS = {
        "page_load": 30,
        "element_visibility": 10,
        "backtest_completion": 120,
        "screenshot": 2,
    }

    # Retry configuration
    RETRIES = {
        "max_attempts": 3,
        "wait_between_attempts": 2,  # seconds
    }

    @staticmethod
    def get_strategy_dict() -> Dict[str, Any]:
        """Get strategy settings as dictionary"""
        return {
            'initial_capital': Config.STRATEGY.initial_capital,
            'risk_per_trade': Config.STRATEGY.risk_per_trade,
            'lot_size_percent': Config.STRATEGY.lot_size_percent,
            'sma_period': Config.STRATEGY.sma_period,
            'sma_touch_threshold_pct': Config.STRATEGY.sma_touch_threshold_pct,
            'lot1_tp_pips': Config.STRATEGY.lot1_tp_pips,
            'lot2_hold_minutes': Config.STRATEGY.lot2_hold_minutes,
            'enable_risk_filtering': Config.STRATEGY.enable_risk_filtering,
            'filter_verytight_compression': Config.STRATEGY.filter_verytight_compression,
            'filter_medium_compression': Config.STRATEGY.filter_medium_compression,
            'max_acceptable_risk_score': Config.STRATEGY.max_acceptable_risk_score,
        }

    @staticmethod
    def get_backtest_config_dict() -> Dict[str, Any]:
        """Get backtest configuration as dictionary"""
        return {
            'instrument': Config.BACKTEST.instrument,
            'timeframe': Config.BACKTEST.timeframe,
            'start_date': Config.BACKTEST.start_date,
            'end_date': Config.BACKTEST.end_date,
        }

    @staticmethod
    def validate_results_against_expected(actual_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate actual backtest results against expected results
        Returns validation report
        """
        report = {
            'status': 'PASSED',
            'issues': [],
            'details': {}
        }

        # Check win rate
        actual_wr = actual_results.get('win_rate', 0)
        expected_wr = Config.EXPECTED.filtered_win_rate
        tolerance = Config.EXPECTED.win_rate_tolerance_pct

        if abs(actual_wr - expected_wr) > tolerance:
            report['status'] = 'FAILED'
            report['issues'].append(
                f"Win rate mismatch: expected {expected_wr:.2f}%, "
                f"got {actual_wr:.2f}%"
            )

        report['details']['win_rate'] = {
            'expected': expected_wr,
            'actual': actual_wr,
            'tolerance': tolerance,
            'status': 'PASS' if abs(actual_wr - expected_wr) <= tolerance else 'FAIL'
        }

        # Check trade count
        actual_trades = actual_results.get('total_trades', 0)
        expected_trades = Config.EXPECTED.filtered_trades
        trade_tolerance = Config.EXPECTED.trade_count_tolerance

        if abs(actual_trades - expected_trades) > trade_tolerance:
            report['status'] = 'FAILED'
            report['issues'].append(
                f"Trade count mismatch: expected {expected_trades}, "
                f"got {actual_trades}"
            )

        report['details']['trades'] = {
            'expected': expected_trades,
            'actual': actual_trades,
            'tolerance': trade_tolerance,
            'status': 'PASS' if abs(actual_trades - expected_trades) <= trade_tolerance else 'FAIL'
        }

        # Check P&L
        actual_pnl = actual_results.get('total_pnl', 0)
        expected_pnl = Config.EXPECTED.filtered_total_pnl
        pnl_tolerance = Config.EXPECTED.pnl_tolerance

        if abs(actual_pnl - expected_pnl) > pnl_tolerance:
            report['status'] = 'FAILED'
            report['issues'].append(
                f"P&L mismatch: expected ${expected_pnl:.2f}, "
                f"got ${actual_pnl:.2f}"
            )

        report['details']['pnl'] = {
            'expected': expected_pnl,
            'actual': actual_pnl,
            'tolerance': pnl_tolerance,
            'status': 'PASS' if abs(actual_pnl - expected_pnl) <= pnl_tolerance else 'FAIL'
        }

        return report


if __name__ == '__main__':
    # Test configuration
    print("Strategy Settings:")
    print(f"  SMA Period: {Config.STRATEGY.sma_period}")
    print(f"  TP: {Config.STRATEGY.lot1_tp_pips} pips")
    print(f"  Hold Time: {Config.STRATEGY.lot2_hold_minutes} minutes")
    print(f"  Risk Filtering: {Config.STRATEGY.enable_risk_filtering}")

    print("\nBacktest Config:")
    print(f"  Instrument: {Config.BACKTEST.instrument}")
    print(f"  Timeframe: {Config.BACKTEST.timeframe}-minute")
    print(f"  Date Range: {Config.BACKTEST.start_date} to {Config.BACKTEST.end_date}")

    print("\nExpected Results:")
    print(f"  Win Rate: {Config.EXPECTED.filtered_win_rate}%")
    print(f"  Trades: {Config.EXPECTED.filtered_trades}")
    print(f"  P&L: ${Config.EXPECTED.filtered_total_pnl:.2f}")

    print("\n✓ Configuration loaded successfully")
