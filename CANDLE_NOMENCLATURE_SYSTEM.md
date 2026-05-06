# 📝 CANDLE NOMENCLATURE SYSTEM
## Official Naming Convention for Inside Bar + SMA(196) + Confluence Strategy

**Status**: Official Standard ✅  
**Date**: 2026-05-06  
**Version**: v1.0

---

## 🎯 PRIMARY CANDLES (Entry Pattern Detection)

### **C0 - REFERENCE/SETUP CANDLE**
```
Definition: Previous bar (one bar before entry candidate)
Pine Script: High[1], Low[1], Open[1], Close[1]
Time Index: bar_index - 1
Purpose: Provides the containment boundaries for inside bar pattern
Role: Reference frame for all measurements

Components:
  C0_High = High[1]
  C0_Low = Low[1]
  C0_Open = Open[1]
  C0_Close = Close[1]
  C0_Body = |C0_Close - C0_Open|
  C0_Range = C0_High - C0_Low
  C0_MidPoint = (C0_High + C0_Low) / 2

Example (BTC/USD 1-min):
  C0_High = 45,500
  C0_Low = 45,200
  C0_Range = 300 pips
  ✓ Used as container for C1
```

---

### **C1 - INSIDE CANDLE (Entry Trigger Candle)**
```
Definition: Current bar (the candidate for inside bar breakout)
Pine Script: High, Low, Open, Close
Time Index: bar_index (current)
Purpose: The actual inside bar pattern candle
Role: Triggers entry signal when conditions met

Components:
  C1_High = High
  C1_Low = Low
  C1_Open = Open
  C1_Close = Close
  C1_Body = |C1_Close - C1_Open|
  C1_Range = C1_High - C1_Low
  C1_MidPoint = (C1_High + C1_Low) / 2

INSIDE BAR CONDITION:
  ✓ C1_High < C0_High
  ✓ C1_Low > C0_Low
  
Meaning: C1 is completely contained within C0

Example (BTC/USD 1-min):
  C1_High = 45,450
  C1_Low = 45,350
  C1_Range = 100 pips
  
  Check: 45,450 < 45,500? ✓ YES
  Check: 45,350 > 45,200? ✓ YES
  → is_inside_bar = TRUE ✓
```

---

## 🔗 CONTEXT CANDLES (Support/Resistance Reference)

### **C_Highest20 - 20-BAR RESISTANCE CANDLE**
```
Definition: Candle with the highest high in last 20 bars
Pine Script: ta.highest(high, 20)
Time Index: Variable (wherever the highest occurred)
Purpose: Identifies resistance level for S/R validation
Role: Reference for "is_near_resistance" check

Components:
  C_H20_High = ta.highest(high, 20)
  C_H20_Level = Current resistance (used for proximity check)
  
Proximity Check:
  is_near_resistance = (C1_High > C_H20_Level - ATR×0.5) AND
                       (C1_High < C_H20_Level + ATR×0.5)

Example:
  C_H20_Level = 45,600
  ATR = 100 pips
  Range: 45,550 to 45,650
  Is C1_High(45,450) in range? ✗ NO
  → Near resistance = FALSE
```

---

### **C_Lowest20 - 20-BAR SUPPORT CANDLE**
```
Definition: Candle with the lowest low in last 20 bars
Pine Script: ta.lowest(low, 20)
Time Index: Variable (wherever the lowest occurred)
Purpose: Identifies support level for S/R validation
Role: Reference for "is_near_support" check

Components:
  C_L20_Low = ta.lowest(low, 20)
  C_L20_Level = Current support (used for proximity check)
  
Proximity Check:
  is_near_support = (C1_Low < C_L20_Level + ATR×0.5) AND
                    (C1_Low > C_L20_Level - ATR×0.5)

Example:
  C_L20_Level = 45,100
  ATR = 100 pips
  Range: 45,050 to 45,150
  Is C1_Low(45,350) in range? ✗ NO
  → Near support = FALSE
```

---

## 📊 DERIVED CANDLE METRICS

### **Compression Ratio (C1 vs C0)**
```
Nomenclature: COMP_Ratio
Definition: How much C1 compressed relative to C0
Formula: COMP_Ratio = C1_Range / C0_Range
Range: 0.0 to 1.0+ (1.0 means equal size)
Target: < 0.5 (50% compression)

Example:
  C0_Range = 300 pips
  C1_Range = 100 pips
  COMP_Ratio = 100 / 300 = 0.333
  Is 0.0 ≤ 0.333 ≤ 1.0? ✓ YES
  → Compression valid ✓
```

---

### **SMA Confluence (C1 vs SMA Line)**
```
Nomenclature: SMA_196
Definition: 196-period Simple Moving Average
Formula: SMA_196 = Sum(Close[last 196 bars]) / 196
Purpose: Trend confirmation reference

Threshold Calculation:
  SMA_Threshold = C1_Range × (2.0 / 100)
  
Confluence Check:
  sma_touches = (SMA_196 ≥ C1_Low - SMA_Threshold) AND
                (SMA_196 ≤ C1_High + SMA_Threshold)
  
Meaning: SMA line passes through or near C1

Example:
  C1_Low = 45,350
  C1_High = 45,450
  C1_Range = 100
  SMA_Threshold = 100 × (2/100) = 2 pips
  SMA_196 = 45,375
  
  Check: 45,375 ≥ 45,348? ✓ YES
  Check: 45,375 ≤ 45,452? ✓ YES
  → SMA touches = TRUE ✓
```

---

## 🎭 PATTERN NOMENCLATURE

### **BULLISH SETUP (Support Pattern)**
```
Pattern Name: BULLISH_C1_C0
Definition: Inside bar at support with bullish confirmation

Components Required:
  ✓ C0: Reference candle with range
  ✓ C1: Inside candle (contained)
  ✓ C1_Low ≈ C_L20_Level (at support)
  ✓ RSI < 30 (oversold)
  ✓ C1_Close > SMA_196 (above trend)
  ✓ Confluence Score ≥ 3

Trigger: All conditions TRUE
Direction: LONG (buy/up)

Price Levels:
  Entry = C1_Close
  Target = Entry + 250 pips (Lot 1)
  Stop = Entry - (ATR × 2.0)
```

---

### **BEARISH SETUP (Resistance Pattern)**
```
Pattern Name: BEARISH_C1_C0
Definition: Inside bar at resistance with bearish confirmation

Components Required:
  ✓ C0: Reference candle with range
  ✓ C1: Inside candle (contained)
  ✓ C1_High ≈ C_H20_Level (at resistance)
  ✓ RSI > 70 (overbought)
  ✓ C1_Close < SMA_196 (below trend)
  ✓ Confluence Score ≥ 3

Trigger: All conditions TRUE
Direction: SHORT (sell/down)

Price Levels:
  Entry = C1_Close
  Target = Entry - 250 pips (Lot 1)
  Stop = Entry + (ATR × 2.0)
```

---

## 🔢 POSITION NOMENCLATURE

### **LOT NOMENCLATURE**
```
Position Split: 2-Lot System

LOT1 (Aggressive):
  Nomenclature: LOT1_C1
  Entry: C1_Close
  Exit TP: C1_Close + 250 pips (bullish)
  Exit SL: C1_Close - (ATR × 2.0)
  Hold: Until TP/SL or 159 bars
  Purpose: Quick profit capture
  
LOT2 (Conservative):
  Nomenclature: LOT2_C1
  Entry: C1_Close
  Exit TP: None (time exit)
  Exit SL: C1_Close - (ATR × 4.0)
  Hold: Until SL or 159 bars
  Purpose: Trend following
```

---

## 📈 COMPLETE CANDLE SEQUENCE

### **Multi-Candle Entry Pattern**
```
Visual Representation:

TIME → 

    C0 (Reference)          C1 (Inside)
    ┌─────────────┐        ┌──────┐
    │ High: 45500 │        │ High │
    │             │        │45450 │
    │             │─────→  │      │
    │             │        │45350 │
    │             │        └──────┘
    │ Low: 45200  │
    └─────────────┘

Nomenclature:
  Position 1: C0 - bar_index[1]
  Position 2: C1 - bar_index[0]

Reading: "C0 contains C1 = Inside bar pattern detected"
```

---

## 🎯 ENTRY SEQUENCE NOMENCLATURE

```
Full Entry Pattern Name: BULLISH_C1_C0_SMA_CONF

Breakdown:
  BULLISH_ = Direction confirmation (bullish setup)
  C1_ = Triggered by current inside candle
  C0_ = Using reference candle bounds
  SMA_ = SMA(196) confirmation
  CONF = Confluence score ≥ 3

Example Full Name:
  BULLISH_C1_C0_SMA_CONF_LOT1+LOT2

Interpretation:
  A bullish inside bar (C1 in C0) at support
  with SMA confluence and high confidence
  entering both Lot 1 (aggressive) and Lot 2 (conservative)
```

---

## 📋 QUICK REFERENCE TABLE

| Nomenclature | Full Name | Time Ref | Purpose |
|---|---|---|---|
| C0 | Reference Candle | [1] | Container for C1 |
| C1 | Inside Candle | [0] | Entry trigger |
| C_H20 | 20-Bar High | Variable | Resistance ref |
| C_L20 | 20-Bar Low | Variable | Support ref |
| COMP_Ratio | Compression Ratio | Current | Volatility check |
| SMA_196 | Simple MA(196) | Current | Trend confirm |
| RSI | Relative Strength | Current | Momentum |
| ATR | Average True Range | Current | Stop sizing |
| LOT1 | Aggressive Lot | Entry | Quick TP |
| LOT2 | Conservative Lot | Entry | Trend follow |

---

## 🔄 NOMENCLATURE IN ACTION

### **Complete Entry Analysis Example**

```
BTC/USD 1-minute Entry Analysis:

CANDLE STATE:
  C0: High=45500, Low=45200, Range=300
  C1: High=45450, Low=45350, Range=100
  
PATTERN CHECK:
  C1_High(45450) < C0_High(45500)? ✓ YES
  C1_Low(45350) > C0_Low(45200)? ✓ YES
  → Pattern: INSIDE_BAR_C1_C0 = TRUE
  
COMPRESSION CHECK:
  COMP_Ratio = 100/300 = 0.333 (< 0.5) ✓
  
SMA CHECK:
  SMA_196 = 45375 (in C1_Low-C1_High ±2)? ✓ YES
  
SUPPORT CHECK:
  C_L20 = 45100
  C1_Low(45350) near C_L20(45100)? ✓ YES
  → is_near_support = TRUE
  
MOMENTUM CHECK:
  RSI = 25 (< 30)? ✓ YES
  → is_oversold = TRUE
  
CONFLUENCE:
  ✓ C1 is inside C0
  ✓ COMP_Ratio valid
  ✓ SMA_196 touches
  ✓ Near C_L20 support
  → Confluence_Score = 4/4 ✓
  
DIRECTIONAL CHECK:
  C1_Close(45380) > SMA_196(45375)? ✓ YES
  → Pattern: BULLISH_C1_C0_SMA_CONF ✓
  
ENTRY PARAMETERS:
  Entry_Price = C1_Close = 45380
  Entry_Candle = C1
  Direction = LONG
  LOT1_TP = 45380 + 250 = 45630
  LOT1_SL = 45380 - (ATR×2) = 45360
  LOT2_TP = None (time exit)
  LOT2_SL = 45380 - (ATR×4) = 45340
  
SIGNAL: ✅ ENTER BULLISH_C1_C0_SMA_CONF
```

---

## ✅ SUMMARY

**Official Candle Nomenclature:**
- **C0** = Reference/Setup Candle (previous bar)
- **C1** = Inside Candle (current bar, entry trigger)
- **C_H20** = 20-Bar Resistance Reference
- **C_L20** = 20-Bar Support Reference
- **COMP_Ratio** = Compression metric
- **SMA_196** = Trend confirmation line

**Pattern Names:**
- **BULLISH_C1_C0_SMA_CONF** = Bullish inside bar at support
- **BEARISH_C1_C0_SMA_CONF** = Bearish inside bar at resistance

**Position Names:**
- **LOT1** = Aggressive, quick TP
- **LOT2** = Conservative, trend follow

This nomenclature provides **complete clarity** on which candle does what, making the strategy easy to understand, code, and analyze.

---

**Status**: Ready for Implementation ✅  
**Clarity**: Professional Standard ✅  
**Date**: 2026-05-06
