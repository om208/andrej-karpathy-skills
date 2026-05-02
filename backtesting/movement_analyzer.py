import pandas as pd
import numpy as np

class MarketMovementAnalyzer:
    """
    Analyze market movement AFTER 159 minutes
    Track positive and negative moves
    Export to CSV for analysis
    """

    def __init__(self, trades_df):
        self.trades_df = trades_df
        self.movement_data = []

    def analyze_movements(self):
        """Analyze market movement for each trade"""
        self.movement_data = []

        for idx, trade in self.trades_df.iterrows():
            movement_record = {
                'trade_id': idx,
                'entry_time': trade['entry_time'],
                'exit_time': trade['exit_time'],
                'entry_price': trade['entry_price'],
                'minutes_held': trade['minutes_held'],
                'lot1_exit_reason': trade['lot1_exit_reason'],
                'lot2_exit_reason': trade['lot2_exit_reason'],
                'lot1_exit_price': trade['lot1_exit_price'],
                'lot2_exit_price': trade['lot2_exit_price'],
                'total_pnl': trade['total_pnl'],
                'positive_move_percent': trade['positive_move_after_159min'],
                'negative_move_percent': trade['negative_move_after_159min'],
                'win': trade['win']
            }
            self.movement_data.append(movement_record)

        return pd.DataFrame(self.movement_data)

    def generate_movement_summary(self):
        """Generate summary statistics"""
        df = pd.DataFrame(self.movement_data)

        if len(df) == 0:
            return {}

        # Filter for trades that reached 159 minutes
        long_trades = df[df['minutes_held'] >= 159]

        summary = {
            'total_trades': len(df),
            'trades_held_159_min': len(long_trades),

            'avg_positive_move': df['positive_move_percent'].mean(),
            'max_positive_move': df['positive_move_percent'].max(),
            'min_positive_move': df['positive_move_percent'].min(),

            'avg_negative_move': df['negative_move_percent'].mean(),
            'max_negative_move': df['negative_move_percent'].min(),  # Most negative
            'min_negative_move': df['negative_move_percent'].max(),  # Least negative (closest to 0)

            'avg_net_move': (df['positive_move_percent'] + df['negative_move_percent']).mean(),

            'trades_with_positive_move': len(df[df['positive_move_percent'] > 0]),
            'trades_with_negative_move': len(df[df['negative_move_percent'] < 0]),

            'winning_trades': len(df[df['win'] == True]),
            'losing_trades': len(df[df['win'] == False]),

            'avg_positive_move_on_winners': df[df['win'] == True]['positive_move_percent'].mean() if len(df[df['win'] == True]) > 0 else 0,
            'avg_positive_move_on_losers': df[df['win'] == False]['positive_move_percent'].mean() if len(df[df['win'] == False]) > 0 else 0,

            'avg_negative_move_on_winners': df[df['win'] == True]['negative_move_percent'].mean() if len(df[df['win'] == True]) > 0 else 0,
            'avg_negative_move_on_losers': df[df['win'] == False]['negative_move_percent'].mean() if len(df[df['win'] == False]) > 0 else 0,
        }

        return summary

    def export_to_csv(self, filepath):
        """Export movement data to CSV"""
        df = pd.DataFrame(self.movement_data)
        df.to_csv(filepath, index=False)
        return filepath

    def generate_movement_report(self):
        """Generate formatted movement analysis report"""
        df = pd.DataFrame(self.movement_data)
        summary = self.generate_movement_summary()

        report = []
        report.append("\n" + "=" * 100)
        report.append("MARKET MOVEMENT ANALYSIS - AFTER 159 MINUTES")
        report.append("=" * 100 + "\n")

        report.append("OVERVIEW")
        report.append("-" * 100)
        report.append(f"Total Trades Analyzed: {summary['total_trades']}")
        report.append(f"Trades Held Full 159 Minutes: {summary['trades_held_159_min']}")
        report.append(f"Winning Trades: {summary['winning_trades']}")
        report.append(f"Losing Trades: {summary['losing_trades']}")
        report.append("")

        report.append("POSITIVE MOVEMENT (Upside) STATISTICS")
        report.append("-" * 100)
        report.append(f"Average Positive Move: {summary['avg_positive_move']:.4f}%")
        report.append(f"Maximum Positive Move: {summary['max_positive_move']:.4f}%")
        report.append(f"Minimum Positive Move: {summary['min_positive_move']:.4f}%")
        report.append(f"Trades with Positive Move: {summary['trades_with_positive_move']}")
        report.append("")

        report.append("NEGATIVE MOVEMENT (Downside) STATISTICS")
        report.append("-" * 100)
        report.append(f"Average Negative Move: {summary['avg_negative_move']:.4f}%")
        report.append(f"Maximum Negative Move (Most Down): {summary['max_negative_move']:.4f}%")
        report.append(f"Minimum Negative Move (Least Down): {summary['min_negative_move']:.4f}%")
        report.append(f"Trades with Negative Move: {summary['trades_with_negative_move']}")
        report.append("")

        report.append("NET MOVEMENT (Combined)")
        report.append("-" * 100)
        report.append(f"Average Net Move: {summary['avg_net_move']:.4f}%")
        report.append("")

        report.append("MOVEMENT ON WINNERS VS LOSERS")
        report.append("-" * 100)
        report.append(f"Avg Positive Move on Winners: {summary['avg_positive_move_on_winners']:.4f}%")
        report.append(f"Avg Positive Move on Losers: {summary['avg_positive_move_on_losers']:.4f}%")
        report.append(f"Avg Negative Move on Winners: {summary['avg_negative_move_on_winners']:.4f}%")
        report.append(f"Avg Negative Move on Losers: {summary['avg_negative_move_on_losers']:.4f}%")
        report.append("")

        report.append("DETAILED TRADE-BY-TRADE MOVEMENT DATA")
        report.append("-" * 100)
        if len(df) > 0:
            report.append(f"{'Trade':<8} {'Entry':<12} {'P&L':<10} {'Pos Move':<12} {'Neg Move':<12} {'Win':<5}")
            report.append("-" * 100)

            for idx, row in df.iterrows():
                entry = f"${row['entry_price']:.2f}"
                pnl = f"${row['total_pnl']:.2f}"
                pos_move = f"{row['positive_move_percent']:.4f}%" if pd.notna(row['positive_move_percent']) else "N/A"
                neg_move = f"{row['negative_move_percent']:.4f}%" if pd.notna(row['negative_move_percent']) else "N/A"
                win = "✓" if row['win'] else "✗"

                report.append(f"{idx:<8} {entry:<12} {pnl:<10} {pos_move:<12} {neg_move:<12} {win:<5}")

        report.append("")
        report.append("=" * 100)

        return "\n".join(report)
