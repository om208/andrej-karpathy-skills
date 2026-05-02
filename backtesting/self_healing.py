import pandas as pd
import numpy as np
from datetime import datetime

class SelfHealingSystem:
    """
    Self-detecting, diagnosing, and correcting trading system
    Implements automatic problem detection and optimization
    """

    def __init__(self, trades_df, initial_capital=100):
        self.trades_df = trades_df
        self.initial_capital = initial_capital
        self.diagnostics = {}
        self.health_status = 'UNKNOWN'
        self.corrections = []

    def analyze(self):
        """Run complete self-healing analysis"""
        if len(self.trades_df) < 5:
            return {'status': 'insufficient_data', 'message': 'Need at least 5 trades for analysis'}

        self.diagnostics = {}
        self.diagnostics['metrics'] = self._calculate_metrics()
        self.diagnostics['pattern_analysis'] = self._analyze_patterns()
        self.diagnostics['time_analysis'] = self._analyze_time()
        self.diagnostics['risk_analysis'] = self._analyze_risk()
        self.diagnostics['health_check'] = self._perform_health_check()

        self.corrections = self._identify_corrections()
        return self.diagnostics

    def _calculate_metrics(self):
        df = self.trades_df
        total_trades = len(df)
        winning_trades = len(df[df['win'] == True])
        losing_trades = len(df[df['win'] == False])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0

        # Handle both 'pnl' and 'total_pnl' column names
        pnl_col = 'total_pnl' if 'total_pnl' in df.columns else 'pnl'

        total_pnl = df[pnl_col].sum()
        avg_win = df[df['win'] == True][pnl_col].mean() if winning_trades > 0 else 0
        avg_loss = abs(df[df['win'] == False][pnl_col].mean()) if losing_trades > 0 else 0
        profit_factor = avg_win / avg_loss if avg_loss > 0 else 0

        return {
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': round(win_rate, 2),
            'total_pnl': round(total_pnl, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'avg_trade_size': round(df[pnl_col].abs().mean(), 2)
        }

    def _analyze_patterns(self):
        df = self.trades_df
        pnl_col = 'total_pnl' if 'total_pnl' in df.columns else 'pnl'
        pattern_perf = {}

        for col in ['exit_reason', 'support']:
            if col in df.columns:
                for val in df[col].unique():
                    subset = df[df[col] == val]
                    wins = len(subset[subset['win'] == True])
                    total = len(subset)
                    wr = (wins / total * 100) if total > 0 else 0
                    pattern_perf[f'{col}_{val}'] = {
                        'count': total,
                        'win_rate': round(wr, 2),
                        'avg_pnl': round(subset[pnl_col].mean(), 2)
                    }

        return pattern_perf

    def _analyze_time(self):
        df = self.trades_df.copy()
        if 'entry_time' not in df.columns:
            return {}

        pnl_col = 'total_pnl' if 'total_pnl' in df.columns else 'pnl'
        df['entry_hour'] = pd.to_datetime(df['entry_time']).dt.hour
        hour_perf = {}

        for hour in df['entry_hour'].unique():
            subset = df[df['entry_hour'] == hour]
            wins = len(subset[subset['win'] == True])
            total = len(subset)
            wr = (wins / total * 100) if total > 0 else 0
            hour_perf[f'hour_{int(hour)}'] = {
                'count': total,
                'win_rate': round(wr, 2),
                'avg_pnl': round(subset[pnl_col].mean(), 2)
            }

        return hour_perf

    def _analyze_risk(self):
        df = self.trades_df
        return {
            'avg_risk_reward': round(df['risk_reward'].mean(), 2),
            'best_risk_reward': round(df['risk_reward'].max(), 2),
            'worst_risk_reward': round(df['risk_reward'].min(), 2),
            'trades_with_positive_rr': len(df[df['risk_reward'] > 1])
        }

    def _perform_health_check(self):
        metrics = self.diagnostics['metrics']
        wr = metrics['win_rate']
        pf = metrics['profit_factor']

        if wr >= 75 and pf > 1.5:
            self.health_status = 'GREEN'
            severity = 'Excellent'
        elif wr >= 65 and pf > 1.0:
            self.health_status = 'YELLOW'
            severity = 'Good'
        elif wr >= 55:
            self.health_status = 'ORANGE'
            severity = 'Needs Attention'
        else:
            self.health_status = 'RED'
            severity = 'Critical'

        return {
            'status': self.health_status,
            'severity': severity,
            'win_rate_target': 'On track' if wr >= 65 else 'Below target',
            'profit_factor_target': 'On track' if pf >= 1.0 else 'Below target'
        }

    def _identify_corrections(self):
        metrics = self.diagnostics['metrics']
        corrections = []

        if metrics['win_rate'] < 65:
            corrections.append({
                'type': 'confluence',
                'action': 'Increase confluence factors required for entry',
                'reason': f"Win rate is {metrics['win_rate']}% (target: 75%+)"
            })

        if metrics['profit_factor'] < 1.0:
            corrections.append({
                'type': 'position_sizing',
                'action': 'Reduce position size and increase TP distance',
                'reason': f"Profit factor is {metrics['profit_factor']} (target: 1.5+)"
            })

        pattern_analysis = self.diagnostics['pattern_analysis']
        for pattern, stats in pattern_analysis.items():
            if stats['win_rate'] < 50 and stats['count'] >= 3:
                corrections.append({
                    'type': 'pattern_elimination',
                    'action': f"Remove or restrict: {pattern}",
                    'reason': f"Win rate {stats['win_rate']}% with {stats['count']} trades"
                })

        return corrections

    def generate_report(self):
        """Generate healing report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'diagnostics': self.diagnostics,
            'health_status': self.health_status,
            'corrections_recommended': self.corrections,
            'action_items': self._generate_action_items()
        }

    def _generate_action_items(self):
        actions = []

        if len(self.corrections) == 0:
            actions.append("✓ System is healthy. Maintain current rules.")
        else:
            for i, corr in enumerate(self.corrections, 1):
                actions.append(f"{i}. {corr['action']}")
                actions.append(f"   Reason: {corr['reason']}")

        return actions
