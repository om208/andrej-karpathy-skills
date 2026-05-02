#!/usr/bin/env python3

import sys
import pandas as pd
from datetime import datetime

from data_loader import DataLoader
from strategies.inside_bar_sma import InsideBarSMAStrategy
from self_healing import SelfHealingSystem
from report_generator import ReportGenerator
from research_analyzer import StrategyResearchAnalyzer


def run_inside_bar_backtest(data_path, output_dir='./reports'):
    """
    Run Inside Bar + SMA Strategy backtest with comprehensive analysis

    Strategy Rules:
    1. Detect inside bar pattern
    2. 96-period SMA must touch the inside bar
    3. Entry when both conditions are met
    4. Exit after 159 minutes OR on TP/SL
    5. Market expected to move drastically
    """

    print("\n" + "=" * 100)
    print("INSIDE BAR + SMA STRATEGY BACKTEST WITH RESEARCH ANALYSIS")
    print("=" * 100)

    # 1. Load data
    print("\n[1/6] Loading BTC/USD 1-minute data...")
    loader = DataLoader(data_path)
    df = loader.get_data()
    summary = loader.get_summary()

    print(f"  ✓ Loaded {summary['total_candles']} candles")
    print(f"  ✓ Period: {summary['start_date']} to {summary['end_date']}")
    print(f"  ✓ Price range: ${summary['price_range'][0]:.2f} - ${summary['price_range'][1]:.2f}")
    print(f"  ✓ Avg volume: {summary['avg_volume']:.0f}")

    # 2. Run strategy
    print(f"\n[2/6] Running Inside Bar + SMA Strategy...")
    print("  - Pattern: Inside bar + SMA(96) touch")
    print("  - Entry: When SMA touches inside bar")
    print("  - Exit: After 159 minutes OR TP/SL hit")
    print("  - TP: +150 pips, SL: -50 pips")

    strategy_params = {
        'initial_capital': 100,
        'risk_per_trade': 7,
        'max_loss': 10,
        'sma_period': 96,
        'touch_threshold': 0.02,
        'exit_minutes': 159,
        'tp_pips': 150,
        'sl_pips': 50
    }

    strategy = InsideBarSMAStrategy(df, **strategy_params)
    trades = strategy.run()
    trades_df = pd.DataFrame(trades)

    print(f"  ✓ Generated {len(trades)} trades")
    if len(trades) > 0:
        wins = len(trades_df[trades_df['win'] == True])
        print(f"  ✓ Winning trades: {wins}")
        print(f"  ✓ Losing trades: {len(trades) - wins}")
        print(f"  ✓ Win rate: {(wins / len(trades) * 100):.2f}%")
        print(f"  ✓ Total P&L: ${trades_df['pnl'].sum():.2f}")

    # 3. Self-healing analysis
    print("\n[3/6] Running self-healing system analysis...")
    healing = SelfHealingSystem(trades_df, strategy_params['initial_capital'])
    healing.analyze()

    print(f"  ✓ Health Status: {healing.health_status}")
    print(f"  ✓ Win Rate: {healing.diagnostics['metrics']['win_rate']}%")
    print(f"  ✓ Profit Factor: {healing.diagnostics['metrics']['profit_factor']}")
    if healing.corrections:
        print(f"  ⚠ Found {len(healing.corrections)} correction(s)")

    # 4. Research analysis
    print("\n[4/6] Performing detailed research analysis...")
    researcher = StrategyResearchAnalyzer(trades_df)
    research_report = researcher.generate_research_report()

    # 5. Generate reports
    print("\n[5/6] Generating comprehensive reports...")
    healing_report = healing.generate_report()
    reporter = ReportGenerator(
        trades_df,
        healing_report,
        "InsideBarSMAStrategy",
        strategy_params['initial_capital']
    )

    # Save main backtest report
    backtest_report = reporter.generate_text_report()
    backtest_path = f"{output_dir}/inside_bar_backtest_report.txt"
    with open(backtest_path, 'w') as f:
        f.write(backtest_report)
    print(f"  ✓ Backtest report saved: {backtest_path}")

    # Save research report
    research_path = f"{output_dir}/inside_bar_research_analysis.txt"
    with open(research_path, 'w') as f:
        f.write(research_report)
    print(f"  ✓ Research report saved: {research_path}")

    # 6. Display summary
    print("\n[6/6] Displaying results...\n")
    print(backtest_report)
    print("\n\n")
    print(research_report)

    return {
        'trades': trades_df,
        'healing_report': healing_report,
        'backtest_path': backtest_path,
        'research_path': research_path
    }


if __name__ == "__main__":
    DATA_PATH = "/root/.claude/uploads/ca2e0534-bab6-4265-aa59-166ae492020c/23c581a8-1M1MonthBTCUSD.P.csv"

    results = run_inside_bar_backtest(DATA_PATH, output_dir='./reports')

    print("\n✓ Analysis complete!")
    print(f"Reports saved to ./reports/")
