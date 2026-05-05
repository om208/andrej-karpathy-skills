# Pine Script Strategy Writing Checklist

**Purpose**: Step-by-step verification before deploying any Pine Script strategy.

**Use This**: Before testing any new strategy to catch errors early.

**Last Updated**: 2026-05-05

---

## 📋 Phase 1: Pre-Writing Setup (Before Coding)

### Planning
- [ ] Define entry conditions clearly
- [ ] Define exit conditions clearly (stop-loss + take-profit)
- [ ] Identify 2-3 working reference strategies with similar pattern
- [ ] Review relevant guidelines from PINE_SCRIPT_GUIDELINES folder
- [ ] Sketch logic flow on paper or text editor
- [ ] List all parameters and input ranges

### Reference Selection
- [ ] Found a working reference strategy with similar structure
- [ ] Reviewed its input parameters and settings
- [ ] Understood its core logic and pattern
- [ ] Identified which sections to modify vs keep
- [ ] Noted its backtesting parameters (timeframe, asset, period)

---

## 🎯 Phase 2: Core Code Structure (During Coding)

### Strategy Declaration
- [ ] Single line: `strategy("Name", shorttitle="SN", overlay=true, ...)`
- [ ] All parameters on same line
- [ ] Include: pyramiding=0, default_qty_type, commission settings
- [ ] shorttitle is 2-5 characters max

### Input Parameters (Section 1)
- [ ] All inputs in dedicated section with header
- [ ] Clear title describing each parameter
- [ ] Appropriate minval/maxval ranges
- [ ] Default values make sense for the strategy
- [ ] Grouped by category (SMA, Risk, Display, etc)

**Example**:
```pine
sma_period = input.int(196, title="SMA Period", minval=50, maxval=500)
```

### Core Calculations (Section 2+)
- [ ] Clear section headers for each logical group
- [ ] Calculations don't depend on undefined variables
- [ ] Using correct ta.* functions (ta.sma, ta.rsi, etc)
- [ ] No circular dependencies in calculations
- [ ] Handling na values properly

**Example**:
```pine
// ============================================================================
// SECTION 2: CORE CALCULATIONS
// ============================================================================
sma = ta.sma(close, sma_period)
```

### Variable Declarations
- [ ] All persistent variables use `var` keyword
- [ ] Initial values are appropriate defaults
- [ ] Types are explicitly declared (bool, float, int)
- [ ] No variables declared without var that need persistence
- [ ] Array initialization: `var array<label> labels = array.new<label>()`

**Example**:
```pine
var bool lot1_active = false
var float entry_price = 0.0
var int entry_bar = 0
```

### Indentation
- [ ] Consistent 4-space indentation throughout
- [ ] No mixing of tabs and spaces
- [ ] Each nested block indented exactly 4 more spaces
- [ ] Code is readable and follows template structure

### Naming Conventions
- [ ] snake_case for all variables
- [ ] No single-letter variables (except i,j in loops)
- [ ] Function names are descriptive verbs
- [ ] Constants in UPPER_CASE
- [ ] Avoid abbreviations (use sma_period not sp)

---

## 🔧 Phase 3: Logic Verification

### Entry Logic
- [ ] Entry condition clearly defined
- [ ] Checked: `not in_position` or `strategy.position_size == 0`
- [ ] All required signals are confirmed (not na)
- [ ] Filters applied (trend, volatility, time-of-day, etc)
- [ ] Entry comment is descriptive
- [ ] Position sizing is sensible

**Example**:
```pine
if signal_detected and strategy.position_size == 0
    strategy.entry("Long", strategy.long, qty=lot_size, comment="Entry L1")
```

### Exit Logic
- [ ] Stop-loss defined and enforced
- [ ] Take-profit levels calculated correctly
- [ ] Proper units (pips converted to points, etc)
- [ ] Time-based exits if needed
- [ ] No same-bar entry/exit (bar_index check)
- [ ] Exit comments descriptive

**Example**:
```pine
tp_points = tp_pips / 10000
if in_position and close >= entry_price + tp_points
    strategy.close("Long", comment="TP Hit")
```

### Risk Management
- [ ] Position size is defined
- [ ] Risk per trade is reasonable (1-2% rule recommended)
- [ ] Maximum drawdown considered
- [ ] Stop-loss takes profit/loss into account
- [ ] pyramiding parameter set appropriately

### State Management
- [ ] Entry bar tracked if comparing current to entry
- [ ] Position active flag tracked properly
- [ ] State resets on exit
- [ ] No variables that should be var but aren't
- [ ] Array size limits enforced

---

## 📊 Phase 4: Visualization (if needed)

### Plot Functions
- [ ] All plot() calls at global scope
- [ ] No plot() inside nested if/for blocks
- [ ] Use bgcolor() for conditional backgrounds instead
- [ ] Use plotshape() for conditional markers
- [ ] Colors are clearly distinguishable

**Checklist**:
- [ ] Main indicator plotted
- [ ] Entry signals marked (plotshape or bgcolor)
- [ ] Exit signals marked if complex
- [ ] All plots have descriptive titles
- [ ] Color scheme is clear (green=bullish, red=bearish)

### Example:
```pine
plot(sma, title="SMA(196)", color=color.blue, linewidth=2)
if signal_detected
    bgcolor(color.new(color.green, 80), title="Entry Signal")
```

---

## 🐛 Phase 5: Error Prevention Checks

### Syntax Rules (L-01 to L-06)
- [ ] **L-01**: strategy() on single line ✅
- [ ] **L-02**: 4-space indentation consistent ✅
- [ ] **L-03**: Ternary operators single-line ✅
- [ ] **L-04**: Drawing functions single-line ✅
- [ ] **L-05**: plot() at global scope ✅
- [ ] **L-06**: var keyword used properly ✅

### Data Type Verification
- [ ] No = (assignment) used in if conditions
- [ ] All == comparisons use double equals
- [ ] No mixing int with float without conversion
- [ ] Array types correct (array<float>, array<label>, etc)
- [ ] Function calls match parameter types

### Index References
- [ ] [0] vs [1] usage is correct
- [ ] Comparing correct bars (not off-by-one)
- [ ] No accessing [99] on bar 50
- [ ] Previous bar references checked for bar_index > 0

### na() Safety
- [ ] na() checks before using early-bar indicators
- [ ] Division by zero prevented
- [ ] Bounds checking on arrays
- [ ] First bar handled properly

**Example**:
```pine
if not na(rsi) and rsi > 70
    signal = true
```

---

## 🎨 Phase 6: Code Quality Review

### Readability
- [ ] Clear section headers (use =============== format)
- [ ] Logical grouping of related code
- [ ] Variable names are self-documenting
- [ ] Comments only where WHY is non-obvious
- [ ] Max line length ~100 characters

### Maintainability
- [ ] Magic numbers replaced with input parameters
- [ ] Repeated code combined into functions if 3+ uses
- [ ] Clear variable names (not x, y, z)
- [ ] Settings in Section 1 (inputs)
- [ ] Logic in Sections 2+

### Performance
- [ ] request.security() calls minimized
- [ ] No nested loops exceeding 100 iterations
- [ ] Calculations cached in variables (not recalculated)
- [ ] Array operations efficient
- [ ] No repeated calculations

---

## ✅ Phase 7: Pre-Test Verification

### Compile Check
- [ ] Add to chart
- [ ] Check for compilation errors
- [ ] Fix any syntax errors
- [ ] No warnings in script

### Logic Dry-Run
- [ ] Entry condition makes logical sense
- [ ] Exit condition makes logical sense
- [ ] Risk management parameters seem reasonable
- [ ] Position sizing won't exceed equity

### Parameter Verification
- [ ] Default inputs are sensible
- [ ] Min/max ranges allow meaningful variations
- [ ] No inputs with invalid ranges (min > max)
- [ ] Inputs match documentation

---

## 🧪 Phase 8: Backtesting Setup

### Chart Setup
- [ ] Choose appropriate timeframe
- [ ] Use sufficient historical data (minimum 1 year)
- [ ] Chart loaded without errors
- [ ] Strategy appears on chart

### Strategy Tester Configuration
- [ ] Commission: 0.1% (FX typical)
- [ ] Slippage: 1-2 pips
- [ ] Initial capital: Reasonable amount ($1000-$10000)
- [ ] Verify position sizing makes sense
- [ ] Pyramiding set correctly

### Test Plan
- [ ] Test on current timeframe first
- [ ] Test on at least 2 different timeframes
- [ ] Test on different assets if applicable
- [ ] Test on different time periods
- [ ] Note any parameter combinations to avoid

---

## 📈 Phase 9: Backtest Results Review

### Metrics to Check
- [ ] Total trades > 20 (statistical significance)
- [ ] Win rate 55%+ (at minimum)
- [ ] Profit factor 1.0+ (breaking even)
- [ ] Max consecutive losses < 5
- [ ] Drawdown < 30% of equity

### Signal Quality
- [ ] Entry signals don't appear random
- [ ] Entries cluster in certain conditions
- [ ] Distribution seems reasonable
- [ ] No obvious overfitting

### Trade Analysis
- [ ] Examine winning trades - do they make sense?
- [ ] Examine losing trades - are they acceptable?
- [ ] Any pattern to winners vs losers?
- [ ] Risk/reward ratio reasonable?

---

## 🔄 Phase 10: Documentation & Deployment

### Documentation
- [ ] Code comments explain WHY, not WHAT
- [ ] Input parameters documented
- [ ] Strategy logic described briefly
- [ ] Known limitations noted
- [ ] Version number tracked

### Final Checklist Before Go-Live
- [ ] Passed all 10 phases above
- [ ] No compilation errors
- [ ] Backtested successfully
- [ ] Parameters make logical sense
- [ ] Risk management in place
- [ ] Code is clean and readable
- [ ] Tested on live chart (visual check)

### Commit & Push
- [ ] Descriptive commit message
- [ ] Clear explanation of what strategy does
- [ ] Reference to research/inspiration if applicable
- [ ] Pushed to correct branch

---

## 🚨 Red Flags (Stop and Fix)

If you see ANY of these:
- [ ] ❌ Compilation error - STOP, don't test
- [ ] ❌ Same-bar entry/exit - STOP, fix logic
- [ ] ❌ Win rate < 50% on backtest - STOP, review logic
- [ ] ❌ Position size unreasonable - STOP, recalculate
- [ ] ❌ No risk management - STOP, add stop-loss
- [ ] ❌ Over-optimized parameters - STOP, use defaults
- [ ] ❌ More than 100 trades on 1-week data - STOP, likely over-fitted
- [ ] ❌ Can't explain why strategy works - STOP, reconsider

---

## 📝 Quick Verification Shortcut

**If pressed for time, check these 7 things:**

1. ✅ `strategy()` on single line?
2. ✅ Indentation consistent (4 spaces)?
3. ✅ var keyword on persistent variables?
4. ✅ Compiles without errors?
5. ✅ No plot() in nested blocks?
6. ✅ Entry AND exit logic defined?
7. ✅ Backtested with realistic settings?

If ALL 7 are green ✅, safe to proceed.

---

## 📊 Before/After Template

**Copy this to verify structure**:

```
BEFORE CODING:
- Reference strategy selected: [name]
- Entry condition: [describe]
- Exit condition: [describe]
- Filters: [list 3-5]

AFTER CODING:
- Section headers: [count =] sections
- var declarations: [count] variables
- plot() calls: [count] at global scope
- Backtest win rate: [%]
- Backtest profit factor: [value]
- Drawdown: [%]

DECISION:
- [ ] Ready to deploy
- [ ] Needs adjustment: [specific issue]
- [ ] Abandon: [reason]
```

---

**Last Updated**: 2026-05-05  
**Usage**: Print this and use as checklist before testing  
**Status**: Comprehensive ✅
