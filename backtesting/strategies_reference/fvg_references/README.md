# FVG Reference Indicators Collection

This directory contains publicly available Fair Value Gap (FVG) indicators from TradingView.
These are stored as reference materials for learning and strategy development purposes.

## How to Add the Reference Files

### 1. Zeiierman - Multitimeframe Fair Value Gap (FVG)
**Source**: https://www.tradingview.com/script/5jS51RsP-Multitimeframe-Fair-Value-Gap-FVG-Zeiierman/

Steps:
1. Visit the TradingView link above
2. Open the indicator in the editor
3. Copy the complete Pine Script code
4. Paste into: `Zeiierman_MTF_FVG.pine`

### 2. kfatkin - MTF Fair Value Gaps  
**Source**: https://www.tradingview.com/script/wMQ5wj87-MTF-Fair-Value-Gaps/

Steps:
1. Visit the TradingView link above
2. Open the indicator in the editor
3. Copy the complete Pine Script code
4. Paste into: `Kfatkin_MTF_FVG.pine`

### 3. 30M FVG Raw Validator
**Source**: Search on TradingView for "30M FVG Raw Validator"

Steps:
1. Find on TradingView
2. Copy the complete Pine Script code  
3. Paste into: `FVG_Raw_Validator_30M.pine`

## File Structure

Once added, your directory will look like:
```
fvg_references/
├── README.md (this file)
├── Zeiierman_MTF_FVG.pine
├── Kfatkin_MTF_FVG.pine
├── FVG_Raw_Validator_30M.pine
├── Zeiierman_ANALYSIS.txt (optional notes)
├── Kfatkin_ANALYSIS.txt (optional notes)
└── FVG_VALIDATION_PATTERNS.txt (what we learned)
```

## Attribution

When storing these reference materials, maintain proper attribution:

```
// Original Indicator: [Indicator Name]
// Creator: [Creator Name]
// Source: https://www.tradingview.com/script/[ID]/
// Original License: [Check on TradingView]
// Usage: Reference material for Pine Script development
```

## Learning Objectives

From these indicators, we will document:

1. **FVG Detection Pattern**
   - 3-candle structure detection
   - Wick-based gap identification
   - Bullish/bearish gap logic

2. **Multi-Timeframe Approach**
   - request.security() usage
   - Data fetching from multiple TF
   - Confirmation logic across timeframes

3. **Visualization Techniques**
   - Box creation and management
   - Color coding for FVG types
   - Mitigation tracking display

4. **Performance Optimization**
   - Memory management strategies
   - Efficient box management
   - Zone limit implementation

## Next Steps

1. Copy and paste the three indicators from TradingView
2. Document key patterns you observe
3. Extract reusable FVG detection logic
4. Create new strategies based on these patterns
5. Test against the reference materials

## Reference Quality Metrics

After adding each indicator, verify:
- [ ] Code compiles without errors
- [ ] All components are documented
- [ ] FVG detection logic is clear
- [ ] Multi-timeframe approach is understandable
- [ ] Performance considerations are noted
- [ ] Can extract key patterns for own strategies

---

**Location**: `/backtesting/strategies_reference/fvg_references/`  
**Purpose**: Reference materials for FVG strategy development  
**Status**: Ready to receive reference indicator files
