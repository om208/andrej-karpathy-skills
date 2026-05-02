# Self-Healing Backtesting System

Advanced backtesting framework with automatic problem detection, diagnosis, and correction.

## Quick Start

```bash
python backtesting/main.py
```

This runs the default Support/Resistance strategy on BTC/USD data and generates a comprehensive report.

## System Architecture

```
backtesting/
├── main.py                 # Entry point - orchestrates entire backtest
├── data_loader.py          # Loads and parses CSV data
├── strategy_base.py        # Abstract base class for all strategies
├── self_healing.py         # Automatic diagnostics and corrections
├── report_generator.py     # Generates formatted reports
└── strategies/
    ├── support_resistance.py  # Example strategy implementation
    └── (add more strategies here)
```

## Understanding the Report

### Performance Metrics
- **Total Trades**: Number of trades executed
- **Win Rate**: Percentage of winning trades (target: 65%+)
- **Profit Factor**: Ratio of wins to losses (target: 1.5+)
- **Avg Win/Loss**: Average size of winning and losing trades

### Health Status
- 🟢 **GREEN**: System performing excellently
- 🟡 **YELLOW**: Good performance, minor improvements available
- 🟠 **ORANGE**: Needs attention
- 🔴 **RED**: Critical issues - implement corrections

### Self-Healing Corrections
Automatic recommendations to improve the strategy:
- **Confluence**: Increase entry requirements
- **Pattern Elimination**: Remove underperforming patterns
- **Risk/Reward**: Adjust take profit / stop loss distance

## Creating Your Own Strategy

### Step 1: Inherit from Strategy Base Class

```python
from strategy_base import Strategy

class MyStrategy(Strategy):
    def __init__(self, df, initial_capital=100, risk_per_trade=7, max_loss=10):
        super().__init__(df, initial_capital, risk_per_trade, max_loss)
        # Add your strategy parameters here
        self.param1 = 20
        self.param2 = 1.5
```

### Step 2: Implement generate_signals()

```python
def generate_signals(self):
    df = self.df.copy()
    
    # Calculate your indicators
    df['indicator1'] = df['close'].rolling(20).mean()
    df['indicator2'] = df['volume'].rolling(20).mean()
    
    self.signals = df
    return df
```

### Step 3: Implement backtest()

```python
def backtest(self):
    df = self.signals.copy()
    trades = []
    position = None
    
    for idx in range(1, len(df)):
        current = df.iloc[idx]
        
        if position is None:
            # Check entry conditions
            if current['indicator1'] > current['indicator2']:
                entry_price = current['close']
                position_size = self.calculate_position_size(entry_price)
                
                # YOUR OWN TAKE PROFIT LOGIC HERE
                take_profit = entry_price + (current['atr'] * 2)  # Example
                stop_loss = entry_price - (current['atr'] * 0.5)
                
                position = {
                    'entry_price': entry_price,
                    'position_size': position_size,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'entry_time': current['datetime']
                }
        else:
            # Check exit conditions
            if current['high'] >= position['take_profit']:
                exit_price = position['take_profit']
                exit_reason = 'take_profit'
            elif current['low'] <= position['stop_loss']:
                exit_price = position['stop_loss']
                exit_reason = 'stop_loss'
            else:
                continue  # Position still open
            
            # Record trade
            pnl = (exit_price - position['entry_price']) * position['position_size']
            trades.append({
                'entry_price': position['entry_price'],
                'exit_price': exit_price,
                'position_size': position['position_size'],
                'pnl': pnl,
                'win': pnl > 0,
                'exit_reason': exit_reason,
                'entry_time': position['entry_time'],
                'exit_time': current['datetime']
            })
            position = None
    
    self.trades = trades
    return trades
```

### Step 4: Update main.py to Use Your Strategy

```python
from strategies.my_strategy import MyStrategy

STRATEGY_PARAMS = {
    'initial_capital': 100,
    'risk_per_trade': 7,
    'max_loss': 10,
    # Add your strategy parameters here
}

results = run_backtest(
    DATA_PATH,
    MyStrategy,
    STRATEGY_PARAMS
)
```

## Available Helper Methods

### From Strategy Base Class

```python
# Calculate position size based on risk
position_size = self.calculate_position_size(entry_price)

# Built-in indicators (if not already calculated)
rsi = self._calculate_rsi(prices)
atr = self._calculate_atr(high, low, close)
```

## Output Files

- `reports/backtest_report.txt` - Complete formatted report with all metrics and recommendations

## Self-Healing System Flow

```
Backtest Complete
    ↓
Calculate Metrics (win rate, profit factor, etc.)
    ↓
Analyze Patterns (which patterns win/lose)
    ↓
Analyze Time (which hours perform best)
    ↓
Analyze Risk/Reward Ratios
    ↓
Health Check (assign status: GREEN/YELLOW/ORANGE/RED)
    ↓
Identify Corrections Needed
    ↓
Generate Action Items
    ↓
Report Generated
```

## Strategy Parameters Explained

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `initial_capital` | 100 | Account size in dollars |
| `risk_per_trade` | 7 | Max risk per trade in dollars |
| `max_loss` | 10 | Stop loss distance in dollars |
| `support_lookback` | 20 | Periods to look back for support |
| `volume_threshold` | 1.5 | Volume multiplier for confirmation |
| `rsi_oversold` | 30 | RSI level for oversold condition |
| `rsi_overbought` | 70 | RSI level for overbought condition |
| `tp_atr_multiplier` | 1.5 | Take profit distance (ATR multiplier) |

## Tips for Strategy Development

1. **Start Simple** - Begin with 2-3 core rules
2. **Check Reports** - Read the self-healing recommendations
3. **Implement Corrections** - Adjust parameters based on analysis
4. **Iterate Weekly** - Run backtest, analyze, improve
5. **Target 65%+ Win Rate** - Aim for YELLOW or better health status

## Common Issues

**Red Status (Low Win Rate)**
- Solution: Add more confluence factors (require multiple conditions)
- Solution: Restrict to best trading times
- Solution: Increase ATR multiplier for take profit

**Profit Factor Too Low**
- Solution: Tighten entry requirements
- Solution: Move take profit further away
- Solution: Eliminate worst-performing patterns

**Too Many Stop Losses**
- Solution: Use wider stop loss distances
- Solution: Require more confluence before entry
- Solution: Check if entries are too early

## Next Steps

1. Review the default `SupportResistanceStrategy` in `strategies/support_resistance.py`
2. Create your own strategy variant
3. Run backtest and analyze report
4. Implement self-healing recommendations
5. Iterate until you reach GREEN status
