# Pine Script Performance Optimization

**Purpose**: Techniques to optimize script execution speed and avoid timeouts.

**Last Updated**: 2026-05-05

---

## ⚡ Performance Goals

**Target**:
- Script completes in < 1 second per bar
- Can handle 10+ years of historical data
- No timeouts on standard timeframes (1m to 1D)

**Indicators of Problems**:
- Script takes > 5 seconds to compile
- Gaps in chart display (script timeout)
- "Script timeout" error messages
- Backtesting stops unexpectedly

---

## 🎯 Optimization Techniques

### 1. Minimize request.security() Calls (Highest Impact)

**Problem**: Each request.security() call is expensive

```pine
// ❌ WRONG - 4 separate calls per bar
high_mtf = request.security(sym, tf, high)
low_mtf = request.security(sym, tf, low)
close_mtf = request.security(sym, tf, close)
sma_mtf = request.security(sym, tf, ta.sma(close, 20))
// 4 calls × 100 bars × 10 years = 4 million calls!

// ✅ CORRECT - 1 call with array return
[high_mtf, low_mtf, close_mtf, sma_mtf] = request.security(sym, tf, 
    [high, low, close, ta.sma(close, 20)])
// 1 call × 100 bars × 10 years = 100k calls
```

**Impact**: 40x performance improvement possible

**Rule**: Combine all security() calls into one per timeframe/symbol

---

### 2. Cache Calculations in Variables

**Problem**: Recalculating same values repeatedly

```pine
// ❌ WRONG - Calculated 3 times
if close > sma and close > sma and rsi < ta.rsi(close, 14)
    strategy.entry("Long", strategy.long)

// ✅ CORRECT - Calculate once, reuse
rsi_val = ta.rsi(close, 14)
sma_val = ta.sma(close, 20)
if close > sma_val and rsi_val < 50
    strategy.entry("Long", strategy.long)
```

**Impact**: Small but measurable improvement

---

### 3. Optimize Loops

**Problem 1**: Too many iterations
```pine
// ❌ WRONG - 1000 iterations per bar
for i = 0 to 1000
    x = close[i]
    // Process 1000 bars per bar

// ✅ CORRECT - Only needed data
for i = 0 to 50  // Last 50 bars only
    x = close[i]
```

**Problem 2**: Expensive operations in loops
```pine
// ❌ WRONG - request.security in loop
for i = 0 to 100
    val = request.security(sym, tf, close[i])
    // 100 security calls per bar!

// ✅ CORRECT - Get data once, iterate
mtf_data = request.security(sym, tf, close)
for i = 0 to 100
    process_value(mtf_data)  // Just iterate
```

**Impact**: 100x improvement possible

---

### 4. Use Efficient Data Structures

**Problem**: Inefficient operations on large arrays
```pine
// ❌ WRONG - O(n²) complexity
for i = 0 to array.size(arr1)
    for j = 0 to array.size(arr2)
        compare(arr1[i], arr2[j])  // Nested loops

// ✅ CORRECT - O(n) solution
for i = 0 to math.min(array.size(arr1), array.size(arr2))
    compare(arr1[i], arr2[i])  // Single pass
```

**Impact**: Scales with data size

---

### 5. Minimize Indicator Calculations

**Problem**: Too many indicator calls
```pine
// ❌ WRONG - 5 RSI calculations
rsi1 = ta.rsi(close, 14)
rsi2 = ta.rsi(close, 21)
rsi3 = ta.rsi(close[1], 14)  // On previous bar
rsi4 = ta.rsi(high, 14)
rsi5 = ta.rsi(low, 14)

// ✅ CORRECT - Calculate what you need
rsi_close_14 = ta.rsi(close, 14)
rsi_close_21 = ta.rsi(close, 21)

// If needed: cache previous value
var float rsi_prev = 0.0
rsi_prev := rsi_close_14[1]
```

**Impact**: Depends on indicator complexity

---

## 🔍 Performance Monitoring

### Enable Pine Profiler

```pine
// Add to top of script
//@version=5
strategy("Strategy", overlay=true)
// Pine Profiler automatically runs

// View results:
// 1. Run script
// 2. Pine Editor > Settings > Show Report
// 3. Check execution times per function
```

**What to Look For**:
- Which functions take most time?
- Any > 100ms calls?
- request.security() efficiency?
- Loop iteration counts?

---

## 📊 Optimization Checklist

### High Priority (Do These First)
- [ ] Combine request.security() calls into arrays
- [ ] Remove unnecessary security() calls entirely
- [ ] Cache indicator values in variables
- [ ] Limit loop iterations to needed data only
- [ ] Check nested loop complexity

### Medium Priority (Nice to Have)
- [ ] Use efficient calculations (avoid sqrt, etc if possible)
- [ ] Minimize array operations in tight loops
- [ ] Pre-calculate static values
- [ ] Cache previous bar values with var

### Low Priority (Minor Impact)
- [ ] Optimize variable naming
- [ ] Reduce string operations
- [ ] Minimize bgcolor() calls
- [ ] Clean up unused variables

---

## 🚀 Before & After Example

### Before Optimization
```pine
//@version=5
strategy("Unoptimized Strategy", overlay=true)

fast_sma = ta.sma(close, 20)
slow_sma = ta.sma(close, 50)
rsi = ta.rsi(close, 14)

mtf_fast = request.security(syminfo.tickerid, "60", ta.sma(close, 20))
mtf_slow = request.security(syminfo.tickerid, "60", ta.sma(close, 50))
mtf_rsi = request.security(syminfo.tickerid, "60", ta.rsi(close, 14))

if fast_sma > slow_sma and rsi < 50
    strategy.entry("Long", strategy.long)

if fast_sma < slow_sma
    strategy.close("Long")

plot(fast_sma)
plot(slow_sma)
plot(mtf_fast)
plot(mtf_slow)
```

**Issues**:
- 3 separate security() calls
- No caching of previous values
- No optimization

**Execution**: ~500ms per bar on 10-year data

---

### After Optimization
```pine
//@version=5
strategy("Optimized Strategy", overlay=true)

// Single security call with array
[mtf_fast, mtf_slow, mtf_rsi] = request.security(syminfo.tickerid, "60", 
    [ta.sma(close, 20), ta.sma(close, 50), ta.rsi(close, 14)])

// Cache current timeframe indicators
fast_sma = ta.sma(close, 20)
slow_sma = ta.sma(close, 50)
rsi = ta.rsi(close, 14)

// Simple, direct conditions
if fast_sma > slow_sma and rsi < 50
    strategy.entry("Long", strategy.long)

if fast_sma < slow_sma
    strategy.close("Long")

// Minimal plotting
plot(fast_sma, title="Fast SMA", color=color.blue)
plot(slow_sma, title="Slow SMA", color=color.red)
```

**Improvements**:
- Combined 3 security() calls into 1
- Cached calculations
- Removed unnecessary plots

**Execution**: ~100ms per bar on 10-year data

**Result**: 5x faster ⚡

---

## ⚠️ Performance Red Flags

| Red Flag | Cause | Fix |
|----------|-------|-----|
| Script timeout on backtest | Too much calculation | Reduce security() calls, optimize loops |
| Takes > 5 seconds to compile | Heavy processing | Enable Pine Profiler, find bottleneck |
| Gaps in chart (bars missing) | Script timeout per bar | Same as above |
| > 100ms per bar execution | Inefficient code | Check Profiler report |
| Multiple request.security() calls | Redundant calls | Combine into array |

---

## 📈 Scalability Guidelines

**Safe Limits**:
- request.security() calls: < 10 per bar
- Loop iterations: < 1000 total per bar
- Array size: < 10,000 elements
- Historical data: 10+ years
- Indicator calculations: < 5 different moving averages

**Exceeding Limits**:
- Causes script timeout
- Backtesting may fail
- Real-time updates may lag
- Not suitable for production

---

## 💾 Memory Management

### Arrays Best Practices
```pine
// Delete old entries to save memory
var array<label> labels = array.new<label>()

if signal_detected
    array.push(labels, label.new(...))
    
    // Keep only last 50 labels
    while array.size(labels) > 50
        label.delete(array.shift(labels))
```

### Variable Scope
```pine
// Use local variables when possible
if condition
    temp_value = expensive_calculation()  // Only calculated if needed

// vs

// Global variables persist in memory
var persistent_value = expensive_calculation()  // Always in memory
```

---

**Last Updated**: 2026-05-05  
**Based On**: TradingView performance best practices  
**Status**: Complete ✅
