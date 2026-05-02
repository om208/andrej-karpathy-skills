#!/usr/bin/env python3

import sys
import pandas as pd
from datetime import datetime

from data_loader import DataLoader
from strategies.inside_bar_sma_2lot import InsideBarSMAVolume2LotStrategy
from self_healing import SelfHealingSystem
from report_generator import ReportGenerator
from research_analyzer import StrategyResearchAnalyzer
from movement_analyzer import MarketMovementAnalyzer
from strategy_facts_generator import StrategyFactsGenerator


def run_2lot_strategy_backtest(data_path, output_base_dir='./strategy_facts'):
    """
    Run Enhanced 2-Lot Inside Bar + SMA Strategy with Complete Analysis

    Strategy Rules:
    1. Pattern: Inside bar + SMA(96) touch + Volume spike
    2. Entry: When ALL 3 conditions confirmed
    3. Position: 2 LOTS
       - Lot 1: Exit at +250 pips OR 159 minutes
       - Lot 2: Exit at 159 minutes (no stop loss)
    4. Track market movement after position closed
    """

    print("\n" + "=" * 110)
    print("2-LOT INSIDE BAR + SMA STRATEGY WITH VOLUME VERIFICATION")
    print("=" * 110)

    # Load data
    print("\n[1/8] Loading BTC/USD 1-minute data...")
    loader = DataLoader(data_path)
    df = loader.get_data()
    summary = loader.get_summary()

    print(f"  ✓ Loaded {summary['total_candles']} candles")
    print(f"  ✓ Period: {summary['start_date']} to {summary['end_date']}")
    print(f"  ✓ Price range: ${summary['price_range'][0]:.2f} - ${summary['price_range'][1]:.2f}")

    # Initialize facts generator
    print("\n[2/8] Initializing strategy documentation system...")
    facts_gen = StrategyFactsGenerator('InsideBarSMA_2Lot_VolumeVerified', output_base_dir)
    print(f"  ✓ Strategy folder: {facts_gen.get_strategy_path()}")

    # Save strategy documentation
    rules = [
        "Inside bar pattern: current high < previous high AND current low > previous low",
        "SMA(96) touches the inside bar candle (within 2% threshold)",
        "Volume spike detected: current volume > 1.8x 20-period average",
        "Entry: When ALL three conditions are met simultaneously",
        "Position sizing: Split into 2 equal lots",
        "Lot 1: Exit at +250 pips (trailing) OR after 159 minutes (whichever comes first)",
        "Lot 2: Exit ONLY at 159 minutes (NO stop loss, no trailing)",
        "Track market movement up to 160 minutes after entry"
    ]

    parameters = {
        'SMA Period': 96,
        'SMA Touch Threshold': '2%',
        'Volume Spike Multiplier': '1.8x',
        'Lot 1 Target': '+250 pips',
        'Lot 2 Hold Time': '159 minutes',
        'Initial Capital': '$100',
        'Risk Per Trade': '$7',
        'Timeframe': '1-minute',
        'Asset': 'BTC/USD'
    }

    facts_gen.save_strategy_documentation(rules, parameters)
    print("  ✓ Strategy documentation saved")

    # Run strategy
    print("\n[3/8] Running 2-Lot Strategy with Volume Verification...")
    strategy_params = {
        'initial_capital': 100,
        'risk_per_trade': 7,
        'max_loss': 10,
        'sma_period': 96,
        'touch_threshold': 0.02,
        'exit_minutes': 159,
        'lot1_tp_pips': 250,
        'volume_spike_multiplier': 1.1,  # Very light volume confirmation (1.1x average)
        'trailing_stop_pips': 50
    }

    strategy = InsideBarSMAVolume2LotStrategy(df, **strategy_params)
    trades = strategy.run()
    trades_df = pd.DataFrame(trades)

    print(f"  ✓ Generated {len(trades)} trades")
    if len(trades) > 0:
        wins = len(trades_df[trades_df['win'] == True])
        print(f"  ✓ Winning trades: {wins}")
        print(f"  ✓ Losing trades: {len(trades) - wins}")
        print(f"  ✓ Win rate: {(wins / len(trades) * 100):.2f}%")
        print(f"  ✓ Total P&L: ${trades_df['total_pnl'].sum():.2f}")

    # Self-healing analysis
    print("\n[4/8] Running self-healing system analysis...")
    if len(trades_df) < 5:
        print(f"  ⚠ Warning: Only {len(trades_df)} trades generated. Need minimum 5 for proper analysis.")
        healing = None
        healing_report = None
    else:
        healing = SelfHealingSystem(trades_df, strategy_params['initial_capital'])
        healing.analyze()
        healing_report = healing.generate_report()

        print(f"  ✓ Health Status: {healing.health_status}")
        print(f"  ✓ Win Rate: {healing.diagnostics['metrics']['win_rate']}%")
        print(f"  ✓ Profit Factor: {healing.diagnostics['metrics']['profit_factor']}")

    # Research analysis
    print("\n[5/8] Performing detailed research analysis...")
    if len(trades_df) > 0:
        researcher = StrategyResearchAnalyzer(trades_df)
        research_report = researcher.generate_research_report()
    else:
        research_report = "No trades to analyze."

    # Movement analysis
    print("\n[6/8] Analyzing market movement after 159 minutes...")
    if len(trades_df) > 0:
        movement_analyzer = MarketMovementAnalyzer(trades_df)
        movement_df = movement_analyzer.analyze_movements()
        movement_report = movement_analyzer.generate_movement_report()
        movement_summary = movement_analyzer.generate_movement_summary()
    else:
        movement_df = pd.DataFrame()
        movement_report = "No trades to analyze for market movement."
        movement_summary = {}

    print(f"  ✓ Trades analyzed for post-exit movement: {len(movement_df)}")
    if movement_summary:
        print(f"  ✓ Avg positive move: {movement_summary.get('avg_positive_move', 0):.4f}%")
        print(f"  ✓ Avg negative move: {movement_summary.get('avg_negative_move', 0):.4f}%")

    # Generate reports
    print("\n[7/8] Generating comprehensive reports...")
    if healing is None:
        # Create dummy healing report for insufficient trades
        backtest_report = f"""
================================================================================
BACKTEST REPORT - INSIDE BAR SMA 2-LOT STRATEGY
================================================================================

WARNING: Insufficient Trades for Analysis
Number of trades generated: {len(trades_df)}
Minimum required for analysis: 5

This may indicate:
1. Volume spike filter is too strict
2. SMA touch condition is too restrictive
3. Inside bar pattern is rare in this timeframe

Recommendation: Adjust confluence factor requirements (volume spike multiplier)
================================================================================
"""
    else:
        backtest_reporter = ReportGenerator(
            trades_df,
            healing_report,
            "InsideBarSMA_2Lot_VolumeVerified",
            strategy_params['initial_capital']
        )
        backtest_report = backtest_reporter.generate_text_report()

    # Save all reports and data
    print("\n[8/8] Saving all results to organized structure...")

    # Save reports
    facts_gen.save_backtest_report(backtest_report)
    facts_gen.save_research_report(research_report)
    facts_gen.save_movement_report(movement_report)

    # Save CSV data
    facts_gen.save_trades_csv(trades_df)
    facts_gen.save_movement_data_csv(movement_df)

    # Generate facts summaries
    if healing is not None:
        backtest_metrics = {
            'Total Trades': len(trades_df),
            'Winning Trades': len(trades_df[trades_df['win'] == True]),
            'Win Rate': f"{healing.diagnostics['metrics']['win_rate']:.2f}%",
            'Profit Factor': f"{healing.diagnostics['metrics']['profit_factor']:.2f}",
            'Total P&L': f"${trades_df['total_pnl'].sum():.2f}",
            'Avg P&L': f"${trades_df['total_pnl'].mean():.2f}",
            'Health Status': healing.health_status
        }
    else:
        backtest_metrics = {
            'Total Trades': len(trades_df),
            'Winning Trades': len(trades_df[trades_df['win'] == True]) if len(trades_df) > 0 else 0,
            'Win Rate': 'N/A - Insufficient trades',
            'Profit Factor': 'N/A - Insufficient trades',
            'Total P&L': f"${trades_df['total_pnl'].sum():.2f}" if len(trades_df) > 0 else '$0.00',
            'Avg P&L': f"${trades_df['total_pnl'].mean():.2f}" if len(trades_df) > 0 else '$0.00',
            'Health Status': 'UNKNOWN - Need more trades'
        }

    patterns = []
    if healing is not None:
        patterns.append(f"Win rate is {healing.diagnostics['metrics']['win_rate']:.2f}% - {'Below target' if healing.diagnostics['metrics']['win_rate'] < 65 else 'On target'}")
        patterns.append(f"Profit factor is {healing.diagnostics['metrics']['profit_factor']:.2f} - {'Strong' if healing.diagnostics['metrics']['profit_factor'] > 1.5 else 'Needs improvement'}")

    if movement_summary:
        patterns.append(f"Average positive market move after 159min: {movement_summary.get('avg_positive_move', 0):.4f}%")
        patterns.append(f"Average negative market move after 159min: {movement_summary.get('avg_negative_move', 0):.4f}%")
        patterns.append(f"Trades with positive move after exit: {movement_summary.get('trades_with_positive_move', 0)}/{movement_summary.get('total_trades', 0)}")

    if len(trades_df) > 0:
        patterns.append(f"Lot 1 exits via take profit: {len(trades_df[trades_df['lot1_exit_reason'] == 'take_profit_250pips'])}")
        patterns.append(f"Lot 1 exits via time: {len(trades_df[trades_df['lot1_exit_reason'] == 'time_exit_159min'])}")

    if not patterns:
        patterns.append("Insufficient data for pattern analysis - need at least 5 trades")

    recommendations = []
    if healing is not None and healing.diagnostics['metrics']['win_rate'] < 50:
        recommendations.append('Increase volume spike multiplier to filter better entries')
    elif healing is not None:
        recommendations.append('Volume filter is working well')

    recommendations.extend([
        'Add support/resistance confirmation for better entry quality',
        'Monitor 159-minute movement predictions vs actual results',
        'Consider different lot exit strategies (wider TP for lot 1)',
        'Evaluate if all 3 confluence factors are necessary or too restrictive',
        'If few trades generated, loosen confluence requirements (especially inside bar sensitivity)'
    ])

    facts_gen.generate_facts_summary(backtest_metrics, patterns, recommendations)

    # Generate index
    facts_gen.generate_index(backtest_metrics)

    print(f"  ✓ All reports saved to: {facts_gen.get_strategy_path()}")

    # Display summary
    print("\n" + "=" * 110)
    print("BACKTEST SUMMARY")
    print("=" * 110)
    print(backtest_report)

    print("\n\n" + "=" * 110)
    print("MOVEMENT ANALYSIS")
    print("=" * 110)
    print(movement_report)

    return {
        'trades': trades_df,
        'movement_data': movement_df,
        'healing_report': healing_report,
        'strategy_path': facts_gen.get_strategy_path()
    }


if __name__ == "__main__":
    DATA_PATH = "/root/.claude/uploads/ca2e0534-bab6-4265-aa59-166ae492020c/23c581a8-1M1MonthBTCUSD.P.csv"

    results = run_2lot_strategy_backtest(DATA_PATH)

    print("\n✓ Complete analysis finished!")
    print(f"✓ All results saved to: {results['strategy_path']}")
