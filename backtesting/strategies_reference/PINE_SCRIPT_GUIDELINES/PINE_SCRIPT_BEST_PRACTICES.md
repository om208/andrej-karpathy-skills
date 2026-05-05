# Pine Script Best Practices & Style Guide

**Purpose**: Standards for writing clean, maintainable, error-free Pine Script code following official TradingView recommendations.

**Based On**: Official TradingView Style Guide + 25-Strategy Library patterns

**Last Updated**: 2026-05-05

---

## 🏗️ Core Structure Requirements

### Strategy Declaration (L-01)
**Rule**: Keep `strategy()` declaration on a single line
```pine
// ✅ CORRECT
strategy("Inside Bar + SMA(196) Strategy", shorttitle="IB-SMA", overlay=true, pyramiding=0, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=1000, commission_type=strategy.commission.percent, commission_value=0.1)

// ❌ WRONG
strategy("Inside Bar + SMA(196) Strategy", 
    shorttitle="IB-SMA", 
    overlay=true, 
    pyramiding=0)
```

**Why**: Pine Script v5 parser requires complete strategy() on one line. Multi-line breaks compilation.

---

### Indentation (L-02)
**Rule**: Use exactly 4 spaces per indentation level (never tabs or 2 spaces)
```pine
// ✅ CORRECT
if signal_detected
    entry_price := close
    lot1_active := true
    if enable_lot1
        strategy.entry("Long", strategy.long)

// ❌ WRONG (2 spaces)
if signal_detected
  entry_price := close
  lot1_active := true

// ❌ WRONG (mixed tabs and spaces)
if signal_detected
	entry_price := close
    lot1_active := true
```

**Why**: Consistency prevents scope errors and makes code readable. Pine Script compiler is sensitive to indentation context.

---

### Input Parameters Organization (L-02a)
**Rule**: Group related inputs with proper section headers
```pine
// ============================================================================
// SECTION 1: INPUT SETTINGS
// ============================================================================

sma_period = input.int(196, title="SMA Period", minval=50, maxval=500)
sma_touch_threshold_pct = input.float(2.0, title="SMA Touch Threshold (%)", minval=0.5, maxval=5.0)

// ============================================================================
// SECTION 2: CORE CALCULATIONS
// ============================================================================

sma = ta.sma(close, sma_period)
prev_high = high[1]
```

**Why**: Clear organization makes code maintainable and reduces errors. Follows official template pattern.

---

## 📝 Naming Conventions

### Variables
- **snake_case** for all variable names
- **Descriptive names** (no single letters except loop counters)
- **Clear intent** (not abbreviated unless obvious)

```pine
// ✅ CORRECT
is_inside_bar = (current_high < prev_high) and (current_low > prev_low)
entry_price = close
lot1_active = true
bars_held = bar_index - entry_bar

// ❌ WRONG
iib = (ch < ph) and (cl > pl)
ep = c
la = t
bh = bi - eb
```

### Functions
- **lowercase** with underscores
- **Verb-first** for action functions
- **Clear behavior** in the name

```pine
// ✅ CORRECT
trackInsideBars(tf) => ...
calculateCompressionRatio() => ...
checkSignalCondition() => ...

// ❌ WRONG
tib() => ...
calcCR() => ...
sig() => ...
```

### Constants
- **UPPER_CASE** for immutable values
- **Meaningful names**

```pine
// ✅ CORRECT
MAX_LABELS_PER_TF = 25
DEFAULT_TP_PIPS = 250
COMPRESSION_RATIO_MIN = 0.0
```

---

## 🔗 Operators & Conditionals (L-03)

### Ternary Operators
**Rule**: Keep ternary operations on single line
```pine
// ✅ CORRECT - Single line
result = condition1 and condition2 ? value_true : value_false

// ✅ CORRECT - In function call
plotshape(series=signal, color=signal ? color.green : color.red)

// ❌ WRONG - Multi-line (will cause errors in function calls)
result = condition1 and condition2 ? 
    value_true : 
    value_false
```

**Why**: Function parameter parsing fails on multi-line ternary. v5 requires single line within parameters.

### Comparison Operators
**Rule**: Use correct comparison (== not =)
```pine
// ✅ CORRECT
if close > sma
if rsi == 50
if bar_index >= entry_bar

// ❌ WRONG
if close = sma  // This assigns, not compares!
```

### Logical Operators
**Rule**: Use explicit conditions, not assignments in conditionals
```pine
// ✅ CORRECT
is_bullish = close > open
if is_bullish
    plotshape(...)

// ❌ WRONG
if is_bullish = true  // Assigns instead of comparing
```

---

## 🎨 Function Calls (L-04)

### Drawing Functions (Single Line)
**Rule**: Keep label.new(), line.new(), etc. on single line with all parameters
```pine
// ✅ CORRECT - All parameters on one line
lbl = label.new(bar_index, low - dist1, text="📈 Signal", style=label.style_label_up, color=color.green, textcolor=color.white, size=size.normal)

// ❌ WRONG - Multi-line (scope error)
lbl = label.new(bar_index, 
                low - dist1, 
                text="📈 Signal",
                style=label.style_label_up)
```

### Strategy Entry/Exit
**Rule**: Keep on single line with all parameters
```pine
// ✅ CORRECT
strategy.entry("Long", strategy.long, qty=lot_size if enable_lot1 else 0, comment="Entry L1")

// ✅ CORRECT - With limit order
strategy.exit("Exit L1 TP", "Lot1", limit=entry_price + tp_points, comment="Exit L1 TP")
```

---

## 📊 Plot Functions (L-05)

### Global Scope Only
**Rule**: All plot() calls must be at global scope, never inside if/for blocks
```pine
// ✅ CORRECT - Global scope
if show_sma
    plot(sma, title="SMA(196)", color=color.blue, linewidth=2)

// ✅ CORRECT - Conditional within plot's series parameter
plot(is_inside_bar ? bgcolor(color.aqua) : na, title="Inside Bar")

// ❌ WRONG - Will cause "Cannot use 'plot' in local scope"
if show_sma
    if close > sma
        plot(sma)  // Nested - ERROR!

// ❌ WRONG - Multi-level nesting
for i = 0 to 10
    plot(value)  // In loop - ERROR!
```

**Exception**: Use bgcolor() for conditional coloring instead of plot()
```pine
// ✅ CORRECT - Use bgcolor for conditional backgrounds
if show_entry_signals and is_inside_bar
    bgcolor(color.new(color.aqua, 80), title="Inside Bar")
```

### Plot Configuration Best Practices
```pine
// ✅ RECOMMENDED STRUCTURE
if show_sma
    plot(sma, title="SMA(196)", color=color.blue, linewidth=2)

if show_entry_signals and is_inside_bar
    bgcolor(color.new(color.aqua, 80), title="Inside Bar")

if show_entry_signals and signal_detected
    plotshape(series=true, style=shape.diamond, location=location.belowbar, color=color.green, title="Entry Signal")
```

---

## 🔧 Variable Declaration (L-06)

### Persistent Variables
**Rule**: Use `var` keyword for variables that maintain state across bars
```pine
// ✅ CORRECT
var bool lot1_active = false
var float entry_price = 0.0
var int entry_bar = 0
var array<label> bullLabels = array.new<label>()

// ❌ WRONG - Will reset every bar
lot1_active = false  // Gets reset each bar!
entry_price = 0.0   // Gets reset each bar!
```

### Session-Persistent Variables
**Rule**: Use `varip` for variables that persist across sessions and resets
```pine
// ✅ CORRECT - For tracking state across everything
varip lastHigh = 0.0
varip lastLow = 0.0
varip broken = false
varip inrange = false

// Use when you need values to survive script.reload()
```

### Local Variables
**Rule**: Use simple assignment for calculations within bars
```pine
// ✅ CORRECT
bars_held = bar_index - entry_bar
current_range = high - low
compression_ratio = current_range / prev_range
```

### Array Initialization
**Rule**: Initialize arrays with var keyword at global scope
```pine
// ✅ CORRECT
var array<label> bullLabels1 = array.new<label>()
var array<label> bearLabels1 = array.new<label>()

// Array operations in main logic
if signal_detected
    array.push(bullLabels1, lbl)
    while array.size(bullLabels1) > maxLabelsPerTF
        label.delete(array.shift(bullLabels1))
```

---

## ⚠️ Common Pattern Errors to Avoid

### Error 1: na() Checks
**Rule**: Always check for na before using values
```pine
// ✅ CORRECT
if not na(rsi) and rsi > 70
    signal = true

// ❌ WRONG - Crashes on first bars
if rsi > 70
    signal = true  // rsi might be na!
```

### Error 2: Historical Indexing
**Rule**: Be explicit about what you're comparing
```pine
// ✅ CORRECT - Clear reference
is_inside_bar = (high < high[1]) and (low > low[1])

// ❌ CONFUSING - Are you comparing previous or current?
is_inside_bar = (high < low[1])  // What are you doing?
```

### Error 3: Position Checks Before Entry
**Rule**: Always check position size before new entries
```pine
// ✅ CORRECT
if signal_detected and strategy.position_size == 0
    strategy.entry("Long", strategy.long)

// ❌ WRONG - Can pyramid unwanted entries
if signal_detected
    strategy.entry("Long", strategy.long)
```

### Error 4: Same-Bar Entry/Exit
**Rule**: Prevent entries and exits on same bar
```pine
// ✅ CORRECT - Track entry bar
if signal_detected and not in_position
    entry_bar := bar_index
    in_position := true

if in_position and bar_index > entry_bar and high >= tp_level
    strategy.close("Long")

// ❌ WRONG - Can enter and exit on same bar
if signal_detected
    strategy.entry("Long", strategy.long)
if high >= tp_level
    strategy.close("Long")  // Same bar!
```

---

## 📚 Code Organization Checklist

- [ ] Single-line strategy() declaration
- [ ] Consistent 4-space indentation throughout
- [ ] Input parameters in Section 1
- [ ] Calculations in Section 2+
- [ ] Entry logic in dedicated section
- [ ] Exit logic in dedicated section
- [ ] All plot() calls at global scope
- [ ] var keyword for persistent variables
- [ ] na() checks before using values
- [ ] Position checks before entries
- [ ] Ternary operators on single lines
- [ ] Drawing functions on single lines
- [ ] snake_case for variables
- [ ] UPPER_CASE for constants
- [ ] Clear section headers

---

## 🎯 Template Structure

```pine
//@version=5
strategy("Strategy Name", shorttitle="SN", overlay=true, pyramiding=0, default_qty_type=strategy.percent_of_equity, default_qty_value=100, initial_capital=1000, commission_type=strategy.commission.percent, commission_value=0.1)

// ============================================================================
// SECTION 1: INPUT SETTINGS
// ============================================================================

param1 = input.int(default_value, title="Parameter 1")

// ============================================================================
// SECTION 2: CORE CALCULATIONS
// ============================================================================

calculation1 = ta.sma(close, param1)
signal = calculation1 > close

// ============================================================================
// SECTION 3: STRATEGY LOGIC
// ============================================================================

var bool in_position = false
var float entry_price = 0.0

if signal and not in_position
    in_position := true
    entry_price := close
    strategy.entry("Long", strategy.long)

if in_position and close < entry_price
    in_position := false
    strategy.close("Long")

// ============================================================================
// SECTION 4: VISUALIZATION
// ============================================================================

plot(calculation1, title="Calculation", color=color.blue)

if signal
    bgcolor(color.new(color.green, 80))
```

---

**Last Updated**: 2026-05-05  
**Status**: Production Ready ✅  
**Based On**: TradingView Official Style Guide + 25-Strategy Library patterns
