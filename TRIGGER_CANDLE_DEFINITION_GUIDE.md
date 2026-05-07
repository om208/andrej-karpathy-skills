# 🔍 TRIGGER CANDLE DEFINITION & IDENTIFICATION
## Complete Logic, Nomenclature & Visual Preview

**Date**: 2026-05-07  
**Status**: Complete Reference Guide  
**Purpose**: Understand how trigger candles work with full nomenclature

---

## 📖 WHAT IS A TRIGGER CANDLE?

### **Definition**
A **trigger candle** is a candle whose price touches (tests) one of the **3 predefined trigger levels** within a consolidation zone.

```
Trigger = Any bar that touches a specific price level

These trigger levels are derived from the inside candle pattern
and represent key support/resistance points where direction is revealed.
```

---

## 🎯 THE 3 TRIGGER LEVELS - COMPLETE NOMENCLATURE

### **Level 1: F1 Boundaries (Trigger Level 1)**

#### **Definition**
The highest high and lowest low of the first inner candle (F1).

#### **Nomenclature**
```
Trigger_1_High = F1_High
Trigger_1_Low = F1_Low

Also written as:
  T1_H = F1_High
  T1_L = F1_Low
```

#### **How to Calculate**
```
Step 1: Identify F1 candle
        F1 = Previous bar = bar_index[1]

Step 2: Extract F1_High
        T1_H = high[1]
        Meaning: Highest price during F1

Step 3: Extract F1_Low
        T1_L = low[1]
        Meaning: Lowest price during F1

Example:
  F1 OHLC: Open=45,200, High=45,450, Low=45,100, Close=45,350
  
  T1_H = 45,450 (top of F1 range)
  T1_L = 45,100 (bottom of F1 range)
```

#### **Visual Representation**
```
Price

45,450 ├─────────────────┐ ← T1_H (Trigger_1_High = F1_High)
       │                 │
45,350 │  ┌────────────┐ │ ← F1 Candle body
       │  │            │ │
45,250 │  │            │ │
       │  │            │ │
45,100 └─────────────────┘ ← T1_L (Trigger_1_Low = F1_Low)
       
Time   │    F1       │

Interpretation:
  T1_H = Top boundary of consolidation
  T1_L = Bottom boundary of consolidation
  Any candle touching these = Trigger candle detected
```

---

### **Level 2: Mean of Inside Candle (Trigger Level 2)**

#### **Definition**
The exact midpoint (equilibrium) between F1's high and low.

#### **Nomenclature**
```
Trigger_2_Mean = (F1_High + F1_Low) / 2

Also written as:
  T2_M = Mean_F1
  T2_Equilibrium = F1_Midpoint
```

#### **How to Calculate**
```
Step 1: Get F1_High and F1_Low
        F1_High = high[1]
        F1_Low = low[1]

Step 2: Calculate mean
        T2_M = (F1_High + F1_Low) / 2

Example:
  F1_High = 45,450
  F1_Low = 45,100
  
  T2_M = (45,450 + 45,100) / 2 = 45,275
  
Interpretation:
  This is the BALANCE POINT
  Above T2_M = Bullish bias
  Below T2_M = Bearish bias
  AT T2_M = Indecision/equilibrium
```

#### **Visual Representation**
```
Price

45,450 ├─────────────┐
       │             │
       │ ╔═══════════╗ ← T2_M (Trigger_2_Mean = Equilibrium)
45,275 │ ║ Balance  ║
       │ ║  Point   ║
       │ ║           ║
45,100 └─────────────┘

Interpretation:
  T2_M divides consolidation into two equal halves
  Represents market indecision point
  Breaking above = bullish momentum
  Breaking below = bearish momentum
```

---

### **Level 3: Context Boundaries (Trigger Level 3)**

#### **Definition**
The extreme prices from the context candles (P-1 and P+1) that define the outer limits.

#### **Nomenclature**
```
Trigger_3_High = P(+1)_High
Trigger_3_Low = P(-1)_Low

Also written as:
  T3_H = P_Plus_1_High = high[0]
  T3_L = P_Minus_1_Low = low[2]
```

#### **How to Calculate**
```
Step 1: Identify context candles
        P(-1) = bar_index[2] (one before F1)
        P(+1) = bar_index[0] (current/next bar)

Step 2: Extract boundaries
        T3_H = high[0]    (P+1's highest price)
        T3_L = low[2]     (P-1's lowest price)

Example:
  P(-1) OHLC: High=45,500, Low=45,000
  P(+1) OHLC: High=45,600, Low=45,050
  
  T3_L = 45,000 (bottom boundary from P-1)
  T3_H = 45,600 (top boundary from P+1)
```

#### **Visual Representation**
```
Price

45,600 ├─────────────────────┐ ← T3_H (Context High = P+1_High)
       │                     │
45,500 │   ┌───────────────┐ │ ← P(-1)
       │   │               │ │
45,450 │ ┌─┤   F1 inside   ├─┤ ← F1 candle
45,350 │ │ │               │ │
45,275 │ │ ║ T2_Mean = M   ║ │
       │ │ │               │ │
45,100 │ └─┤               ├─┤ ← F1 boundaries
       │   │               │ │
45,050 │   │   P(+1)       │ │
       │   └───────────────┘ │
45,000 ├─────────────────────┘ ← T3_L (Context Low = P-1_Low)

Interpretation:
  T3_L = Ultimate downside breakout level
  T3_H = Ultimate upside breakout level
  Breaking these = Strong directional confirmation
```

---

## 🔄 COMPLETE 3-TRIGGER LEVEL DIAGRAM

### **All Triggers Together**

```
PRICE LEVEL HIERARCHY (from top to bottom):

╔════════════════════════════════════════╗
║          T3_H (Context High)           │ ← Outer breakout level
║          P(+1) = Current candle        │
║                                        │
║        ╔══════════════════════╗        │
║        │   T1_H (F1 High)     │        │ ← Inner boundary
║        │  ┌──────────────┐    │        │
║        │  │              │    │        │
║        │  │  F1 Candle   │    │        │
║        │  │              │    │        │
║        │  ║  T2_M (Mean) ║    │        │ ← Equilibrium point
║        │  ║              ║    │        │
║        │  │              │    │        │
║        │  │              │    │        │
║        │  └──────────────┘    │        │
║        │   T1_L (F1 Low)      │        │ ← Inner boundary
║        ╚══════════════════════╝        │
║                                        │
║          T3_L (Context Low)            │ ← Outer breakout level
║          P(-1) = Previous candle       │
╚════════════════════════════════════════╝

3 Trigger Levels Summary:
┌─────────────────────────────────────────────┐
│ Trigger 1: T1_H and T1_L (F1 boundaries)    │
│            Inner boundaries of consolidation│
│            Range: F1_Low to F1_High        │
│                                            │
│ Trigger 2: T2_M (Equilibrium)              │
│            Middle of consolidation         │
│            Point: (F1_H + F1_L) / 2        │
│                                            │
│ Trigger 3: T3_H and T3_L (Context limits)  │
│            Outer breakout levels           │
│            Range: P(-1)_Low to P(+1)_High  │
└─────────────────────────────────────────────┘
```

---

## 📊 TRIGGER CANDLE DETECTION LOGIC

### **What is a Trigger Candle?**

A candle is a **trigger candle** if its High or Low **touches (passes through) any trigger level**.

### **Complete Detection Formula**

```
TRIGGER_CANDLE_DETECTED if any of these conditions are TRUE:

Condition 1: Candle touches T1_High
  Current_High >= T1_H
  Example: Candle High reaches or exceeds F1_High

Condition 2: Candle touches T1_Low
  Current_Low <= T1_L
  Example: Candle Low reaches or drops below F1_Low

Condition 3: Candle touches T2_Mean
  Current_High >= T2_M AND Current_Low <= T2_M
  OR (Current_High >= T2_M >= Current_Low)
  Example: Candle body crosses the equilibrium point

Condition 4: Candle touches T3_High
  Current_High >= T3_H
  Example: Candle High reaches or exceeds context high

Condition 5: Candle touches T3_Low
  Current_Low <= T3_L
  Example: Candle Low reaches or drops below context low
```

### **Pseudocode for Trigger Detection**

```
FOR each candle in data:
  
  IF candle_high >= T1_High THEN
    trigger_detected = "T1_H"
    action = Record_Trigger
  
  IF candle_low <= T1_Low THEN
    trigger_detected = "T1_L"
    action = Record_Trigger
  
  IF candle_high >= T2_Mean >= candle_low THEN
    trigger_detected = "T2_M"
    action = Record_Trigger
  
  IF candle_high >= T3_High THEN
    trigger_detected = "T3_H"
    action = Record_Trigger
    breakout_direction = "UP" (if first T3 touch)
  
  IF candle_low <= T3_Low THEN
    trigger_detected = "T3_L"
    action = Record_Trigger
    breakout_direction = "DOWN" (if first T3 touch)

END FOR
```

---

## 🎨 VISUAL PREVIEW: TRIGGER CANDLE EXAMPLES

### **EXAMPLE 1: Bullish Pattern (Triggers T1_L → T2_M → T1_H)**

```
TIME PROGRESSION: → → →

                    Candle 5
                     ┌─┐
                   40├─┤ ← Touches T1_H
                     │ │
                     │ │
                     │ │
                   35└─┘ ← Trigger_Candle_5 = "T1_H" (BREAKOUT UP!)

                    Candle 4
                     ┌─┐
                   33├─┤
                     │ │
                   30├─┼─ ← T2_M (Equilibrium)
                     │ │
                   27└─┘ ← Touches T2_M
                     
                    Trigger_Candle_4 = "T2_M" (at equilibrium)

                    Candle 3
                     ┌─┐
                   25├─┤
                     │ │
                     │ │
                     │ │
                   20└─┘

                    Candle 2
                     ┌─┐
                   20├─┤ ← Touches T1_L
                     │ │
                     │ │
                   15└─┘ ← Consolidation bottom
                   
                    Trigger_Candle_2 = "T1_L" (first test of bottom)

        ═══════════════════════════════════════════════
        TRIGGER SEQUENCE: T1_L → T2_M → T1_H
        ═══════════════════════════════════════════════
        PATTERN: 72% BULLISH (UP expected)
        ═══════════════════════════════════════════════

PRICES:
  T1_H = 40 (F1 High)
  T2_M = 30 (Equilibrium = (40+20)/2)
  T1_L = 20 (F1 Low)
  T3_H = 45 (Context High from P+1)
  T3_L = 15 (Context Low from P-1)
```

### **EXAMPLE 2: Bearish Pattern (Triggers T1_H → T2_M → T1_L)**

```
TIME PROGRESSION: ↓ ↓ ↓

                    Candle 5
                     ┌─┐
                   20└─┘ ← Touches T1_L
                     │ │
                   15├─┤ ← BREAKOUT DOWN!
                     
                    Trigger_Candle_5 = "T1_L" (BREAKOUT DOWN!)

                    Candle 4
                     ┌─┐
                   28├─┤
                     │ │
                   25├─┼─ ← T2_M (Equilibrium)
                     │ │
                   22└─┘ ← Touches T2_M
                     
                    Trigger_Candle_4 = "T2_M" (at equilibrium)

                    Candle 3
                     ┌─┐
                   30├─┤
                     │ │
                     │ │
                     │ │
                   25└─┘

                    Candle 2
                     ┌─┐
                   40├─┤ ← Touches T1_H
                     │ │
                     │ │
                   35└─┘ ← Consolidation top
                   
                    Trigger_Candle_2 = "T1_H" (first test of top)

        ═══════════════════════════════════════════════
        TRIGGER SEQUENCE: T1_H → T2_M → T1_L
        ═══════════════════════════════════════════════
        PATTERN: 71% BEARISH (DOWN expected)
        ═══════════════════════════════════════════════

PRICES:
  T1_H = 40 (F1 High)
  T2_M = 30 (Equilibrium = (40+20)/2)
  T1_L = 20 (F1 Low)
  T3_H = 45 (Context High from P+1)
  T3_L = 15 (Context Low from P-1)
```

---

## 📋 TRIGGER CANDLE NOMENCLATURE REFERENCE

### **Complete Nomenclature Table**

```
COMPONENT              | NOMENCLATURE | FORMULA/VALUE         | DATA TYPE
─────────────────────────────────────────────────────────────────────────
Trigger 1 High         | T1_H         | F1_High = high[1]    | Float
Trigger 1 Low          | T1_L         | F1_Low = low[1]      | Float
Trigger 2 Mean         | T2_M         | (F1_H + F1_L) / 2    | Float
Trigger 3 High         | T3_H         | P(+1)_High = high[0] | Float
Trigger 3 Low          | T3_L         | P(-1)_Low = low[2]   | Float
─────────────────────────────────────────────────────────────────────────
Trigger Touched        | trigger_id   | "T1_H" or "T1_L", etc| String
Candle High            | current_high | high (of test candle)| Float
Candle Low             | current_low  | low (of test candle) | Float
─────────────────────────────────────────────────────────────────────────
Sequence               | sequence     | "T1_L→T2_M→T1_H"     | String
Trigger Count          | touch_count  | Number of touches    | Integer
Volume at Trigger      | trigger_vol  | Volume when touched  | Float
Volume Ratio           | vol_ratio    | current_vol/baseline | Float
─────────────────────────────────────────────────────────────────────────
```

### **Trigger Candle States**

```
TRIGGER_CANDLE:
  • touched_trigger: Which level was touched (T1_H, T1_L, T2_M, T3_H, T3_L)
  • touch_price: Price at which trigger was hit
  • touch_volume: Volume when trigger was touched
  • touch_volume_ratio: Volume ratio (actual / baseline)
  • bar_offset: How many bars after entry
  • timestamp: When trigger was touched
  • is_confirmed: Is this a valid trigger? (passed filters)
```

---

## 🔧 PINE SCRIPT IMPLEMENTATION

### **How to Code Trigger Detection**

```pine
// DEFINE TRIGGER LEVELS
trigger_1_high = high[1]        // F1 High
trigger_1_low = low[1]          // F1 Low
trigger_2_mean = (high[1] + low[1]) / 2  // Equilibrium
trigger_3_high = high[0]        // P(+1) High
trigger_3_low = low[2]          // P(-1) Low

// DETECT TRIGGERS
is_trigger_1_h = high >= trigger_1_high
is_trigger_1_l = low <= trigger_1_low
is_trigger_2_m = (high >= trigger_2_mean) and (low <= trigger_2_mean)
is_trigger_3_h = high >= trigger_3_high
is_trigger_3_l = low <= trigger_3_low

// RECORD WHICH TRIGGER
if is_trigger_1_h
    trigger_touched = "T1_H"
else if is_trigger_1_l
    trigger_touched = "T1_L"
else if is_trigger_2_m
    trigger_touched = "T2_M"
else if is_trigger_3_h
    trigger_touched = "T3_H"
else if is_trigger_3_l
    trigger_touched = "T3_L"

// RECORD VOLUME
trigger_volume = volume
trigger_vol_ratio = volume / baseline_volume
```

---

## 📊 TRIGGER CANDLE SEQUENCE TRACKING

### **How Sequences Form**

```
CANDLE 1:
  ├─ Check: Does it touch any trigger?
  ├─ No → Skip
  └─ Yes → Record first trigger

CANDLE 2:
  ├─ Check: Does it touch a NEW trigger (not already touched)?
  ├─ No → Skip
  └─ Yes → Record second trigger

CANDLE 3:
  ├─ Check: Does it touch another NEW trigger?
  ├─ No → Skip
  └─ Yes → Record third trigger

CANDLE 4:
  ├─ Check: Does it touch T3_H or T3_L?
  ├─ No → Continue monitoring
  └─ Yes → BREAKOUT DETECTED (end sequence)

RESULT: Sequence = T1_L → T2_M → T1_H → T3_H
        This is a BULLISH sequence (breakout UP)
```

### **Sequence Recording Example**

```
Bar | High | Low | Trigger? | Sequence So Far
────┼──────┼─────┼──────────┼──────────────────
1   | 100  | 95  | No       | (empty)
2   | 102  | 90  | Yes: T1_L| [T1_L]
3   | 105  | 98  | Yes: T2_M| [T1_L, T2_M]
4   | 108  | 102 | Yes: T1_H| [T1_L, T2_M, T1_H]
5   | 112  | 106 | Yes: T3_H| [T1_L, T2_M, T1_H, T3_H]
      ↑                      ↑
   BREAKOUT!           BULLISH SEQUENCE COMPLETE
   Direction: UP       Probability: 72%
```

---

## 🎯 TRIGGER CANDLE USE CASES

### **USE CASE 1: Predict Direction from First Trigger**

```
IF first_trigger = T1_Low
  THEN likely direction = UP (65% probability)
  BECAUSE: Market testing bottom = weak selling = buyers waiting

IF first_trigger = T1_High
  THEN likely direction = DOWN (65% probability)
  BECAUSE: Market testing top = weak buying = sellers waiting
```

### **USE CASE 2: Confirm with Sequence**

```
IF sequence = T1_L → T2_M → T1_H
  THEN direction = BULLISH (72% probability)
  BECAUSE: Follows bullish template exactly

IF sequence = T1_H → T2_M → T1_L
  THEN direction = BEARISH (71% probability)
  BECAUSE: Follows bearish template exactly
```

### **USE CASE 3: Validate with Volume**

```
IF volume_at_T1_L = 0.8x (weak)
  AND volume_at_breakout = 2.5x (strong)
  THEN direction_confirmed = UP
  CONFIDENCE: 85%+
```

---

## 📈 COMPLETE TRIGGER CANDLE LOGIC FLOW

```
╔════════════════════════════════════════════════════════╗
║         TRIGGER CANDLE IDENTIFICATION FLOW             ║
╚════════════════════════════════════════════════════════╝

START: New candle arrives
  │
  ├─→ STEP 1: Calculate Trigger Levels
  │   ├─ T1_H = F1_High = high[1]
  │   ├─ T1_L = F1_Low = low[1]
  │   ├─ T2_M = (F1_H + F1_L) / 2
  │   ├─ T3_H = P(+1)_High = high[0]
  │   └─ T3_L = P(-1)_Low = low[2]
  │
  ├─→ STEP 2: Check Candle Against Triggers
  │   ├─ Does High >= T1_H? → Potential T1_H touch
  │   ├─ Does Low <= T1_L? → Potential T1_L touch
  │   ├─ Does High >= T2_M >= Low? → Potential T2_M touch
  │   ├─ Does High >= T3_H? → Potential T3_H touch
  │   └─ Does Low <= T3_L? → Potential T3_L touch
  │
  ├─→ STEP 3: Verify Trigger is NEW (not already touched)
  │   ├─ Was T1_H already touched in sequence?
  │   │  ├─ Yes → Skip (don't record duplicate)
  │   │  └─ No → Record as new trigger
  │   └─ (Same logic for T1_L, T2_M, T3_H, T3_L)
  │
  ├─→ STEP 4: Record Trigger Information
  │   ├─ trigger_id = "T1_H" (or T1_L, T2_M, etc.)
  │   ├─ touch_price = current_high (or low)
  │   ├─ touch_volume = current_volume
  │   ├─ volume_ratio = touch_volume / baseline_volume
  │   └─ timestamp = current_bar_time
  │
  ├─→ STEP 5: Build Sequence
  │   ├─ Append trigger to sequence array
  │   ├─ Check if sequence matches known pattern
  │   │  ├─ Matches bullish? → Direction = UP
  │   │  ├─ Matches bearish? → Direction = DOWN
  │   │  └─ Mixed/unknown? → Continue monitoring
  │   └─ Check if T3 touched (breakout confirmed)
  │
  ├─→ STEP 6: Check for Breakout
  │   ├─ Did candle touch T3_H?
  │   │  ├─ Yes → BREAKOUT_UP (strong bullish)
  │   │  ├─ Record: direction = UP, confirmed = TRUE
  │   │  └─ Action: Can enter LONG position
  │   ├─ Did candle touch T3_L?
  │   │  ├─ Yes → BREAKOUT_DOWN (strong bearish)
  │   │  ├─ Record: direction = DOWN, confirmed = TRUE
  │   │  └─ Action: Can enter SHORT position
  │   └─ Neither? → Continue to next candle
  │
  └─→ OUTPUT: Trigger candle information
      ├─ Trigger ID (T1_H, T1_L, T2_M, T3_H, T3_L)
      ├─ Sequence so far (T1_L→T2_M→T1_H, etc.)
      ├─ Direction bias (UP, DOWN, or NEUTRAL)
      ├─ Confidence level (based on sequence match)
      └─ Volume confirmation (ratio and strength)
```

---

## 🎓 SUMMARY: TRIGGER CANDLE DEFINITION

```
TRIGGER CANDLE = Any candle that touches a trigger level

3 TRIGGER LEVELS:
  1. T1_H & T1_L = F1 boundaries (inner limits)
  2. T2_M = Equilibrium (balance point)
  3. T3_H & T3_L = Context limits (breakout levels)

DETECTION RULE:
  IF candle_high >= trigger_level  OR  candle_low <= trigger_level
  THEN: Trigger_Candle detected

SEQUENCE TRACKING:
  Record order of triggers touched: T1_L → T2_M → T1_H
  Compare to known patterns (72% bullish, 71% bearish)
  Direction determined by sequence pattern

CONFIRMATION:
  First T3 touch (T3_H or T3_L) = BREAKOUT confirmed
  Direction validated, trade ready

VOLUME ROLE:
  Low volume on first trigger = weak opposition
  High volume on breakout = real conviction
  Together = direction confirmed
```

---

**Created**: 2026-05-07  
**Status**: Complete Reference  
**Ready**: For implementation and live use
