#!/usr/bin/env python3

import sys
import pandas as pd
from datetime import datetime

from data_loader import DataLoader
from strategies.support_resistance import SupportResistanceStrategy
from self_healing import SelfHealingSystem
from report_generator import ReportGenerator


def run_backtest(data_path, strategy_class, strategy_params, output_dir='./reports'):
    """
    Run complete backtesting with self-healing analysis

    Args:
        data_path: Path to CSV data file
        strategy_class: Strategy class to use
        strategy_params: Dict of strategy parameters
        output_dir: Directory to save reports
    """

    print("\n" + "=" * 80)
    print("BACKTESTING ENGINE - SELF-HEALING TRADING SYSTEM")
    print("=" * 80)

    # 1. Load data
    print("\n[1/5] Loading data...")
    loader = DataLoader(data_path)
    df = loader.get_data()
    summary = loader.get_summary()

    print(f"  ✓ Loaded {summary['total_candles']} candles")
    print(f"  ✓ Period: {summary['start_date']} to {summary['end_date']}")
    print(f"  ✓ Price range: ${summary['price_range'][0]:.2f} - ${summary['price_range'][1]:.2f}")
    print(f"  ✓ Avg volume: {summary['avg_volume']:.0f}")

    # 2. Run strategy
    print(f"\n[2/5] Running {strategy_class.__name__}...")
    strategy = strategy_class(df, **strategy_params)
    trades = strategy.run()

    print(f"  ✓ Generated {len(trades)} trades")
    trades_df = pd.DataFrame(trades)

    # 3. Self-healing analysis
    print("\n[3/5] Running self-healing analysis...")
    healing = SelfHealingSystem(trades_df, strategy_params['initial_capital'])
    healing.analyze()

    print(f"  ✓ Health Status: {healing.health_status}")
    print(f"  ✓ Win Rate: {healing.diagnostics['metrics']['win_rate']}%")
    print(f"  ✓ Profit Factor: {healing.diagnostics['metrics']['profit_factor']}")
    print(f"  ✓ Total P&L: ${healing.diagnostics['metrics']['total_pnl']:.2f}")

    if healing.corrections:
        print(f"  ⚠ Found {len(healing.corrections)} correction(s)")

    # 4. Generate report
    print("\n[4/5] Generating report...")
    healing_report = healing.generate_report()
    reporter = ReportGenerator(
        trades_df,
        healing_report,
        strategy_class.__name__,
        strategy_params['initial_capital']
    )

    report_path = reporter.save_report(f"{output_dir}/backtest_report.txt")
    print(f"  ✓ Report saved to: {report_path}")

    # 5. Display summary
    print("\n[5/5] Summary")
    print(reporter.generate_text_report())

    return {
        'trades': trades_df,
        'healing_report': healing_report,
        'report_path': report_path
    }


if __name__ == "__main__":
    # Configuration
    DATA_PATH = "/root/.claude/uploads/ca2e0534-bab6-4265-aa59-166ae492020c/23c581a8-1M1MonthBTCUSD.P.csv"

    STRATEGY_PARAMS = {
        'initial_capital': 100,
        'risk_per_trade': 7,
        'max_loss': 10,
        'support_lookback': 20,
        'volume_threshold': 1.5,
        'rsi_oversold': 30,
        'rsi_overbought': 70,
        'tp_atr_multiplier': 1.5
    }

    # Run backtest
    results = run_backtest(
        DATA_PATH,
        SupportResistanceStrategy,
        STRATEGY_PARAMS,
        output_dir='./reports'
    )

    print("\n✓ Backtest complete!")
