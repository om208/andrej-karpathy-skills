import pandas as pd
from datetime import datetime

class ReportGenerator:
    """Generate comprehensive backtesting reports"""

    def __init__(self, trades_df, healing_report, strategy_name, initial_capital):
        self.trades_df = trades_df
        self.healing_report = healing_report
        self.strategy_name = strategy_name
        self.initial_capital = initial_capital

    def generate_text_report(self):
        """Generate formatted text report"""
        report = []
        report.append("=" * 80)
        report.append("BACKTESTING REPORT - SELF-HEALING TRADING SYSTEM")
        report.append("=" * 80)
        report.append("")

        report.extend(self._section_summary())
        report.extend(self._section_metrics())
        report.extend(self._section_health())
        report.extend(self._section_trade_details())
        report.extend(self._section_pattern_analysis())
        report.extend(self._section_corrections())
        report.extend(self._section_next_steps())

        return "\n".join(report)

    def _section_summary(self):
        lines = []
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Strategy:           {self.strategy_name}")
        lines.append(f"Initial Capital:    ${self.initial_capital}")
        lines.append(f"Total P&L:          ${self.healing_report['diagnostics']['metrics']['total_pnl']}")
        lines.append(f"Report Generated:   {self.healing_report['timestamp']}")
        lines.append("")
        return lines

    def _section_metrics(self):
        lines = []
        lines.append("PERFORMANCE METRICS")
        lines.append("-" * 80)

        metrics = self.healing_report['diagnostics']['metrics']
        lines.append(f"Total Trades:       {metrics['total_trades']}")
        lines.append(f"Winning Trades:     {metrics['winning_trades']}")
        lines.append(f"Losing Trades:      {metrics['losing_trades']}")
        lines.append(f"Win Rate:           {metrics['win_rate']}%")
        lines.append(f"Profit Factor:      {metrics['profit_factor']}")
        lines.append(f"Avg Win:            ${metrics['avg_win']}")
        lines.append(f"Avg Loss:           ${metrics['avg_loss']}")
        lines.append(f"Avg Trade Size:     ${metrics['avg_trade_size']}")
        lines.append("")
        return lines

    def _section_health(self):
        lines = []
        lines.append("SYSTEM HEALTH CHECK")
        lines.append("-" * 80)

        health = self.healing_report['diagnostics']['health_check']
        status = self.healing_report['health_status']

        status_color = {
            'GREEN': '🟢 GREEN',
            'YELLOW': '🟡 YELLOW',
            'ORANGE': '🟠 ORANGE',
            'RED': '🔴 RED'
        }

        lines.append(f"Health Status:      {status_color.get(status, status)}")
        lines.append(f"Severity:           {health['severity']}")
        lines.append(f"Win Rate Target:    {health['win_rate_target']}")
        lines.append(f"Profit Factor:      {health['profit_factor_target']}")
        lines.append("")
        return lines

    def _section_trade_details(self):
        lines = []
        lines.append("TRADE ANALYSIS")
        lines.append("-" * 80)

        df = self.trades_df
        if len(df) > 0:
            lines.append(f"{'Entry Time':<20} {'Entry':<10} {'Exit':<10} {'P&L':<10} {'Reason':<15}")
            lines.append("-" * 80)

            for idx, trade in df.iterrows():
                entry_time = str(trade['entry_time'])[:16] if 'entry_time' in trade else 'N/A'
                entry = f"${trade['entry_price']:.2f}"
                exit_p = f"${trade['exit_price']:.2f}"
                pnl = f"${trade['pnl']:.2f}"
                reason = trade.get('exit_reason', 'N/A')

                lines.append(f"{entry_time:<20} {entry:<10} {exit_p:<10} {pnl:<10} {reason:<15}")

        lines.append("")
        return lines

    def _section_pattern_analysis(self):
        lines = []
        lines.append("PATTERN PERFORMANCE")
        lines.append("-" * 80)

        patterns = self.healing_report['diagnostics']['pattern_analysis']
        if patterns:
            lines.append(f"{'Pattern':<30} {'Trades':<10} {'Win Rate':<10} {'Avg P&L':<10}")
            lines.append("-" * 80)

            for pattern, stats in patterns.items():
                lines.append(
                    f"{pattern:<30} {stats['count']:<10} {stats['win_rate']}%{'':<7} ${stats['avg_pnl']:<9.2f}"
                )
        lines.append("")
        return lines

    def _section_corrections(self):
        lines = []
        lines.append("SELF-HEALING CORRECTIONS")
        lines.append("-" * 80)

        corrections = self.healing_report['corrections_recommended']
        if corrections:
            for i, corr in enumerate(corrections, 1):
                lines.append(f"{i}. {corr['type'].upper()}")
                lines.append(f"   Action: {corr['action']}")
                lines.append(f"   Reason: {corr['reason']}")
                lines.append("")
        else:
            lines.append("✓ No corrections needed. System is performing well.")
            lines.append("")

        return lines

    def _section_next_steps(self):
        lines = []
        lines.append("ACTION ITEMS FOR NEXT WEEK")
        lines.append("-" * 80)

        actions = self.healing_report['action_items']
        for action in actions:
            lines.append(action)

        lines.append("")
        lines.append("=" * 80)
        return lines

    def save_report(self, filepath):
        """Save report to file"""
        report_text = self.generate_text_report()
        with open(filepath, 'w') as f:
            f.write(report_text)
        return filepath
