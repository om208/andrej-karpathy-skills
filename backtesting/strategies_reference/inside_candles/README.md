# Inside Candles/Bars Reference Library

**Purpose**: Reference indicators for Inside Bar pattern detection and breakout signals

**Indicators in this folder**:
1. Inside Bars/Candles [CodeCraftedTrading] - v6 indicator
2. Multi-Timeframe Inside Bar Breakout - v6 indicator (4-Symbol Simultaneous)

---

## File Structure

```
inside_candles/
├── README.md (this file)
├── InsideBar_CodeCraftedTrading.pine (v6 indicator)
├── InsideBar_CodeCraftedTrading_ANALYSIS.md
├── MTF_InsideBar_4Symbol_Breakout.pine (v6 indicator)
└── MTF_InsideBar_4Symbol_ANALYSIS.md
```

---

## How These Indicators Work

### 1. Inside Bars/Candles [CodeCraftedTrading]

**Purpose**: Identifies inside bar patterns with visual highlights and level tracking

**Key Features**:
- Detects inside candles: `(high < high[1]) and (low > low[1])`
- Color highlights for inside bars
- Tracks previous bar's high/low levels
- Draws horizontal lines at support/resistance
- Labels with exact price levels
- Monitors for breakout (when levels are broken)

**Logic Flow**:
```
1. Detect inside bar formation
2. Store parent bar's high/low
3. Draw horizontal lines at those levels
4. Track until breakout occurs
5. Reset when broken
```

### 2. Multi-Timeframe Inside Bar Breakout (4-Symbol)

**Purpose**: Tracks inside bars across 4 symbols and multiple timeframes simultaneously

**Key Features**:
- Monitors 4 symbols: SPY, QQQ, IWM, DIA (configurable)
- Tracks 4 timeframes: 15m, 30m, 1h, Daily (configurable)
- Detects inside bars on ALL timeframes
- Identifies when ALL 4 symbols break in SAME direction
- Color-coded labels (bullish green, bearish red)
- Adaptive label positioning to avoid overlap

**Logic Flow**:
```
1. Fetch OHLC data from 4 symbols + 4 timeframes
2. Detect inside bars: (high < high[1]) and (low > low[1])
3. Check if all 4 symbols formed inside bars
4. Monitor for breakout in same direction
5. Plot labels with emoji indicators (📈 bullish, 📉 bearish)
```

---

## Key Implementation Patterns

### Inside Bar Detection
```pine
// Basic pattern (used in both indicators)
inside_bar = (high < high[1]) and (low > low[1])

// With confirmation
is_inside_bar_made = high < high[1] and low > low[1] and barstate.isconfirmed
```

### Multi-Timeframe Detection
```pine
// Fetch data from different timeframe
[h, l, c] = request.security(symbol, timeframe, [high, low, close])

// Check inside bar on that timeframe
inside_bar_mtf = (h < h[1]) and (l > l[1])
```

### Breakout Detection
```pine
// Bullish breakout (close above previous high)
bullish_break = close > high[1]

// Bearish breakout (close below previous low)
bearish_break = close < low[1]

// All 4 symbols break same direction
all_bullish = bullBreak1 and bullBreak2 and bullBreak3 and bullBreak4
```

### Label Management with Arrays
```pine
var array<label> labels = array.new<label>()

// Add new label
lbl = label.new(bar_index, price, text="Text")
array.push(labels, lbl)

// Limit array size (memory management)
while array.size(labels) > maxLabels
    label.delete(array.shift(labels))
```

---

## Comparison: v5 vs v6

### What Changed from v5 to v6

**v6 Features Not in v5**:
- `request.security()` with `lookahead` parameter
- `array<label>` for dynamic label management
- `input.symbol()` for symbol selection
- `input.timeframe()` for timeframe selection
- Enhanced color customization with opacity
- Better label positioning (stagger, distance %)

**Same Core Logic**:
- Inside bar detection formula unchanged
- Breakout detection logic identical
- Visual representation similar

### Converting to v5 Strategy (if needed)

Key differences:
- v6 indicators → use `indicator()`
- v5 strategies → use `strategy()`
- v6 arrays → replace with `var` tracking variables
- v6 color.new() with opacity → same in v5

---

## Learning Objectives

From these reference indicators, extract:

1. **Inside Bar Detection Pattern**
   - 3-candle confirmation: inside bar + confirmation bar + breakout bar
   - How to track previous levels
   - When to reset tracking

2. **Multi-Symbol Synchronization**
   - Fetch data from multiple symbols simultaneously
   - Compare conditions across symbols
   - Trigger only when all align

3. **Dynamic Label Management**
   - Use arrays for label storage
   - Implement memory limits (max labels)
   - Auto-delete old labels for performance

4. **Visual Clarity Techniques**
   - Stagger labels to prevent overlap
   - Adaptive positioning based on bar range
   - Color coding for direction
   - Emoji indicators for quick recognition

5. **State Management in Indicators**
   - Using `var` and `varip` keywords
   - Tracking bar indices
   - Managing breakout logic
   - Resetting state conditions

---

## How to Use These References

### For Strategy Development

When building inside bar strategies:
1. Use detection pattern from CodeCraftedTrading indicator
2. Apply MTF logic from 4-Symbol indicator
3. Convert to strategy using `strategy.entry()` / `strategy.close()`
4. Add position management and risk rules

### For Learning Pine Script v6

Study these indicators to learn:
- `request.security()` multi-symbol fetching
- `array<type>` dynamic data structures
- Label management and positioning
- State tracking with `var` and `varip`

### For Backtesting

Create strategies that:
1. Detect inside bars (from CodeCraftedTrading pattern)
2. Enter when ALL timeframes confirm (from MTF logic)
3. Exit on breakout or time-based rules
4. Track multiple symbols simultaneously

---

## Reference Materials Status

- ✅ CodeCraftedTrading Inside Bar indicator (v6)
- ✅ MTF Inside Bar 4-Symbol Breakout (v6)  
- ✅ Analysis documents for both
- ✅ Pattern extraction complete

Ready for:
- Creating inside bar strategies
- Multi-timeframe confirmation systems
- 4-symbol synchronized trading systems
- Educational Pine Script v6 learning

---

**Created**: 2026-05-04
**Source**: Public TradingView indicators
**Purpose**: Reference materials for strategy development
**Status**: Complete
