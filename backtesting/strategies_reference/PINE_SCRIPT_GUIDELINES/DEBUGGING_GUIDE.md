# Pine Script Debugging Guide

**Purpose**: Tools and techniques for finding and fixing bugs in Pine Script strategies.

**Based On**: TradingView official debugging documentation

**Last Updated**: 2026-05-05

---

## 🔍 Debugging Tools Available

### 1. Plot Function (Visual Debugging)
**Best For**: Quick visual inspection of values on chart

```pine
// Plot a calculation to see its value
plot(sma, title="SMA Debug", color=color.blue, linewidth=2)

// Plot a condition (true/false appears as 1/0)
plot(is_inside_bar ? 1 : 0, title="Inside Bar Debug")

// Plot with different colors based on condition
plot_color = signal ? color.green : color.gray
plot(close, title="Price", color=plot_color)
```

**When to Use**:
- Check if calculations are correct
- Verify signal behavior visually
- Test parameter changes impact

---

### 2. Label Function (Precise Marking)
**Best For**: Marking exact bars and prices with annotations

```pine
// Mark entry points on chart
if signal_detected
    label.new(bar_index, low - 5*syminfo.mintick, text="ENTRY", style=label.style_label_up, color=color.green, textcolor=color.white)

// Mark values at specific bars
if barstate.islast
    label.new(bar_index, sma, text=str.format("SMA: {0,number,0.00000}", sma), yloc=yloc.abovebar)
```

**Advantages**:
- Precise bar identification
- Can show exact values
- Visible directly on chart

**Disadvantages**:
- Limited to 500 labels per script
- Can clutter chart

---

### 3. Pine Logs (Structured Debugging) - RECOMMENDED
**Best For**: Production debugging without cluttering chart

```pine
// Log info messages
if signal_detected
    log.info(str.format("Signal at bar {0}, price: {1,number,0.00000}", bar_index, close))

// Log warnings for unusual conditions
if compression_ratio < min_compression_ratio
    log.warning(str.format("Compression too tight: {0,number,0.00}", compression_ratio))

// Log errors when issues occur
if not na(rsi) and rsi > 100
    log.error("RSI impossible value: " + str.tostring(rsi))
```

**How to View**:
1. Open Pine Editor
2. Click "Pine Logs" tab (bottom of editor)
3. Logs appear in real-time

**Advantages**:
- Doesn't clutter chart
- Structured output
- Can disable easily
- Works in production

**Log Levels**:
- `log.info()` - General information
- `log.warning()` - Something unexpected
- `log.error()` - Something is wrong

---

## 🎯 Common Debugging Scenarios

### Scenario 1: Entry Signal Never Fires

**Step 1: Verify Entry Condition**
```pine
// Add logging to entry condition
if barstate.isconfirmed
    log.info(str.format("is_inside_bar: {0}, sma_touches: {1}, compression: {2,number,0.00}", is_inside_bar, sma_touches, compression_ratio))
```

**Step 2: Check Each Component**
```pine
// Debug individual conditions
if not is_inside_bar
    log.warning("Not inside bar")
if not sma_touches
    log.warning("SMA not touching")
if compression_ratio < min_compression_ratio
    log.warning(str.format("Compression {0} below min {1}", compression_ratio, min_compression_ratio))
```

**Step 3: Visualize Conditions**
```pine
// Show what's passing and what's failing
bgcolor(is_inside_bar ? color.new(color.blue, 80) : na, title="Inside Bar")
bgcolor(sma_touches ? color.new(color.green, 80) : na, title="SMA Touch")
```

---

### Scenario 2: Entry Fires But Exit Doesn't

**Step 1: Verify Exit Condition**
```pine
if in_position
    log.info(str.format("In position - Entry: {0,number,0.00000}, Current: {1,number,0.00000}, TP: {2,number,0.00000}", entry_price, close, tp_level))
```

**Step 2: Check Exit Trigger**
```pine
if in_position
    bars_held = bar_index - entry_bar
    log.info(str.format("Bars held: {0}, Required: {1}", bars_held, max_hold_bars))
    log.info(str.format("Close {0} >= TP {1}? {2}", close, tp_level, close >= tp_level))
```

**Step 3: Mark Exit Points**
```pine
if in_position and (close >= tp_level or bars_held >= max_hold_bars)
    label.new(bar_index, high + 5*syminfo.mintick, text="EXIT", style=label.style_label_down, color=color.red)
```

---

### Scenario 3: Results Seem Unrealistic

**Problem**: Win rate too high, or trades too profitable

**Common Causes**:
1. **Repainting** - Condition fires late with hindsight
2. **Lookahead bias** - Using future data
3. **Same-bar entry/exit** - Unrealistic fills

**Debug Repainting**:
```pine
// Good: Only fires when bar confirmed
if barstate.isconfirmed and signal_detected
    strategy.entry("Long", strategy.long)

// Bad: Fires on open bar, changes with updates
if signal_detected
    strategy.entry("Long", strategy.long)
```

**Debug Lookahead**:
```pine
// Check request.security lookahead setting
mtf_close = request.security(syminfo.tickerid, mtf_timeframe, close, lookahead=barmerge.lookahead_off)
```

**Debug Same-Bar Entry/Exit**:
```pine
if in_position
    bars_held = bar_index - entry_bar
    if bars_held <= 1
        log.warning("Potential same-bar exit")
    // Require at least 2 bars before exit
    if bars_held >= 2 and close >= tp_level
        strategy.close("Long")
```

---

### Scenario 4: Script Runs Slowly or Times Out

**Step 1: Identify Bottleneck**
```pine
// Check request.security call count
log.info("Getting MTF data...")
mtf_sma1 = request.security(sym, tf, ta.sma(close, 20))
log.info("MTF SMA 1 retrieved")

mtf_sma2 = request.security(sym, tf, ta.sma(close, 50))
log.info("MTF SMA 2 retrieved")
```

**Step 2: Optimize request.security() Calls**

```pine
// WRONG - Two calls
sma20 = request.security(sym, tf, ta.sma(close, 20))
sma50 = request.security(sym, tf, ta.sma(close, 50))

// RIGHT - One call
[sma20, sma50] = request.security(sym, tf, [ta.sma(close, 20), ta.sma(close, 50)])
```

**Step 3: Check Loop Performance**
```pine
// WRONG - Too many iterations
for i = 0 to 1000
    x = close[i] // Accessing 1000 bars

// RIGHT - Access only needed bars
max_lookback = 50
for i = 0 to max_lookback
    x = close[i]
```

---

## 📋 Debugging Checklist

When something's wrong, check in this order:

### Compilation Issues
1. [ ] strategy() on single line?
2. [ ] Indentation consistent (4 spaces)?
3. [ ] Missing semicolons or commas?
4. [ ] var keyword on persistent variables?
5. [ ] plot() outside nested blocks?

### Logic Issues
1. [ ] Entry condition reaches (add logging)?
2. [ ] Entry condition is persistent (var needed)?
3. [ ] Exit condition reaches (add logging)?
4. [ ] Bars separated (not same-bar entry/exit)?
5. [ ] na() values handled (not crashing)?

### Performance Issues
1. [ ] request.security() calls minimized?
2. [ ] Loops don't exceed 100+ iterations?
3. [ ] Calculations cached in variables?
4. [ ] No nested loops over large ranges?
5. [ ] Script completes in < 1 second per bar?

---

## 🔧 Debug Session Example

**Problem**: Entry signal fires too much

**Solution Approach**:

```pine
// Step 1: Log entry condition components
if barstate.isconfirmed
    log.info(str.format("Bar {0}: close={1}, sma={2}, diff={3}", 
        bar_index, close, sma, close - sma))

// Step 2: Visualize each condition
bgcolor(close > sma ? color.new(color.green, 80) : na, title="Price > SMA")
bgcolor(signal_detected ? color.new(color.blue, 80) : na, title="Signal")

// Step 3: Mark entries
if signal_detected
    label.new(bar_index, low - 5*syminfo.mintick, text=str.format("Entry #{0}", entry_count), 
        style=label.style_label_up, color=color.green)

// Step 4: Log entry details
if signal_detected and not in_position
    entry_count := entry_count + 1
    log.info(str.format("Entry #{0} at {1}, price: {2,number,0.00000}", 
        entry_count, bar_index, close))
```

**Result**: Instantly see:
- How many signals fire
- Why they fire
- Where they occur
- Exact values involved

---

## 💡 Pro Tips

### Tip 1: Use str.format() for Readable Output
```pine
// BAD - Hard to read
log.info(close)
log.info(sma)
log.info(signal)

// GOOD - Clear output
log.info(str.format("Close: {0,number,0.00000}, SMA: {1,number,0.00000}, Signal: {2}", 
    close, sma, signal))
```

### Tip 2: Conditional Logging
```pine
// Only log on specific conditions to reduce noise
if barstate.islast
    log.info("Final values: " + str.format("Close: {0}", close))
```

### Tip 3: Use table for Final Summary
```pine
if barstate.islast
    t = table.new(position.top_right, 2, 3, border_color=color.white)
    table.cell(t, 0, 0, "Total Trades", text_color=color.white, bgcolor=color.navy)
    table.cell(t, 1, 0, str.tostring(total_trades), text_color=color.white, bgcolor=color.gray)
    table.cell(t, 0, 1, "Win Rate", text_color=color.white, bgcolor=color.navy)
    table.cell(t, 1, 1, str.format("{0,number,0.00}%", win_rate), text_color=color.white, bgcolor=color.gray)
```

---

## 🎓 When to Remove Debug Code

Remove debug elements before deploying:
- [ ] log.info() calls (or keep 1-2 for monitoring)
- [ ] label.new() markers (except final summary)
- [ ] Extra plot() calls (keep main indicators)
- [ ] Test variables (used only for debugging)

Keep for production:
- [ ] Core plot() for main indicators
- [ ] One log.info() for entry/exit signals
- [ ] table with statistics
- [ ] bgcolor for entry/exit highlighting

---

**Last Updated**: 2026-05-05  
**Based On**: TradingView official debugging documentation  
**Status**: Comprehensive ✅
