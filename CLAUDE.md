# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 5. Self-Healing Trading System Principles

**Automatic problem detection, diagnosis, and correction in backtesting.**

The backtesting system incorporates self-healing capabilities inspired by trading system resilience:

### Core Principles

1. **Auto-Detection** - Monitor performance metrics in real-time
   - Win rate tracking (target: 65-75%+)
   - Profit factor analysis (target: 1.5+)
   - Loss pattern detection
   - Trade timing analysis
   - Confluence factor evaluation

2. **Health Status Levels**
   - 🟢 **GREEN**: Win rate 75%+, Profit Factor >1.5 → Continue as is
   - 🟡 **YELLOW**: Win rate 65-75%, PF >1.0 → Minor adjustments
   - 🟠 **ORANGE**: Win rate 55-65% → Needs attention
   - 🔴 **RED**: Win rate <55% → Emergency healing

3. **Automatic Diagnosis** (When problems detected)
   - Segment data by pattern type, time, confluence factors
   - Compare problem periods to healthy periods
   - Identify which specific rules were violated
   - Quantify the impact of each issue

4. **Auto-Correction Protocol**
   - **Level 1** (Minor): Tighten requirements (+3-8% improvement)
   - **Level 2** (Moderate): Remove problem patterns temporarily (+10-15%)
   - **Level 3** (Severe): Reset to proven baseline, rebuild confidence

5. **Prevention Before Trades**
   - Pre-entry checks: Confluence factor count, time window, volume confirmation
   - Pattern quality verification
   - Market condition assessment
   - Emotional control rules (max 3 losses in a row → halt)

### Backtesting System Integration

Each backtest automatically:
- ✅ Generates detailed performance metrics
- ✅ Identifies underperforming patterns
- ✅ Diagnoses root causes
- ✅ Recommends corrections
- ✅ Produces action items for strategy improvement

### Example Self-Healing Workflow

```
Week 1: Backtest shows 60% win rate (below 65% target)
├─ Diagnosis: Too many low-confluence entries (2-3 factors)
├─ Correction: Require minimum 4 confluence factors
└─ Expected result: Win rate improves to 68%

Week 2: After adjustment, win rate at 68%
├─ Diagnosis: Pattern X underperforming (45% vs 70% overall)
├─ Correction: Restrict or remove pattern X
└─ Expected result: Win rate improves to 75%+

Week 3: System stabilizes at 75%+ win rate
├─ Diagnosis: System healthy
├─ Action: Maintain rules, optimize position sizing
└─ Result: Consistent profitability
```

### How to Use in Backtesting

1. Create a new strategy by inheriting from `Strategy` base class
2. Implement `generate_signals()` and `backtest()` methods
3. Define your own take-profit logic per strategy
4. Run backtest - self-healing system will analyze automatically
5. Review report for corrections and implement improvements
6. Iterate weekly until system reaches GREEN status

See `/backtesting/` directory for examples and implementation details.
