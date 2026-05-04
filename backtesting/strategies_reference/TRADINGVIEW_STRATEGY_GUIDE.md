# TradingView Strategy Reference Guide

## How to Access TradingView Public Strategies

### TradingView Script Library Categories
- **URL**: https://www.tradingview.com/scripts/
- **Filtered by Type**: https://www.tradingview.com/scripts/?script_type=strategies
- **By Indicator Category**:
  - Moving Averages: https://www.tradingview.com/scripts/sma/
  - RSI: https://www.tradingview.com/scripts/relativestrengthindex/
  - MACD: https://www.tradingview.com/scripts/macd/?script_type=strategies
  - Ichimoku: https://www.tradingview.com/scripts/ichimoku/
  - Bollinger Bands: https://www.tradingview.com/scripts/bollingerbands/
  - VWAP: https://www.tradingview.com/scripts/vwap/

### Finding Public v5 Strategies

1. Go to https://www.tradingview.com/scripts/
2. Filter by "Strategies" 
3. Filter by "Pine Script v5"
4. Click on any public strategy (green lock icon = open source)
5. Click "Open in New Window" to view full code
6. Copy the complete code to your reference library

## Popular Pine Script v5 Strategy Categories

### 1. Multi-Timeframe Confirmation Strategies
**Characteristics**: Confirm signals on higher timeframes before entering
**Typical Indicators**: Moving Averages, RSI, MACD on multiple timeframes
**Example Use**: Entry on 5-min, confirm on 1-hour
**TradingView Library Search**: "multi-timeframe" or "MTF"

### 2. Smart Money Concepts (SMC) Strategies
**Characteristics**: Focus on order blocks, FVG, liquidity sweeps
**Key Patterns**: 
- Fair Value Gap (FVG)
- Order Blocks
- Internal Bar Strength (IBS)
- Liquidity Sweeps
**TradingView Library Search**: "order block" or "FVG" or "smart money"

### 3. Trend Following Strategies
**Characteristics**: Ride trends using momentum indicators
**Typical Indicators**: Supertrend, ADX, Moving Averages, Parabolic SAR
**Entry Logic**: Confirm trend strength before entering
**TradingView Library Search**: "trend" or "supertrend" or "ADX"

### 4. Mean Reversion Strategies
**Characteristics**: Trade extremes and expect reversal
**Typical Indicators**: RSI, Stochastic, Bollinger Bands, Z-Score
**Entry Logic**: Overbought/oversold conditions with momentum divergence
**TradingView Library Search**: "mean reversion" or "overbought" or "oversold"

### 5. Breakout Strategies
**Characteristics**: Enter on price breaking key levels
**Typical Setups**: 
- Support/resistance breaks
- Range breakouts
- Consolidation breakouts
**TradingView Library Search**: "breakout"

### 6. Indicator Combination Strategies
**Characteristics**: Combine 2-3 complementary indicators
**Common Combos**:
- RSI + MACD
- Moving Average + RSI + Volume
- Stochastic + MACD
- Bollinger Bands + RSI
**TradingView Library Search**: "RSI MACD" or specific indicator names

## Key Strategies to Reference

### Documented Below (Community/Official Examples)

| Name | Type | Indicator | Link |
|------|------|-----------|------|
| Ichimoku Cloud Strategy | Multi-Indicator | Ichimoku | GitHub |
| RSI Mean Reversion | Mean Reversion | RSI | TradingView Library |
| MACD Crossover | Trend Following | MACD | TradingView Library |
| Bollinger Bands Breakout | Breakout | Bollinger Bands | TradingView Library |
| Stochastic Divergence | Mean Reversion | Stochastic | TradingView Library |
| ADX Trend Filter | Trend Following | ADX | TradingView Library |
| VWAP Breakout | Breakout | VWAP | TradingView Library |
| Fibonacci Retracements | Support/Resistance | Fibonacci | TradingView Library |
| Volume Profile | Smart Money | Volume | TradingView Library |
| SuperTrend | Trend Following | ATR | TradingView Library |

## How to Evaluate TradingView Strategies

### Quality Checklist for Reference Strategies

When evaluating a strategy to add to your reference library:

**Syntax Quality**:
- [ ] Compiles without errors in Pine Script v5
- [ ] Clear, readable code structure
- [ ] Proper indentation and formatting
- [ ] Comments explain the "WHY", not the "WHAT"

**Scope Compliance**:
- [ ] plot() functions at global scope only
- [ ] No plot() calls inside nested if blocks
- [ ] All drawing functions use single-line syntax
- [ ] strategy.entry() and strategy.close() properly scoped

**Logic Quality**:
- [ ] Entry conditions clearly defined
- [ ] Exit conditions explicit
- [ ] Risk management implemented
- [ ] No obvious logical errors

**Performance**:
- [ ] Strategy description includes backtest results
- [ ] Win rate documented (should be 55%+)
- [ ] Profit factor mentioned (should be 1.0+)
- [ ] Maximum drawdown reasonable

**Documentation**:
- [ ] Clear explanation of what strategy does
- [ ] Parameters documented
- [ ] Recommended timeframes specified
- [ ] Known limitations mentioned

## Steps to Build 25-Strategy Reference Library

### Phase 1: Gather Strategies (1-2 hours)
1. Visit https://www.tradingview.com/scripts/?script_type=strategies
2. For each of 25 popular strategies:
   - Click on strategy name
   - Verify it's Pine Script v5
   - Verify it's open source (green lock)
   - Copy full source code
3. Save to appropriate category folder

### Phase 2: Organize & Categorize (1 hour)
1. Review each strategy's purpose
2. Assign to category:
   - multi_timeframe_strategies/
   - smart_money_concepts/
   - trend_following/
   - mean_reversion/
   - support_resistance/
   - (others as needed)
3. Rename files with clear names

### Phase 3: Document & Analyze (2-3 hours)
For each strategy, create analysis file containing:
- Strategy name and author
- Category and description
- Key indicators used
- Entry/exit logic summary
- Pine Script v5 syntax patterns demonstrated
- Performance metrics (if available)
- Unique features or innovations
- How to adapt/customize

### Phase 4: Extract Best Practices (1 hour)
1. Review all 25 strategies for common patterns
2. Document:
   - Scope rule patterns
   - Indentation standards used
   - Entry/exit pattern variations
   - Error handling approaches
   - Visualization techniques

## Expected Deliverables

After building the reference library, you should have:

1. **25 Pine Script v5 Strategy Files**
   - Organized in 6 category directories
   - All syntax verified
   - All from public TradingView sources

2. **Analysis Document for Each**
   - Strategy overview
   - Indicator list
   - Entry/exit conditions
   - Syntax patterns used
   - Performance summary

3. **Master Reference Index**
   - All 25 strategies listed
   - Category breakdown
   - Quick reference guide
   - Common patterns documented

4. **Validation Framework**
   - 4-iteration testing cycle
   - Quality checklist
   - Error prevention guide
   - Reference pattern library

## Why This Reference Library Matters

✅ **Consistency**: All new strategies follow same patterns  
✅ **Quality**: Every strategy verified against standards  
✅ **Learning**: See how professionals structure strategies  
✅ **Prevention**: Avoid common syntax and logic errors  
✅ **Speed**: Copy proven patterns for faster development  
✅ **Confidence**: Know your strategies are production-ready  

---

**Guide Created**: 2026-05-04  
**Pine Script Version**: v5  
**TradingView Scripts URL**: https://www.tradingview.com/scripts/
