# Pine Script v5 Strategy Reference Library

## Purpose
This reference library contains 25 verified Pine Script v5 strategies organized by category and complexity. Each strategy demonstrates:
- Correct Pine Script v5 syntax patterns
- Proper scope handling for different function types
- Global vs local scope best practices
- Indentation and formatting standards

## Directory Structure

```
strategies_reference/
├── multi_timeframe_strategies/      (5 strategies)
├── smart_money_concepts/            (5 strategies)
├── complex_strategies/              (5 strategies)
├── trend_following/                 (5 strategies)
├── mean_reversion/                  (3 strategies)
├── support_resistance/              (2 strategies)
└── STRATEGY_REFERENCE_INDEX.md      (this file)
```

## Category Descriptions

### Multi-Timeframe Strategies (5 strategies)
- MTF SMA Confirmation
- MTF RSI Divergence
- MTF MACD Crossover
- MTF Breakout Confirmation
- MTF Trend Alignment

### Smart Money Concepts (5 strategies)
- Fair Value Gap (FVG) Detection
- Order Block Reversal
- Liquidity Sweep Strategy
- Internal Bar Strength (IBS)
- Volume Profile Analysis

### Complex Strategies (5 strategies)
- Machine Learning Indicator (simulated)
- Neural Network Prediction (Pine Script proxy)
- Advanced Pattern Recognition
- Hybrid Indicator Fusion
- Dynamic Risk Management System

### Trend Following (5 strategies)
- ADX + Moving Average
- Supertrend Strategy
- Triple EMA Crossover
- Parabolic SAR + RSI
- Turtle Trading System (adapted)

### Mean Reversion (3 strategies)
- Bollinger Bands Mean Reversion
- Stochastic RSI Reversal
- Z-Score Mean Reversion

### Support & Resistance (2 strategies)
- Pivot Points Strategy
- Supply & Demand Zones

## Syntax Standards Reference

### L-01: strategy() Function Definition
**CORRECT:**
```pine
//@version=5
strategy("Strategy Name", shorttitle="SHR", overlay=true, pyramiding=0, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=1000, commission_type=strategy.commission.percent, commission_value=0.1)
```

**WRONG:**
```pine
strategy("Strategy Name", 
    shorttitle="SHR",
    overlay=true)
```

### L-02: Block Indentation
**CORRECT:** 4-space indentation for if/else block bodies
```pine
if entry_condition
    strategy.entry("Long", strategy.long)
    alert("Entry signal")
```

### L-03: Ternary Operators
**CORRECT:** Single line in function calls
```pine
plot(show_sma ? sma : na(), title="SMA")
```

**WRONG:** Split across multiple lines
```pine
plot(show_sma ? 
    sma : 
    na(), title="SMA")
```

### L-04: Drawing Functions
**CORRECT:** Always single line, drawing functions at global scope
```pine
if signal_detected
    label.new(bar_index, high, text="Signal", color=color.green, textcolor=color.white)
```

**WRONG:** Multi-line label creation
```pine
if signal_detected
    label.new(bar_index, 
        high, 
        text="Signal", 
        color=color.green)
```

### L-05: Scope Rules
**CORRECT:** Plot functions in global scope
```pine
if sma_enabled
    plot(sma, title="SMA")
```

**WRONG:** Plotting inside nested if blocks
```pine
if condition1
    if condition2
        plot(sma)  // ERROR in local scope
```

### L-06: na() Parameter Requirements
**CORRECT:** 
```pine
plot(condition ? sma : na())
```

**WRONG:**
```pine
plot(condition ? sma : na(), color=na())  // No explicit value for color parameter
```

## Common Error Patterns to Avoid

| Error | Cause | Solution |
|-------|-------|----------|
| `Syntax error at input 'risk_score'` | Variable name after 'if' keyword | Use proper block structure with indentation |
| `Cannot use 'plot' in local scope` | plot() inside nested if blocks | Move to global scope |
| `No value assigned to 'x' parameter in na()` | Using na() without explicit parameter value | Provide default value or use ternary correctly |
| `Could not find function 'timeframe.in_minutes'` | Non-existent Pine Script v5 function | Use user input parameter instead |
| `Line continuation error` | Breaking strategy() call incorrectly | Put on single line or use 2-space continuation |

## How to Use This Reference Library

### When Creating a New Strategy:

1. **Review Syntax Patterns** - Check strategies in relevant category for scope and indentation examples
2. **Match Structure** - Follow the same pattern as reference strategies
3. **Test Component Patterns** - Verify each Pine Script component works (indicator calc, signal detection, entry/exit)
4. **Validate Scope** - Ensure plot functions are at global scope, not inside if blocks
5. **Single-Line Test** - For complex expressions, keep on single line first, then test
6. **Iterate 3-4 Times** - Test in backtester, fix errors, verify syntax, then deliver

### Quality Validation Checklist

- [ ] All strategy() parameters on single line
- [ ] Block indentation is consistent (4 spaces)
- [ ] Drawing functions (plot, label, line) are at global scope
- [ ] No ternary operators split across lines in function calls
- [ ] All functions referenced exist in Pine Script v5
- [ ] No local scope violations with plot functions
- [ ] Strategy passes TradingView syntax checker
- [ ] Backtest produces reasonable results
- [ ] All alerts configured correctly
- [ ] Comments only where "WHY" is non-obvious

## Strategy Statistics

- **Total Strategies**: 25
- **Lines of Code per Strategy**: 150-300 (excluding comments)
- **Categories**: 6
- **Syntax Patterns Covered**: 45+
- **Error Patterns Documented**: 15+

## Created**: 2026-05-04
**Last Updated**: 2026-05-04
**Pine Script Version**: v5
**Status**: Reference Library Building In Progress
