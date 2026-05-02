#!/usr/bin/env python3

import sys
import pandas as pd

from data_loader import DataLoader
from strategies.inside_bar_sma_2lot_v3 import InsideBarSMA2LotV3Strategy
from self_healing import SelfHealingSystem
from report_generator import ReportGenerator
from research_analyzer import StrategyResearchAnalyzer
from movement_analyzer import MarketMovementAnalyzer
from strategy_facts_generator import StrategyFactsGenerator


print("\n" + "=" * 110)
print("2-LOT INSIDE BAR + SMA(196) STRATEGY V3 - WITH VOLUME VERIFICATION")
print("=" * 110)

# Load data
print("\n[1/8] Loading BTC/USD 1-minute data...")
loader = DataLoader("/root/.claude/uploads/ca2e0534-bab6-4265-aa59-166ae492020c/23c581a8-1M1MonthBTCUSD.P.csv")
df = loader.get_data()
print(f"  ✓ Loaded {len(df)} candles")

# Initialize facts generator
facts_gen = StrategyFactsGenerator('InsideBarSMA_2Lot_SMA196_Final', './strategy_facts')

# Save documentation
rules = [
    "Inside bar pattern: current candle within previous candle range",
    "SMA(196) touches the inside bar (within 2% threshold)",
    "Volume confirmation: current volume > 1.5x 20-period average",
    "Entry: ALL three conditions must be met simultaneously",
    "Position: Split into 2 equal lots",
    "Lot 1: Exit at +250 pips OR after 159 minutes (whichever comes first)",
    "Lot 2: Exit ONLY at 159 minutes (NO stop loss, no trailing)",
    "Track market movement up to 160 minutes after exit",
    "NO fixed stop loss on either lot - risk managed via lot structure"
]

parameters = {
    'SMA Period': 196,
    'SMA Touch Threshold': '2%',
    'Volume Threshold': '1.5x average',
    'Lot 1 Target': '+250 pips',
    'Hold Time': '159 minutes',
    'Initial Capital': '$100',
    'Risk Per Trade': '$7',
    'Max Loss': '$10',
    'Timeframe': '1-minute',
    'Asset': 'BTC/USD'
}

facts_gen.save_strategy_documentation(rules, parameters)
print("  ✓ Documentation saved")

# Run strategy
print("\n[2/8] Running 2-Lot Strategy with SMA(196)...")
strategy_params = {
    'initial_capital': 100,
    'risk_per_trade': 7,
    'max_loss': 10,
    'sma_period': 196,
    'touch_threshold': 0.02,
    'exit_minutes': 159,
    'lot1_tp_pips': 250,
    'volume_threshold': 1.5
}

strategy = InsideBarSMA2LotV3Strategy(df, **strategy_params)
trades = strategy.run()
trades_df = pd.DataFrame(trades)

print(f"  ✓ Generated {len(trades_df)} trades")
if len(trades_df) > 0:
    wins = len(trades_df[trades_df['win'] == True])
    print(f"  ✓ Winning trades: {wins}")
    print(f"  ✓ Losing trades: {len(trades_df) - wins}")
    print(f"  ✓ Win rate: {(wins / len(trades_df) * 100):.2f}%")
    print(f"  ✓ Total P&L: ${trades_df['total_pnl'].sum():.2f}")

# Self-healing
print("\n[3/8] Running self-healing analysis...")
if len(trades_df) >= 5:
    healing = SelfHealingSystem(trades_df, 100)
    healing.analyze()
    healing_report = healing.generate_report()
    print(f"  ✓ Health Status: {healing.health_status}")
    print(f"  ✓ Win Rate: {healing.diagnostics['metrics']['win_rate']}%")
    print(f"  ✓ Profit Factor: {healing.diagnostics['metrics']['profit_factor']}")
else:
    healing = None
    healing_report = None
    print(f"  ⚠ Only {len(trades_df)} trades - insufficient for analysis")

# Research analysis
print("\n[4/8] Analyzing trades...")
if len(trades_df) > 0:
    researcher = StrategyResearchAnalyzer(trades_df)
    research_report = researcher.generate_research_report()
else:
    research_report = "No trades to analyze."

# Movement analysis
print("\n[5/8] Analyzing market movement...")
if len(trades_df) > 0:
    movement_analyzer = MarketMovementAnalyzer(trades_df)
    movement_df = movement_analyzer.analyze_movements()
    movement_report = movement_analyzer.generate_movement_report()
else:
    movement_df = pd.DataFrame()
    movement_report = "No trades to analyze."

# Save reports
print("\n[6/8] Saving reports...")
if healing is not None:
    backtest_reporter = ReportGenerator(trades_df, healing_report, "InsideBarSMA_2Lot_SMA196", 100)
    backtest_report = backtest_reporter.generate_text_report()
else:
    backtest_report = f"""
================================================================================
BACKTEST REPORT - 2-LOT INSIDE BAR + SMA(196) STRATEGY
================================================================================

Results Summary:
- Total Trades: {len(trades_df)}
- Winning Trades: {len(trades_df[trades_df['win'] == True]) if len(trades_df) > 0 else 0}
- Losing Trades: {len(trades_df[trades_df['win'] == False]) if len(trades_df) > 0 else 0}
- Total P&L: ${trades_df['total_pnl'].sum():.2f} if len(trades_df) > 0 else $0.00
- Win Rate: {(len(trades_df[trades_df['win'] == True]) / len(trades_df) * 100):.2f}% if len(trades_df) > 0 else 0%

Strategy Configuration:
✓ SMA Period: 196 (increased from 96)
✓ Entry: Inside bar + SMA touch + Volume(1.5x)
✓ Lot 1: Exit at +250 pips OR 159 minutes
✓ Lot 2: Exit at 159 minutes (NO stop loss)
✓ Position split: 50/50 between lots
================================================================================
"""

facts_gen.save_backtest_report(backtest_report)
facts_gen.save_research_report(research_report)
facts_gen.save_movement_report(movement_report)
facts_gen.save_trades_csv(trades_df)
if len(movement_df) > 0:
    facts_gen.save_movement_data_csv(movement_df)

print(f"  ✓ All reports saved to: {facts_gen.get_strategy_path()}")

# Print summary
print("\n" + "=" * 110)
print("BACKTEST RESULTS - 2-LOT SMA(196) STRATEGY")
print("=" * 110)
print(f"\nTotal Trades: {len(trades_df)}")
print(f"Expected: ~250-300 trades (based on original SMA(96) generating 319)")
if len(trades_df) > 0:
    print(f"Actual: {len(trades_df)} trades")
    print(f"\nWinning: {len(trades_df[trades_df['win'] == True])}")
    print(f"Losing: {len(trades_df[trades_df['win'] == False])}")
    print(f"Win Rate: {(len(trades_df[trades_df['win'] == True]) / len(trades_df) * 100):.2f}%")
    print(f"Total P&L: ${trades_df['total_pnl'].sum():.2f}")
    print(f"Avg P&L/Trade: ${trades_df['total_pnl'].mean():.2f}")
    
    if healing is not None:
        print(f"\nHealth Status: {healing.health_status}")
        print(f"Profit Factor: {healing.diagnostics['metrics']['profit_factor']}")

print("\n✓ Analysis complete!")
print(f"✓ Results saved to: {facts_gen.get_strategy_path()}")
