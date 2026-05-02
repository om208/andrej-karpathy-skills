import os
import pandas as pd
from datetime import datetime

class StrategyFactsGenerator:
    """
    Generate and organize strategy facts and documentation
    Creates a structured folder for each strategy with all results and findings
    """

    def __init__(self, strategy_name, base_facts_dir='./strategy_facts'):
        self.strategy_name = strategy_name
        self.base_facts_dir = base_facts_dir
        self.strategy_dir = os.path.join(base_facts_dir, strategy_name)
        self._create_structure()

    def _create_structure(self):
        """Create organized folder structure"""
        os.makedirs(self.strategy_dir, exist_ok=True)
        os.makedirs(os.path.join(self.strategy_dir, 'reports'), exist_ok=True)
        os.makedirs(os.path.join(self.strategy_dir, 'data'), exist_ok=True)
        os.makedirs(os.path.join(self.strategy_dir, 'facts'), exist_ok=True)

    def save_strategy_documentation(self, rules, parameters):
        """Save strategy rules and parameters"""
        doc_path = os.path.join(self.strategy_dir, 'STRATEGY_DOCUMENTATION.txt')

        doc = []
        doc.append("=" * 100)
        doc.append(f"STRATEGY: {self.strategy_name}")
        doc.append("=" * 100)
        doc.append(f"Generated: {datetime.now().isoformat()}\n")

        doc.append("RULES")
        doc.append("-" * 100)
        for i, rule in enumerate(rules, 1):
            doc.append(f"{i}. {rule}")
        doc.append("")

        doc.append("PARAMETERS")
        doc.append("-" * 100)
        for param, value in parameters.items():
            doc.append(f"{param}: {value}")
        doc.append("")

        with open(doc_path, 'w') as f:
            f.write("\n".join(doc))

        return doc_path

    def save_backtest_report(self, report_content):
        """Save main backtest report"""
        report_path = os.path.join(self.strategy_dir, 'reports', 'BACKTEST_REPORT.txt')
        with open(report_path, 'w') as f:
            f.write(report_content)
        return report_path

    def save_research_report(self, report_content):
        """Save research analysis report"""
        report_path = os.path.join(self.strategy_dir, 'reports', 'RESEARCH_ANALYSIS.txt')
        with open(report_path, 'w') as f:
            f.write(report_content)
        return report_path

    def save_movement_report(self, report_content):
        """Save market movement analysis"""
        report_path = os.path.join(self.strategy_dir, 'reports', 'MOVEMENT_ANALYSIS.txt')
        with open(report_path, 'w') as f:
            f.write(report_content)
        return report_path

    def save_facts(self, fact_category, facts_content):
        """Save specific facts category"""
        fact_path = os.path.join(self.strategy_dir, 'facts', f'{fact_category.upper()}_FACTS.txt')
        with open(fact_path, 'w') as f:
            f.write(facts_content)
        return fact_path

    def save_trades_csv(self, trades_df):
        """Save trades data to CSV"""
        csv_path = os.path.join(self.strategy_dir, 'data', 'TRADES.csv')
        trades_df.to_csv(csv_path, index=False)
        return csv_path

    def save_movement_data_csv(self, movement_df):
        """Save movement analysis to CSV"""
        csv_path = os.path.join(self.strategy_dir, 'data', 'MOVEMENT_DATA.csv')
        movement_df.to_csv(csv_path, index=False)
        return csv_path

    def generate_facts_summary(self, metrics, patterns, recommendations):
        """Generate comprehensive facts summary"""
        facts = []

        facts.append("=" * 100)
        facts.append(f"FACTS SUMMARY - {self.strategy_name}")
        facts.append("=" * 100 + "\n")

        facts.append("KEY METRICS")
        facts.append("-" * 100)
        for metric, value in metrics.items():
            facts.append(f"{metric}: {value}")
        facts.append("")

        facts.append("PATTERNS DISCOVERED")
        facts.append("-" * 100)
        for i, pattern in enumerate(patterns, 1):
            facts.append(f"{i}. {pattern}")
        facts.append("")

        facts.append("RECOMMENDATIONS FOR IMPROVEMENT")
        facts.append("-" * 100)
        for i, rec in enumerate(recommendations, 1):
            facts.append(f"{i}. {rec}")
        facts.append("")

        facts.append("=" * 100)

        fact_path = os.path.join(self.strategy_dir, 'facts', 'FACTS_SUMMARY.txt')
        with open(fact_path, 'w') as f:
            f.write("\n".join(facts))

        return fact_path

    def generate_index(self, backtest_results):
        """Generate index file with all results"""
        index = []

        index.append("=" * 100)
        index.append(f"STRATEGY INDEX - {self.strategy_name}")
        index.append("=" * 100 + "\n")

        index.append("QUICK STATS")
        index.append("-" * 100)
        index.append(f"Total Trades: {backtest_results.get('total_trades', 'N/A')}")
        index.append(f"Win Rate: {backtest_results.get('win_rate', 'N/A')}%")
        index.append(f"Profit Factor: {backtest_results.get('profit_factor', 'N/A')}")
        index.append(f"Total P&L: {backtest_results.get('total_pnl', 'N/A')}")
        index.append(f"Health Status: {backtest_results.get('health_status', 'N/A')}")
        index.append("")

        index.append("FILES INCLUDED")
        index.append("-" * 100)
        index.append("📄 STRATEGY_DOCUMENTATION.txt - Complete strategy rules and parameters")
        index.append("📊 /reports/")
        index.append("   ├─ BACKTEST_REPORT.txt - Full backtest metrics and trade analysis")
        index.append("   ├─ RESEARCH_ANALYSIS.txt - Detailed data research on trades")
        index.append("   └─ MOVEMENT_ANALYSIS.txt - Market movement after 159 minutes")
        index.append("📋 /facts/")
        index.append("   ├─ FACTS_SUMMARY.txt - Key findings and patterns")
        index.append("   ├─ WINNING_TRADES_FACTS.txt - Analysis of winners")
        index.append("   └─ LOSING_TRADES_FACTS.txt - Analysis of losers")
        index.append("📈 /data/")
        index.append("   ├─ TRADES.csv - All trades with metrics")
        index.append("   └─ MOVEMENT_DATA.csv - Market movement data")
        index.append("")

        index.append("HOW TO USE")
        index.append("-" * 100)
        index.append("1. Start with STRATEGY_DOCUMENTATION.txt for rules overview")
        index.append("2. Read BACKTEST_REPORT.txt for performance summary")
        index.append("3. Study /facts/ folder for detailed findings")
        index.append("4. Analyze /data/ CSV files for deeper research")
        index.append("5. Check MOVEMENT_ANALYSIS.txt for 159-minute predictions")
        index.append("")

        index_path = os.path.join(self.strategy_dir, 'README.md')
        with open(index_path, 'w') as f:
            f.write("\n".join(index))

        return index_path

    def get_strategy_path(self):
        """Return the strategy folder path"""
        return self.strategy_dir
