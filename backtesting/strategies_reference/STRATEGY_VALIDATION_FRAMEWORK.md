# Pine Script v5 Strategy Validation Framework

## Overview

This framework provides a 3-4 iteration testing cycle for creating and validating Pine Script v5 strategies before delivery. Each iteration focuses on specific quality criteria.

## 4-Iteration Development Cycle

### ITERATION 1: Syntax Validation
**Focus**: Ensure code compiles without syntax errors

**Checklist**:
- [ ] All indicators calculate correctly without runtime errors
- [ ] strategy.entry() and strategy.close() syntax correct
- [ ] Variable declarations use proper 'var' keyword for persistent state
- [ ] No undefined function references
- [ ] All required parameters have default values
- [ ] strategy() declaration on single line with all parameters

**Key Tests**:
1. Load strategy in TradingView without errors
2. Open strategy settings and verify all inputs are editable
3. Apply to a 1-hour chart with 1-year data
4. Confirm no "Script error" message appears in bottom panel

**Common Errors in Iteration 1**:
- Line continuation syntax errors in strategy() call
- Undefined variable references
- Missing parameter values in function calls
- Incorrect indentation in block structures

**Acceptance Criteria**:
- ✅ Strategy loads without errors
- ✅ TradingView compiler returns zero errors
- ✅ All input fields appear in settings panel
- ✅ No runtime calculation errors

---

### ITERATION 2: Scope & Structure Validation
**Focus**: Ensure proper Pine Script v5 scope rules are followed

**Checklist**:
- [ ] plot() functions at global scope only
- [ ] No plot() calls inside nested if blocks
- [ ] label.new(), line.new(), box.new() on single lines
- [ ] No ternary operators split across multiple lines in function calls
- [ ] strategy.entry() and strategy.close() at global scope
- [ ] var variables initialized before use
- [ ] No na() parameters in ternary operators without explicit values
- [ ] Alert messages formatted correctly with str.format()

**Key Tests**:
1. Run backtest for 100+ trades minimum
2. Verify alerts fire at appropriate times
3. Check that entry/exit orders execute as expected
4. Confirm visualization elements (plots, shapes, boxes) appear correctly

**Scope Rule Verification**:
```
GLOBAL SCOPE (✓ Allowed):
- plot() ✓
- bgcolor() ✓
- plotshape() ✓
- label.new() ✓
- alert() ✓

LOCAL SCOPE (✗ NOT Allowed):
- plot() inside if block ✗
- Drawing functions after if statement ✗
```

**Common Errors in Iteration 2**:
- "Cannot use 'plot' in local scope" - plot inside nested if block
- "No value assigned to parameter" - na() in ternary
- Multi-line label.new() calls
- Ternary split across lines

**Acceptance Criteria**:
- ✅ Backtest runs without scope errors
- ✅ All visualization elements appear on chart
- ✅ Alerts generate and display correctly
- ✅ Entry/exit orders execute as intended

---

### ITERATION 3: Logic & Performance Validation
**Focus**: Verify trading logic and performance metrics

**Checklist**:
- [ ] Entry conditions work as designed
- [ ] Exit conditions execute properly
- [ ] Risk management parameters effective
- [ ] Win rate at acceptable threshold (65%+ for most strategies)
- [ ] Profit factor > 1.0
- [ ] No excessive whipsaws or false signals
- [ ] Position sizing appropriate for capital
- [ ] Commission impact on PnL realistic

**Key Tests**:
1. Full backtest on 2+ years of historical data
2. Analyze performance metrics:
   - Total trades: Should be reasonable for strategy type
   - Win rate: Target 60%+ for trend strategies, 55%+ for mean reversion
   - Profit factor: Target 1.5+ for consistent profitability
   - Max drawdown: Should be < 20% for conservative strategies
   - Average winner vs loser ratio: Should be > 1.5

3. Visual inspection:
   - Check for entry/exit clusters (over-trading)
   - Verify signals appear in correct market conditions
   - Confirm no signal generation during choppy markets (if unintended)

4. Compare performance across different market conditions:
   - Trending markets
   - Range-bound markets
   - High volatility periods
   - Low volatility periods

**Common Issues in Iteration 3**:
- Win rate too low (< 55%) → Tighten entry conditions
- Too many losing trades in sequence → Add volatility filter
- Too few trades → Expand entry conditions or adjust timeframes
- High drawdown → Reduce position size or tighten stops

**Acceptance Criteria**:
- ✅ Win rate >= 65% (or 55% for mean reversion)
- ✅ Profit factor >= 1.5
- ✅ Max drawdown <= 20%
- ✅ Trade frequency appropriate for strategy type
- ✅ No excessive whipsaws visible on chart
- ✅ Performance consistent across different market types

---

### ITERATION 4: Reference & Optimization Validation
**Focus**: Compare against reference strategies and optimize final parameters

**Checklist**:
- [ ] Compare syntax patterns with reference strategies
- [ ] Verify all scope rules match reference implementations
- [ ] Review entry/exit logic against reference strategies
- [ ] Confirm indentation consistent with library standards
- [ ] Optimize key parameters for better performance
- [ ] Test parameter sensitivity
- [ ] Verify backward compatibility (no breaking changes)
- [ ] Document any deviations from standard patterns
- [ ] Final code review for quality

**Key Tests**:
1. **Syntax Pattern Comparison**:
   - Match indentation with 4-space blocks (reference: MTF_SMA_Confirmation.pine)
   - Verify strategy() declaration format (reference: Supertrend_Strategy.pine)
   - Check plot function patterns (reference: FVG_Detection_Strategy.pine)

2. **Parameter Optimization**:
   - Test with different input combinations
   - Document optimal parameters found
   - Record parameter ranges that produce acceptable results
   - Note any parameter that significantly affects performance

3. **Edge Case Testing**:
   - Low volatility environments
   - Gaps and gaps downs
   - News-driven spikes
   - Weekend gaps in crypto
   - Holiday market closures

4. **Final Quality Review**:
   - [ ] Code follows all 6 syntax rules (L-01 through L-06)
   - [ ] Documentation complete and accurate
   - [ ] Error messages are clear
   - [ ] All alerts properly formatted
   - [ ] Comments only explain "WHY", not "WHAT"
   - [ ] No dead code or commented-out sections
   - [ ] Variable names are descriptive
   - [ ] Function structure is clean and logical

**Acceptance Criteria**:
- ✅ All syntax patterns match reference strategies
- ✅ Scope rules 100% compliant
- ✅ Performance stable across parameter ranges
- ✅ Edge cases handled appropriately
- ✅ Code passes final quality review
- ✅ Documentation is complete
- ✅ Ready for production deployment

---

## Reference Pattern Library Quick Links

| Pattern | Reference Strategy | Location |
|---------|-------------------|----------|
| Multi-Timeframe | MTF_SMA_Confirmation.pine | multi_timeframe_strategies/ |
| FVG Detection | FVG_Detection_Strategy.pine | smart_money_concepts/ |
| Trend Following | Supertrend_Strategy.pine | trend_following/ |
| Mean Reversion | Bollinger_Bands_MeanReversion.pine | mean_reversion/ |

## Metrics Interpretation Guide

### Win Rate
- **> 75%**: Excellent, very conservative strategy
- **65-75%**: Good, market-adaptive strategy
- **55-65%**: Acceptable, needs good risk management
- **< 55%**: Needs redesign or adjustment

### Profit Factor
- **> 2.0**: Excellent, high profitability
- **1.5-2.0**: Good, sustainable profitability
- **1.0-1.5**: Marginal, acceptable with good position sizing
- **< 1.0**: Strategy loses money, needs redesign

### Max Drawdown
- **< 10%**: Excellent, very stable
- **10-15%**: Good, acceptable risk
- **15-20%**: Moderate risk, acceptable for some strategies
- **> 20%**: High risk, consider reducing position size

### Trade Frequency
- **1-3 per day** (on daily chart): Good, not over-trading
- **3-10 per day**: Acceptable for some strategies
- **> 10 per day**: Over-trading, consider tightening entries
- **< 1 per week**: Under-trading, consider relaxing conditions

---

## Common Error Patterns & Fixes

| Error | Root Cause | Solution | Reference |
|-------|-----------|----------|-----------|
| `Syntax error at input 'if'` | Variable assigned incorrectly | Check if/else block indentation | L-02 |
| `Cannot use 'plot' in local scope` | plot() inside nested if | Move to global scope | L-05 |
| `No value assigned to 'x' parameter` | Using na() without value | Use if block instead of ternary | L-06 |
| `Line continuation error` | strategy() split incorrectly | Put on single line | L-01 |
| `Expected 'end', found 'if'` | Missing block closure | Check indentation | L-02 |
| `Multi-line ternary in function` | Ternary split across lines | Keep single line | L-03 |

---

## Pre-Delivery Checklist

Before sending strategy to user:

**Code Quality**:
- [ ] Runs in TradingView without errors (Iteration 1)
- [ ] All scope rules followed correctly (Iteration 2)
- [ ] Performance metrics acceptable (Iteration 3)
- [ ] Reference pattern validation complete (Iteration 4)
- [ ] Comments are minimal and explain "WHY"
- [ ] Variable names are self-documenting
- [ ] No console output or debug statements

**Documentation**:
- [ ] Strategy description provided
- [ ] All input parameters documented
- [ ] Entry/exit conditions clearly explained
- [ ] Example trades shown
- [ ] Risk management approach described

**Backtesting**:
- [ ] Tested on 2+ years data minimum
- [ ] Performance verified across market types
- [ ] Parameter sensitivity documented
- [ ] Edge cases handled appropriately

**Final Sign-Off**:
- [ ] Code review complete
- [ ] No outstanding issues
- [ ] Ready for live trading consideration
- [ ] User documentation complete

---

## Status Tracking Template

Create a file for each strategy during development:

```
STRATEGY: [Name]
STATUS: [ITERATION 1|2|3|4] ✓ COMPLETE

ITERATION 1: Syntax Validation
- Started: [Date]
- Errors Found: [List]
- Fixed: [Yes/No]
- Status: [✓ PASS | ✗ FAIL]

ITERATION 2: Scope & Structure
- Started: [Date]
- Errors Found: [List]
- Fixed: [Yes/No]
- Status: [✓ PASS | ✗ FAIL]

ITERATION 3: Logic & Performance
- Started: [Date]
- Win Rate: [XX%]
- Profit Factor: [X.XX]
- Trades: [XXX]
- Status: [✓ PASS | ✗ FAIL]

ITERATION 4: Reference & Optimization
- Started: [Date]
- Deviations from Reference: [List or None]
- Optimal Parameters: [List]
- Status: [✓ PASS | ✗ FAIL]

READY FOR DELIVERY: [✓ YES | ✗ NO]
```

---

**Framework Created**: 2026-05-04  
**Pine Script Version**: v5  
**Compliance**: Follows all L-01 through L-06 rules
