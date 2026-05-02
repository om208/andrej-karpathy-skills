import pandas as pd
import numpy as np
from collections import defaultdict

class StrategyResearchAnalyzer:
    """
    Advanced analysis of trading strategy results with detailed research
    Generates facts about winning vs losing trades
    """

    def __init__(self, trades_df):
        self.trades_df = trades_df
        self.winning_trades = trades_df[trades_df['win'] == True]
        self.losing_trades = trades_df[trades_df['win'] == False]

    def analyze_all(self):
        """Run complete analysis"""
        return {
            'winning_trades_facts': self._analyze_winning_trades(),
            'losing_trades_facts': self._analyze_losing_trades(),
            'pattern_facts': self._analyze_patterns(),
            'timing_facts': self._analyze_timing(),
            'volatility_facts': self._analyze_volatility(),
            'comparative_facts': self._compare_wins_vs_losses(),
            'drastic_move_analysis': self._analyze_drastic_moves()
        }

    def _analyze_winning_trades(self):
        """Detailed analysis of winning trades"""
        if len(self.winning_trades) == 0:
            return {'count': 0, 'message': 'No winning trades'}

        wt = self.winning_trades
        facts = {
            'count': len(wt),
            'percentage': f"{(len(wt) / len(self.trades_df) * 100):.2f}%",
            'total_pnl': f"${wt['pnl'].sum():.2f}",
            'avg_pnl': f"${wt['pnl'].mean():.2f}",
            'median_pnl': f"${wt['pnl'].median():.2f}",
            'max_pnl': f"${wt['pnl'].max():.2f}",
            'min_pnl': f"${wt['pnl'].min():.2f}",
            'std_dev_pnl': f"${wt['pnl'].std():.2f}",

            'avg_minutes_held': f"{wt['minutes_held'].mean():.0f} min",
            'median_minutes_held': f"{wt['minutes_held'].median():.0f} min",

            'exit_reason_breakdown': wt['exit_reason'].value_counts().to_dict(),

            'avg_inside_bar_range': f"${wt['inside_bar_range'].mean():.2f}",
            'avg_prev_bar_range': f"${wt['prev_bar_range'].mean():.2f}",

            'avg_drastic_move': f"{wt['drastic_move_percent'].mean():.2f}%",
            'max_drastic_move': f"{wt['drastic_move_percent'].max():.2f}%",

            'sma_touch_stats': {
                'avg_sma': f"${wt['sma_value'].mean():.2f}",
                'min_sma': f"${wt['sma_value'].min():.2f}",
                'max_sma': f"${wt['sma_value'].max():.2f}",
            },

            'price_range_stats': {
                'avg_entry_price': f"${wt['entry_price'].mean():.2f}",
                'price_std_dev': f"${wt['entry_price'].std():.2f}",
            }
        }

        return facts

    def _analyze_losing_trades(self):
        """Detailed analysis of losing trades"""
        if len(self.losing_trades) == 0:
            return {'count': 0, 'message': 'No losing trades'}

        lt = self.losing_trades
        facts = {
            'count': len(lt),
            'percentage': f"{(len(lt) / len(self.trades_df) * 100):.2f}%",
            'total_loss': f"-${abs(lt['pnl'].sum()):.2f}",
            'avg_loss': f"-${abs(lt['pnl'].mean()):.2f}",
            'median_loss': f"-${abs(lt['pnl'].median()):.2f}",
            'max_loss': f"-${abs(lt['pnl'].min()):.2f}",
            'min_loss': f"-${abs(lt['pnl'].max()):.2f}",
            'std_dev_loss': f"${lt['pnl'].std():.2f}",

            'avg_minutes_held': f"{lt['minutes_held'].mean():.0f} min",
            'median_minutes_held': f"{lt['minutes_held'].median():.0f} min",

            'exit_reason_breakdown': lt['exit_reason'].value_counts().to_dict(),

            'avg_inside_bar_range': f"${lt['inside_bar_range'].mean():.2f}",
            'avg_prev_bar_range': f"${lt['prev_bar_range'].mean():.2f}",

            'avg_drastic_move': f"{lt['drastic_move_percent'].mean():.2f}%",
            'max_drastic_move': f"{lt['drastic_move_percent'].max():.2f}%",

            'sma_touch_stats': {
                'avg_sma': f"${lt['sma_value'].mean():.2f}",
                'min_sma': f"${lt['sma_value'].min():.2f}",
                'max_sma': f"${lt['sma_value'].max():.2f}",
            },

            'price_range_stats': {
                'avg_entry_price': f"${lt['entry_price'].mean():.2f}",
                'price_std_dev': f"${lt['entry_price'].std():.2f}",
            }
        }

        return facts

    def _analyze_patterns(self):
        """Analyze inside bar and previous bar patterns"""
        facts = {}

        # Inside bar range analysis
        small_inside_bars = self.trades_df[self.trades_df['inside_bar_range'] < 50]
        medium_inside_bars = self.trades_df[(self.trades_df['inside_bar_range'] >= 50) & (self.trades_df['inside_bar_range'] < 100)]
        large_inside_bars = self.trades_df[self.trades_df['inside_bar_range'] >= 100]

        facts['inside_bar_analysis'] = {
            'small_bars_(<$50)': {
                'count': len(small_inside_bars),
                'win_rate': f"{(len(small_inside_bars[small_inside_bars['win'] == True]) / len(small_inside_bars) * 100):.2f}%" if len(small_inside_bars) > 0 else "N/A",
                'avg_pnl': f"${small_inside_bars['pnl'].mean():.2f}" if len(small_inside_bars) > 0 else "N/A"
            },
            'medium_bars_($50-$100)': {
                'count': len(medium_inside_bars),
                'win_rate': f"{(len(medium_inside_bars[medium_inside_bars['win'] == True]) / len(medium_inside_bars) * 100):.2f}%" if len(medium_inside_bars) > 0 else "N/A",
                'avg_pnl': f"${medium_inside_bars['pnl'].mean():.2f}" if len(medium_inside_bars) > 0 else "N/A"
            },
            'large_bars_(>$100)': {
                'count': len(large_inside_bars),
                'win_rate': f"{(len(large_inside_bars[large_inside_bars['win'] == True]) / len(large_inside_bars) * 100):.2f}%" if len(large_inside_bars) > 0 else "N/A",
                'avg_pnl': f"${large_inside_bars['pnl'].mean():.2f}" if len(large_inside_bars) > 0 else "N/A"
            }
        }

        # Ratio analysis (inside bar vs previous bar)
        self.trades_df['bar_ratio'] = self.trades_df['inside_bar_range'] / (self.trades_df['prev_bar_range'] + 0.001)
        ratio_lt_0_5 = self.trades_df[self.trades_df['bar_ratio'] < 0.5]
        ratio_0_5_to_0_8 = self.trades_df[(self.trades_df['bar_ratio'] >= 0.5) & (self.trades_df['bar_ratio'] < 0.8)]
        ratio_gte_0_8 = self.trades_df[self.trades_df['bar_ratio'] >= 0.8]

        facts['bar_ratio_analysis'] = {
            'very_small_ratio_(<0.5)': {
                'count': len(ratio_lt_0_5),
                'win_rate': f"{(len(ratio_lt_0_5[ratio_lt_0_5['win'] == True]) / len(ratio_lt_0_5) * 100):.2f}%" if len(ratio_lt_0_5) > 0 else "N/A",
                'avg_pnl': f"${ratio_lt_0_5['pnl'].mean():.2f}" if len(ratio_lt_0_5) > 0 else "N/A"
            },
            'medium_ratio_(0.5-0.8)': {
                'count': len(ratio_0_5_to_0_8),
                'win_rate': f"{(len(ratio_0_5_to_0_8[ratio_0_5_to_0_8['win'] == True]) / len(ratio_0_5_to_0_8) * 100):.2f}%" if len(ratio_0_5_to_0_8) > 0 else "N/A",
                'avg_pnl': f"${ratio_0_5_to_0_8['pnl'].mean():.2f}" if len(ratio_0_5_to_0_8) > 0 else "N/A"
            },
            'high_ratio_(>=0.8)': {
                'count': len(ratio_gte_0_8),
                'win_rate': f"{(len(ratio_gte_0_8[ratio_gte_0_8['win'] == True]) / len(ratio_gte_0_8) * 100):.2f}%" if len(ratio_gte_0_8) > 0 else "N/A",
                'avg_pnl': f"${ratio_gte_0_8['pnl'].mean():.2f}" if len(ratio_gte_0_8) > 0 else "N/A"
            }
        }

        return facts

    def _analyze_timing(self):
        """Analyze holding time and exit timing"""
        facts = {}

        quick_exits = self.trades_df[self.trades_df['minutes_held'] < 60]
        medium_holds = self.trades_df[(self.trades_df['minutes_held'] >= 60) & (self.trades_df['minutes_held'] < 159)]
        long_holds = self.trades_df[self.trades_df['minutes_held'] >= 159]

        facts['quick_exits_(<60_min)'] = {
            'count': len(quick_exits),
            'win_rate': f"{(len(quick_exits[quick_exits['win'] == True]) / len(quick_exits) * 100):.2f}%" if len(quick_exits) > 0 else "N/A",
            'avg_pnl': f"${quick_exits['pnl'].mean():.2f}" if len(quick_exits) > 0 else "N/A",
            'wins': len(quick_exits[quick_exits['win'] == True]),
            'losses': len(quick_exits[quick_exits['win'] == False])
        }

        facts['medium_holds_(60-159_min)'] = {
            'count': len(medium_holds),
            'win_rate': f"{(len(medium_holds[medium_holds['win'] == True]) / len(medium_holds) * 100):.2f}%" if len(medium_holds) > 0 else "N/A",
            'avg_pnl': f"${medium_holds['pnl'].mean():.2f}" if len(medium_holds) > 0 else "N/A",
            'wins': len(medium_holds[medium_holds['win'] == True]),
            'losses': len(medium_holds[medium_holds['win'] == False])
        }

        facts['long_holds_(>=159_min)'] = {
            'count': len(long_holds),
            'win_rate': f"{(len(long_holds[long_holds['win'] == True]) / len(long_holds) * 100):.2f}%" if len(long_holds) > 0 else "N/A",
            'avg_pnl': f"${long_holds['pnl'].mean():.2f}" if len(long_holds) > 0 else "N/A",
            'wins': len(long_holds[long_holds['win'] == True]),
            'losses': len(long_holds[long_holds['win'] == False])
        }

        return facts

    def _analyze_volatility(self):
        """Analyze market volatility at entry"""
        facts = {}

        low_vol = self.trades_df[self.trades_df['inside_bar_range'] < self.trades_df['inside_bar_range'].quantile(0.33)]
        mid_vol = self.trades_df[(self.trades_df['inside_bar_range'] >= self.trades_df['inside_bar_range'].quantile(0.33)) &
                                 (self.trades_df['inside_bar_range'] < self.trades_df['inside_bar_range'].quantile(0.67))]
        high_vol = self.trades_df[self.trades_df['inside_bar_range'] >= self.trades_df['inside_bar_range'].quantile(0.67)]

        facts['low_volatility_entries'] = {
            'count': len(low_vol),
            'win_rate': f"{(len(low_vol[low_vol['win'] == True]) / len(low_vol) * 100):.2f}%" if len(low_vol) > 0 else "N/A",
            'avg_pnl': f"${low_vol['pnl'].mean():.2f}" if len(low_vol) > 0 else "N/A",
            'avg_bar_range': f"${low_vol['inside_bar_range'].mean():.2f}" if len(low_vol) > 0 else "N/A"
        }

        facts['medium_volatility_entries'] = {
            'count': len(mid_vol),
            'win_rate': f"{(len(mid_vol[mid_vol['win'] == True]) / len(mid_vol) * 100):.2f}%" if len(mid_vol) > 0 else "N/A",
            'avg_pnl': f"${mid_vol['pnl'].mean():.2f}" if len(mid_vol) > 0 else "N/A",
            'avg_bar_range': f"${mid_vol['inside_bar_range'].mean():.2f}" if len(mid_vol) > 0 else "N/A"
        }

        facts['high_volatility_entries'] = {
            'count': len(high_vol),
            'win_rate': f"{(len(high_vol[high_vol['win'] == True]) / len(high_vol) * 100):.2f}%" if len(high_vol) > 0 else "N/A",
            'avg_pnl': f"${high_vol['pnl'].mean():.2f}" if len(high_vol) > 0 else "N/A",
            'avg_bar_range': f"${high_vol['inside_bar_range'].mean():.2f}" if len(high_vol) > 0 else "N/A"
        }

        return facts

    def _compare_wins_vs_losses(self):
        """Direct comparison of winning vs losing trades"""
        facts = {}

        if len(self.winning_trades) > 0 and len(self.losing_trades) > 0:
            facts['win_vs_loss_comparison'] = {
                'avg_pnl_winners': f"${self.winning_trades['pnl'].mean():.2f}",
                'avg_pnl_losers': f"-${abs(self.losing_trades['pnl'].mean()):.2f}",
                'pnl_difference': f"${self.winning_trades['pnl'].mean() + abs(self.losing_trades['pnl'].mean()):.2f}",

                'avg_hold_time_winners': f"{self.winning_trades['minutes_held'].mean():.0f} min",
                'avg_hold_time_losers': f"{self.losing_trades['minutes_held'].mean():.0f} min",

                'avg_inside_bar_winners': f"${self.winning_trades['inside_bar_range'].mean():.2f}",
                'avg_inside_bar_losers': f"${self.losing_trades['inside_bar_range'].mean():.2f}",

                'avg_drastic_move_winners': f"{self.winning_trades['drastic_move_percent'].mean():.2f}%",
                'avg_drastic_move_losers': f"{self.losing_trades['drastic_move_percent'].mean():.2f}%",

                'exit_reason_winners': dict(self.winning_trades['exit_reason'].value_counts()),
                'exit_reason_losers': dict(self.losing_trades['exit_reason'].value_counts())
            }

        return facts

    def _analyze_drastic_moves(self):
        """Analyze if 159-minute prediction holds true"""
        facts = {}

        # Trades held past 159 minutes
        past_159 = self.trades_df[self.trades_df['minutes_held'] >= 159]

        if len(past_159) > 0:
            facts['trades_held_past_159_minutes'] = {
                'count': len(past_159),
                'win_rate': f"{(len(past_159[past_159['win'] == True]) / len(past_159) * 100):.2f}%",
                'avg_pnl': f"${past_159['pnl'].mean():.2f}",
                'avg_drastic_move': f"{past_159['drastic_move_percent'].mean():.2f}%",
                'max_drastic_move': f"{past_159['drastic_move_percent'].max():.2f}%",
                'min_drastic_move': f"{past_159['drastic_move_percent'].min():.2f}%"
            }

        # Early exits (TP/SL before 159 minutes)
        early_exits = self.trades_df[self.trades_df['minutes_held'] < 159]

        if len(early_exits) > 0:
            facts['early_exits_before_159_minutes'] = {
                'count': len(early_exits),
                'win_rate': f"{(len(early_exits[early_exits['win'] == True]) / len(early_exits) * 100):.2f}%",
                'avg_pnl': f"${early_exits['pnl'].mean():.2f}",
                'avg_drastic_move': f"{early_exits['drastic_move_percent'].mean():.2f}%",
                'exit_via_tp': len(early_exits[early_exits['exit_reason'] == 'take_profit']),
                'exit_via_sl': len(early_exits[early_exits['exit_reason'] == 'stop_loss'])
            }

        return facts

    def generate_research_report(self):
        """Generate formatted research report"""
        analysis = self.analyze_all()

        report = []
        report.append("\n" + "=" * 80)
        report.append("TRADING STRATEGY RESEARCH REPORT - DATA ANALYSIS")
        report.append("=" * 80 + "\n")

        # Winning Trades Analysis
        report.append("📈 WINNING TRADES DETAILED ANALYSIS")
        report.append("-" * 80)
        for key, value in analysis['winning_trades_facts'].items():
            if isinstance(value, dict):
                report.append(f"\n{key}:")
                for k, v in value.items():
                    report.append(f"  {k}: {v}")
            else:
                report.append(f"{key}: {value}")
        report.append("")

        # Losing Trades Analysis
        report.append("\n📉 LOSING TRADES DETAILED ANALYSIS")
        report.append("-" * 80)
        for key, value in analysis['losing_trades_facts'].items():
            if isinstance(value, dict):
                report.append(f"\n{key}:")
                for k, v in value.items():
                    report.append(f"  {k}: {v}")
            else:
                report.append(f"{key}: {value}")
        report.append("")

        # Pattern Analysis
        report.append("\n🔍 PATTERN ANALYSIS (Inside Bar + Previous Bar)")
        report.append("-" * 80)
        for key, value in analysis['pattern_facts'].items():
            report.append(f"\n{key}:")
            if isinstance(value, dict):
                for pattern, stats in value.items():
                    report.append(f"\n  {pattern}:")
                    for k, v in stats.items():
                        report.append(f"    {k}: {v}")
        report.append("")

        # Timing Analysis
        report.append("\n⏱️  TIMING & HOLDING ANALYSIS")
        report.append("-" * 80)
        for key, value in analysis['timing_facts'].items():
            report.append(f"\n{key}:")
            for k, v in value.items():
                report.append(f"  {k}: {v}")
        report.append("")

        # Volatility Analysis
        report.append("\n📊 VOLATILITY ANALYSIS AT ENTRY")
        report.append("-" * 80)
        for key, value in analysis['volatility_facts'].items():
            report.append(f"\n{key}:")
            for k, v in value.items():
                report.append(f"  {k}: {v}")
        report.append("")

        # Win vs Loss Comparison
        report.append("\n⚖️  WIN VS LOSS COMPARISON")
        report.append("-" * 80)
        for key, value in analysis['comparative_facts'].items():
            report.append(f"\n{key}:")
            if isinstance(value, dict):
                for k, v in value.items():
                    if isinstance(v, dict):
                        report.append(f"\n  {k}:")
                        for k2, v2 in v.items():
                            report.append(f"    {k2}: {v2}")
                    else:
                        report.append(f"  {k}: {v}")
        report.append("")

        # Drastic Move Analysis (159-minute prediction)
        report.append("\n🚀 DRASTIC MOVE ANALYSIS (159-Minute Prediction)")
        report.append("-" * 80)
        for key, value in analysis['drastic_move_analysis'].items():
            report.append(f"\n{key}:")
            for k, v in value.items():
                report.append(f"  {k}: {v}")
        report.append("")

        report.append("\n" + "=" * 80)
        return "\n".join(report)
