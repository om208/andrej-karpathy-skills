#!/usr/bin/env python3

import sys
import pandas as pd

from data_loader import DataLoader
from strategies.inside_bar_sma_2lot_v2 import InsideBarSMA2LotV2Strategy
from self_healing import SelfHealingSystem
from report_generator import ReportGenerator
from research_analyzer import StrategyResearchAnalyzer
from movement_analyzer import MarketMovementAnalyzer
from strategy_facts_generator import StrategyFactsGenerator


print("\n" + "=" * 110)
print("2-LOT INSIDE BAR + SMA STRATEGY V2 - COMPREHENSIVE ANALYSIS")
print("=" * 110)

# Load data
print("\n[1/8] Loading data...")
loader = DataLoader("/root/.claude/uploads/ca2e0534-bab6-4265-aa59-166ae492020c/23c581a8-1M1MonthBTCUSD.P.csv")
df = loader.get_data()

# Initialize facts generator
facts_gen = StrategyFactsGenerator('InsideBarSMA_2Lot_Final', './strategy_facts')

# Save documentation
rules = [
    "Inside bar pattern: current candle within previous candle range",
    "SMA(96) touches the inside bar (within 2% threshold)",
    "Volume confirmation: current volume > 1.5x 20-period average",
    "Entry: ALL three conditions must be met",
    "Position: Split into 2 equal lots",
    "Lot 1: Exit at +250 pips OR after 159 minutes",
    "Lot 2: Exit ONLY at 159 minutes (NO stop loss)",
    "Track market movement after exit"
]

parameters = {
    'SMA Period': 96,
    'SMA Touch Threshold': '2%',
    'Volume Threshold': '1.5x',
    'Lot 1 Target': '+250 pips',
    'Hold Time': '159 minutes',
    'Initial Capital': '$100',
    'Risk Per Trade': '$7',
    'Timeframe': '1-minute',
    'Asset': 'BTC/USD'
}

facts_gen.save_strategy_documentation(rules, parameters)

# Run strategy
print("\n[2/8] Running 2-Lot Strategy...")
strategy_params = {
    'initial_capital': 100,
    'risk_per_trade': 7,
    'max_loss': 10,
    'sma_period': 96,
    'touch_threshold': 0.02,
    'exit_minutes': 159,
    'lot1_tp_pips': 250,
    'volume_threshold': 1.5
}

strategy = InsideBarSMA2LotV2Strategy(df, **strategy_params)
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
else:
    healing = None
    healing_report = None
    print(f"  ⚠ Only {len(trades_df)} trades - skipping detailed analysis")

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
    movement_summary = movement_analyzer.generate_movement_summary()
else:
    movement_df = pd.DataFrame()
    movement_report = "No trades to analyze."
    movement_summary = {}

# Save reports
print("\n[6/8] Saving reports...")
if healing is not None:
    backtest_reporter = ReportGenerator(trades_df, healing_report, "InsideBarSMA_2Lot_Final", 100)
    backtest_report = backtest_reporter.generate_text_report()
else:
    backtest_report = "Strategy produced fewer than 5 trades for proper analysis."

facts_gen.save_backtest_report(backtest_report)
facts_gen.save_research_report(research_report)
facts_gen.save_movement_report(movement_report)
facts_gen.save_trades_csv(trades_df)
if len(movement_df) > 0:
    facts_gen.save_movement_data_csv(movement_df)

print(f"  ✓ All reports saved to: {facts_gen.get_strategy_path()}")

# Print summary
print("\n" + "=" * 110)
print("RESULTS")
print("=" * 110)
print(backtest_report)

if movement_report != "No trades to analyze.":
    print("\n" + "=" * 110)
    print("MARKET MOVEMENT AFTER 159 MINUTES")
    print("=" * 110)
    print(movement_report)

print("\n✓ Analysis complete!")
