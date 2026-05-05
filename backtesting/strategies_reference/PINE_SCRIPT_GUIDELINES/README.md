# Pine Script Strategy Writing Guidelines

**Purpose**: Central repository for official TradingView documentation, best practices, error prevention methods, and proven patterns for writing error-free Pine Script strategies.

**Updated**: 2026-05-05  
**Version**: 1.0 (Based on Pine Script v5 & v6 official documentation)

---

## 📚 Quick Links to Resources

- **[Official Documentation Links](./OFFICIAL_REFERENCES.md)** - Direct links to TradingView docs and quality resources
- **[Writing Standards & Best Practices](./PINE_SCRIPT_BEST_PRACTICES.md)** - Code style, naming conventions, structure
- **[Common Mistakes & Fixes](./COMMON_MISTAKES_AND_FIXES.md)** - 10+ common errors and how to prevent them
- **[Debugging Guide](./DEBUGGING_GUIDE.md)** - Tools and techniques for debugging Pine Script
- **[Strategy Writing Checklist](./STRATEGY_WRITING_CHECKLIST.md)** - Step-by-step verification before deployment
- **[Performance Optimization](./PERFORMANCE_OPTIMIZATION.md)** - Optimization techniques to avoid timeouts

---

## 🎯 Core Principles

### 1. **Test Small, Iterate Frequently**
- Write 5-10 lines of code, then test immediately
- Don't write 50 lines and hope it compiles
- Isolate errors before they compound

### 2. **Use Official Templates**
- Reference working strategies from `/strategies_reference/`
- Never start from scratch
- Proven patterns = fewer errors

### 3. **Apply Syntax Rules (L-01 through L-06)**
See `PINE_SCRIPT_BEST_PRACTICES.md` for detailed explanation:
- **L-01**: Single-line strategy() declaration
- **L-02**: Consistent 4-space indentation blocks
- **L-03**: Single-line ternary operators
- **L-04**: Single-line drawing functions
- **L-05**: plot() only in global scope
- **L-06**: Proper parameter handling

### 4. **Always Include Risk Management**
- Define stop-loss levels
- Set position sizing rules
- Track maximum drawdown
- Implement profit targets

### 5. **Backtest with Realistic Settings**
- Commission rates matching your broker
- Slippage (1-2 pips typical)
- Appropriate position sizes
- Test across multiple market conditions (bull, bear, sideways)

### 6. **Avoid Over-Optimization**
- Use out-of-sample testing
- Test across different timeframes
- Validate on different asset classes
- Don't curve-fit historical data

---

## 📋 File Structure

```
PINE_SCRIPT_GUIDELINES/
├── README.md (this file)
├── OFFICIAL_REFERENCES.md          # Links to TradingView docs
├── PINE_SCRIPT_BEST_PRACTICES.md   # Style guide, standards, structure
├── COMMON_MISTAKES_AND_FIXES.md    # 10+ errors and solutions
├── DEBUGGING_GUIDE.md               # Debugging tools and techniques
├── STRATEGY_WRITING_CHECKLIST.md   # Pre-deployment verification
├── PERFORMANCE_OPTIMIZATION.md      # Speed optimization tips
└── SYNTAX_RULES_L01_L06.md         # Detailed syntax rules with examples
```

---

## 🚀 Workflow: Using These Guidelines

### When Building a New Strategy:
1. Read `STRATEGY_WRITING_CHECKLIST.md` first
2. Select a similar **working strategy** from `/strategies_reference/`
3. Reference `PINE_SCRIPT_BEST_PRACTICES.md` while coding
4. Review `SYNTAX_RULES_L01_L06.md` for each code block
5. Run through `COMMON_MISTAKES_AND_FIXES.md` before testing
6. Use `DEBUGGING_GUIDE.md` if errors occur
7. Check `PERFORMANCE_OPTIMIZATION.md` before deployment

### When Debugging:
1. Check error message against `COMMON_MISTAKES_AND_FIXES.md`
2. Use techniques from `DEBUGGING_GUIDE.md`
3. Reference `SYNTAX_RULES_L01_L06.md` for structure issues
4. Verify against `STRATEGY_WRITING_CHECKLIST.md`

---

## 🔑 Key Statistics from Documentation

### Common Issues Breakdown
- **Syntax Errors**: ~70% of reported issues
- **Runtime Errors**: Exceeding limits (security calls, loops)
- **Logical Errors**: Incorrect series data handling, off-by-one errors

### Most Common Mistakes
1. Using [1] instead of [0] (or vice versa)
2. Undeclared identifiers (misspelled variables)
3. Wrong data types passed to functions
4. Calculations returning `na` on first bars
5. Entries/exits firing on same candle
6. Too many request.security() calls
7. Missing na() checks
8. Incorrect historical indexing
9. Assignment (=) instead of comparison (==)
10. plot() in nested if blocks (scope violation)

---

## 📊 Quality Targets

### For Reference Strategies:
- **Compilation Errors**: 0
- **Syntax Pass Rate**: 100%
- **Scope Violations**: 0
- **Code Quality Score**: 9/10+

### For Backtesting Results:
- **Win Rate**: 65%+ for first lot, 55%+ for second lot
- **Profit Factor**: 1.5+
- **Maximum Drawdown**: 15-20%
- **Data Coverage**: Minimum 1 year

---

## 🛠️ Tools Available

### Debugging Tools:
- `plot()` - Visual indicators on chart
- `label.new()` - Annotate specific bars
- `Pine Logs` (log.info(), log.warning(), log.error()) - Structured debugging

### Backtesting:
- Strategy Tester tab for performance analysis
- Bar Magnifier for detailed intrabar fills (Premium+)
- Walk-forward testing for validation

### Performance Analysis:
- Pine Profiler - Identifies bottlenecks
- Pine Editor - Code compilation and validation

---

## 📖 How to Use This Reference Library

**When you need to write a strategy:**
1. Find a similar working strategy in `/strategies_reference/`
2. Understand its structure using the Reference Guide
3. Copy its template structure
4. Follow the patterns in `PINE_SCRIPT_BEST_PRACTICES.md`
5. Reference `COMMON_MISTAKES_AND_FIXES.md` to avoid errors
6. Complete the `STRATEGY_WRITING_CHECKLIST.md` before testing

**This approach ensures:**
- ✅ Error-free code first time
- ✅ Consistent structure across strategies
- ✅ Fast development using proven patterns
- ✅ Higher quality output

---

## 🔄 Continuous Improvement

This guidelines folder is designed to evolve as new patterns are discovered and new Pine Script versions released. When you create a new working strategy:
1. Document the pattern used
2. Add examples to the appropriate guideline file
3. Update this README with new insights
4. Share with team for consistency

---

## 📞 Quick Reference

**Need help with**:
- **Syntax errors?** → `SYNTAX_RULES_L01_L06.md`
- **Scope violations?** → `COMMON_MISTAKES_AND_FIXES.md` (Error #10)
- **Won't compile?** → `DEBUGGING_GUIDE.md`
- **Slow script?** → `PERFORMANCE_OPTIMIZATION.md`
- **Writing a new strategy?** → `STRATEGY_WRITING_CHECKLIST.md`
- **Official docs?** → `OFFICIAL_REFERENCES.md`

---

**Last Updated**: 2026-05-05  
**Status**: Production Ready ✅
