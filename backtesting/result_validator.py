"""
Result Validator - Extracts and validates TradingView backtest results
Compares TradingView results with Python validator predictions
"""

import re
import json
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
from datetime import datetime
from config import Config


@dataclass
class BacktestResult:
    """Parsed backtest result"""
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0
    win_rate: float = 0.0
    total_pnl: float = 0.0
    avg_pnl: float = 0.0
    largest_win: float = 0.0
    largest_loss: float = 0.0
    profit_factor: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'total_trades': self.total_trades,
            'winning_trades': self.winning_trades,
            'losing_trades': self.losing_trades,
            'win_rate': self.win_rate,
            'total_pnl': self.total_pnl,
            'avg_pnl': self.avg_pnl,
            'largest_win': self.largest_win,
            'largest_loss': self.largest_loss,
            'profit_factor': self.profit_factor,
        }


class ResultValidator:
    """Validates backtest results from TradingView"""

    def __init__(self):
        self.result = BacktestResult()
        self.validation_report = {}

    def parse_backtest_html(self, html_content: str) -> BacktestResult:
        """
        Extract backtest results from TradingView HTML page

        Args:
            html_content: Raw HTML from backtest results page

        Returns:
            BacktestResult with parsed metrics
        """
        result = BacktestResult()

        try:
            # Pattern 1: Look for "Total Trades"
            trades_match = re.search(r'Total Trades[:\s]*(\d+)', html_content, re.IGNORECASE)
            if trades_match:
                result.total_trades = int(trades_match.group(1))

            # Pattern 2: Look for "Winning Trades"
            wins_match = re.search(r'Winning Trades[:\s]*(\d+)', html_content, re.IGNORECASE)
            if wins_match:
                result.winning_trades = int(wins_match.group(1))

            # Pattern 3: Look for "Losing Trades"
            losses_match = re.search(r'Losing Trades[:\s]*(\d+)', html_content, re.IGNORECASE)
            if losses_match:
                result.losing_trades = int(losses_match.group(1))

            # Pattern 4: Look for "Win Rate" or "Win %"
            wr_match = re.search(r'Win (?:Rate|%)[:\s]*([0-9.]+)%?', html_content, re.IGNORECASE)
            if wr_match:
                result.win_rate = float(wr_match.group(1))

            # Pattern 5: Look for "Net Profit" or "Total P&L"
            pnl_match = re.search(
                r'(?:Net Profit|Total P&L)[:\s]*(-?\$?[0-9,]+\.?[0-9]*)',
                html_content,
                re.IGNORECASE
            )
            if pnl_match:
                pnl_str = pnl_match.group(1).replace(',', '').replace('$', '')
                result.total_pnl = float(pnl_str)

            # Pattern 6: Look for "Avg P&L" or "Average"
            avg_match = re.search(
                r'(?:Avg P&L|Average)[:\s]*(-?\$?[0-9,]+\.?[0-9]*)',
                html_content,
                re.IGNORECASE
            )
            if avg_match:
                avg_str = avg_match.group(1).replace(',', '').replace('$', '')
                result.avg_pnl = float(avg_str)

            # Pattern 7: Look for "Largest Win"
            largest_win_match = re.search(
                r'Largest Win[:\s]*(-?\$?[0-9,]+\.?[0-9]*)',
                html_content,
                re.IGNORECASE
            )
            if largest_win_match:
                win_str = largest_win_match.group(1).replace(',', '').replace('$', '')
                result.largest_win = float(win_str)

            # Pattern 8: Look for "Largest Loss"
            largest_loss_match = re.search(
                r'Largest Loss[:\s]*(-?\$?[0-9,]+\.?[0-9]*)',
                html_content,
                re.IGNORECASE
            )
            if largest_loss_match:
                loss_str = largest_loss_match.group(1).replace(',', '').replace('$', '')
                result.largest_loss = float(loss_str)

            # Pattern 9: Calculate profit factor if we have wins and losses
            if result.winning_trades > 0 and result.total_pnl > 0:
                # Estimate profit factor from win rate and P&L
                if result.largest_loss != 0:
                    result.profit_factor = abs(result.total_pnl / (result.largest_loss * result.losing_trades))
                else:
                    result.profit_factor = float('inf')

            self.result = result
            return result

        except Exception as e:
            print(f"Error parsing backtest HTML: {str(e)}")
            return result

    def validate_against_expected(self) -> Dict[str, Any]:
        """
        Validate parsed results against expected results

        Returns:
            Validation report with status and details
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': 'PASSED',
            'issues': [],
            'details': {},
            'comparison': {}
        }

        # Validate win rate
        actual_wr = self.result.win_rate
        expected_wr = Config.EXPECTED.filtered_win_rate
        tolerance_wr = Config.EXPECTED.win_rate_tolerance_pct

        wr_status = 'PASS' if abs(actual_wr - expected_wr) <= tolerance_wr else 'FAIL'
        if wr_status == 'FAIL':
            report['status'] = 'FAILED'
            report['issues'].append(
                f"Win rate outside tolerance: {actual_wr:.2f}% vs {expected_wr:.2f}% "
                f"(tolerance: ±{tolerance_wr}%)"
            )

        report['details']['win_rate'] = {
            'expected': expected_wr,
            'actual': actual_wr,
            'difference': actual_wr - expected_wr,
            'tolerance': tolerance_wr,
            'status': wr_status
        }

        # Validate trade count
        actual_trades = self.result.total_trades
        expected_trades = Config.EXPECTED.filtered_trades
        tolerance_trades = Config.EXPECTED.trade_count_tolerance

        trades_status = 'PASS' if abs(actual_trades - expected_trades) <= tolerance_trades else 'FAIL'
        if trades_status == 'FAIL':
            report['status'] = 'FAILED'
            report['issues'].append(
                f"Trade count outside tolerance: {actual_trades} vs {expected_trades} "
                f"(tolerance: ±{tolerance_trades})"
            )

        report['details']['trades'] = {
            'expected': expected_trades,
            'actual': actual_trades,
            'difference': actual_trades - expected_trades,
            'tolerance': tolerance_trades,
            'status': trades_status
        }

        # Validate P&L
        actual_pnl = self.result.total_pnl
        expected_pnl = Config.EXPECTED.filtered_total_pnl
        tolerance_pnl = Config.EXPECTED.pnl_tolerance

        pnl_status = 'PASS' if abs(actual_pnl - expected_pnl) <= tolerance_pnl else 'FAIL'
        if pnl_status == 'FAIL':
            report['status'] = 'FAILED'
            report['issues'].append(
                f"P&L outside tolerance: ${actual_pnl:.2f} vs ${expected_pnl:.2f} "
                f"(tolerance: ±${tolerance_pnl})"
            )

        report['details']['pnl'] = {
            'expected': expected_pnl,
            'actual': actual_pnl,
            'difference': actual_pnl - expected_pnl,
            'tolerance': tolerance_pnl,
            'status': pnl_status
        }

        # Win/Loss ratio
        if self.result.total_trades > 0:
            ratio = (self.result.winning_trades / self.result.losing_trades) if self.result.losing_trades > 0 else float('inf')
            report['details']['ratio'] = {
                'wins': self.result.winning_trades,
                'losses': self.result.losing_trades,
                'ratio': ratio
            }

        self.validation_report = report
        return report

    def compare_with_validator(self, validator_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare TradingView results with Python validator results

        Args:
            validator_results: Results from Python validator

        Returns:
            Comparison report
        """
        comparison = {
            'status': 'MATCHED',
            'discrepancies': [],
            'metrics': {}
        }

        # Compare each metric
        metrics_to_compare = [
            ('win_rate', 'win_rate', 0.5),  # 0.5% tolerance
            ('total_trades', 'total_trades', 1),  # 1 trade tolerance
            ('total_pnl', 'total_pnl', 25.0),  # $25 tolerance
            ('winning_trades', 'winning_trades', 1),  # 1 trade tolerance
            ('losing_trades', 'losing_trades', 1),  # 1 trade tolerance
        ]

        for tradingview_key, validator_key, tolerance in metrics_to_compare:
            tv_value = getattr(self.result, tradingview_key, None)
            val_value = validator_results.get(validator_key)

            if tv_value is not None and val_value is not None:
                diff = abs(tv_value - val_value)
                matches = diff <= tolerance

                comparison['metrics'][tradingview_key] = {
                    'tradingview': tv_value,
                    'validator': val_value,
                    'difference': diff,
                    'tolerance': tolerance,
                    'match': matches
                }

                if not matches:
                    comparison['status'] = 'DISCREPANCIES'
                    comparison['discrepancies'].append(
                        f"{tradingview_key}: TV={tv_value}, Validator={val_value}, "
                        f"Diff={diff}, Tolerance={tolerance}"
                    )

        return comparison

    def generate_report(
        self,
        validator_results: Optional[Dict[str, Any]] = None,
        screenshots: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive validation report

        Args:
            validator_results: Results from Python validator
            screenshots: List of screenshot paths

        Returns:
            Complete report
        """
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {},
            'tradingview_results': self.result.to_dict(),
            'validation': self.validation_report,
            'comparison': None,
            'screenshots': screenshots or [],
            'recommendations': []
        }

        # Add comparison if validator results provided
        if validator_results:
            report['comparison'] = self.compare_with_validator(validator_results)

        # Generate summary
        report['summary'] = {
            'strategy': 'Inside Bar + SMA(196) with Inverse Filtering',
            'instrument': Config.BACKTEST.instrument,
            'timeframe': f"{Config.BACKTEST.timeframe}-minute",
            'date_range': f"{Config.BACKTEST.start_date} to {Config.BACKTEST.end_date}",
            'results': {
                'total_trades': self.result.total_trades,
                'win_rate': f"{self.result.win_rate:.2f}%",
                'total_pnl': f"${self.result.total_pnl:.2f}",
                'avg_pnl': f"${self.result.avg_pnl:.2f}"
            }
        }

        # Recommendations based on results
        if self.validation_report.get('status') == 'PASSED':
            report['recommendations'].append('✓ VALIDATION PASSED - Strategy ready for deployment')
            if self.result.win_rate >= 85:
                report['recommendations'].append('✓ Win rate EXCEEDS expectations (85%+)')
            report['recommendations'].append('→ Next step: Paper trading validation')
        else:
            report['recommendations'].append('✗ VALIDATION FAILED - Review discrepancies')
            for issue in self.validation_report.get('issues', []):
                report['recommendations'].append(f'  • {issue}')
            report['recommendations'].append('→ Next step: Debug and rerun backtest')

        return report

    def export_report_json(self, report: Dict[str, Any], filename: str = None) -> str:
        """
        Export report as JSON

        Args:
            report: Report to export
            filename: Output filename (optional)

        Returns:
            JSON string (and saves to file if filename provided)
        """
        json_str = json.dumps(report, indent=2, default=str)

        if filename:
            with open(filename, 'w') as f:
                f.write(json_str)
            print(f"✓ Report saved to {filename}")

        return json_str


if __name__ == '__main__':
    # Test parsing and validation
    print("="*80)
    print("RESULT VALIDATOR TEST")
    print("="*80 + "\n")

    # Create validator
    validator = ResultValidator()

    # Test with sample results
    sample_html = """
    <html>
    <body>
        Total Trades: 27
        Winning Trades: 23
        Losing Trades: 4
        Win Rate: 85.19%
        Net Profit: $4108.12
        Avg P&L: $152.15
        Largest Win: $436.98
        Largest Loss: -$79.10
    </body>
    </html>
    """

    print("[1] Parsing backtest HTML...")
    result = validator.parse_backtest_html(sample_html)
    print(f"  ✓ Total Trades: {result.total_trades}")
    print(f"  ✓ Win Rate: {result.win_rate}%")
    print(f"  ✓ Total P&L: ${result.total_pnl:.2f}")

    print("\n[2] Validating against expected results...")
    validation = validator.validate_against_expected()
    print(f"  Status: {validation['status']}")
    print(f"  Issues: {len(validation['issues'])}")

    print("\n[3] Comparing with validator results...")
    validator_results = {
        'total_trades': 27,
        'winning_trades': 23,
        'losing_trades': 4,
        'win_rate': 85.19,
        'total_pnl': 4108.12,
        'avg_pnl': 152.15
    }
    comparison = validator.compare_with_validator(validator_results)
    print(f"  Status: {comparison['status']}")
    print(f"  Discrepancies: {len(comparison['discrepancies'])}")

    print("\n[4] Generating complete report...")
    report = validator.generate_report(validator_results)
    print(f"  Summary: {report['summary']}")
    print(f"  Recommendations: {report['recommendations']}")

    print("\n" + "="*80)
    print("✓ Result Validator test completed successfully")
    print("="*80)
