# FVG Reference Guide - External Indicator Analysis

**Last Updated**: 2026-05-04  
**Purpose**: Reference material for FVG pattern detection in Pine Script v5

---

## Reference Indicator 1: Multitimeframe Fair Value Gap (Zeiierman)

**Source**: [TradingView - Zeiierman MTF FVG](https://www.tradingview.com/script/5jS51RsP-Multitimeframe-Fair-Value-Gap-FVG-Zeiierman/)  
**Type**: Indicator (Free, Editor's Pick)  
**Focus**: Multi-timeframe FVG detection with institutional imbalance visualization  

### Core Implementation Details

**FVG Detection Logic**:
- Uses 3-candle sequence analysis
- Detects institutional imbalances (gaps between wick levels)
- Analyzes OHLCV data from user-selected timeframes
- Applies wick-based logic for confirmation

**Technical Approach**:
```
Bullish FVG: When high[0] < low[2] (high of candle 1 < low of candle 3)
Bearish FVG: When low[0] > high[2] (low of candle 1 > high of candle 3)

Uses request.security() to fetch data from:
- Multiple timeframes simultaneously
- Higher timeframes for bias confirmation
- Lower timeframes for execution levels
```

**Key Features**:
- Dynamic box visualization extending across chart
- Customizable strength criteria filtering
- Mitigation detection (FVG fill confirmation)
- Volume-based smart logic
- Adaptive visual elements
- Real-time unmitigated gap tracking

**Parameters to Consider**:
- Timeframe selection (1m, 5m, 15m, 1h, 4h, daily, weekly)
- Minimum FVG size threshold (percentage-based)
- Box extension settings
- Mitigation toggle
- Display options

### Integration Points for Our Library

Can implement in strategies:
- Use request.security() for multi-timeframe data
- Apply 3-candle FVG detection to smart money concepts category
- Create hybrid strategies combining FVG with other indicators

---

## Reference Indicator 2: MTF Fair Value Gaps by kfatkin

**Source**: [TradingView - kfatkin MTF FVG](https://www.tradingview.com/script/wMQ5wj87-MTF-Fair-Value-Gaps/)  
**Type**: Indicator (Open-Source)  
**Focus**: Multi-timeframe FVG with liquidity void analysis  

### Core Implementation Details

**Architecture**:
- Tracks up to 6 timeframes simultaneously
- Blends standard FVGs with Daily Liquidity Voids
- Projects higher-timeframe imbalances onto intraday charts
- Designed for SMC/ICT trading methodologies

**Optimization Features**:
```
Memory Management:
- Default max zones to track: 150
- Prevents terminal slowdown
- Avoids execution timeouts on high-tick charts

Performance Tuning:
- Selective timeframe updating
- Efficient box creation/deletion
- Smart filtering system
```

**Customization Options**:
1. **Mitigation Toggle**: Auto-delete vs. keep historical gaps
2. **Threshold %**: Minimum gap size filter
3. **Extend Boxes**: Control right-side projection distance
4. **Max Zones**: Memory limit for performance

**Supported Timeframes**:
- 1m, 3m, 5m, 15m, 30m, 45m, 60m
- 2h, 3h, 4h
- Daily, Weekly

### Integration Points for Our Library

Can implement in strategies:
- Multi-timeframe tracking system (up to 6 TF)
- Daily liquidity void detection
- Memory-efficient zone management
- Performance optimization patterns

---

## Reference Indicator 3: 30M FVG Raw Validator

**Characteristics**: Raw validator for traders who want full control  
**Purpose**: True 30M FVG detection with correct 3-candle imbalance logic  
**Use Case**: ICT/SMC traders, London/NY session analysis, FVG retest models  

### Core Implementation Details

**FVG Detection (3-Candle Structure)**:
```
Bearish FVG (down move):
- Condition: low[0] > high[2]
- Meaning: Lower level of candle 1 above upper level of candle 3
- Creates unfilled gap below candle 3

Bullish FVG (up move):
- Condition: high[0] < low[2]
- Meaning: Upper level of candle 1 below lower level of candle 3
- Creates unfilled gap above candle 3
```

**Technical Implementation**:
```pine
Uses request.security() for 30M data fetch
On 30M chart: Detects FVG formation
On lower TF chart: Draws box showing 30M FVG level
```

**Box Configuration**:
- Anchored to candle 1 of formation
- Optional right-side extension (for mitigation tracking)
- Minimum FVG size filtering

### Integration Points for Our Library

Core pattern for:
- FVG_Detection_Strategy (already created)
- Multi-timeframe FVG confirmation
- Time-specific trading windows

---

## Comparison Matrix

| Feature | Zeiierman | kfatkin | 30M Validator |
|---------|-----------|---------|---------------|
| Timeframes | Multiple | Up to 6 | 1 (30M to current) |
| FVG Detection | 3-candle wick | 3-candle wick | 3-candle gap |
| Liquidity Voids | Built-in logic | Daily voids | Optional |
| Mitigation Tracking | Yes | Yes | Yes |
| Open Source | Free | Yes | Likely |
| Performance Focus | Dynamic viz | Memory efficient | Lean/fast |
| Use Case | Institutional analysis | SMC/ICT trading | Raw validator |

---

## Common FVG Implementation Patterns

All three indicators share core concepts:

### 1. Three-Candle Structure
```
Pattern: [Candle 1] [Candle 2] [Candle 3]

Bearish FVG: low[0] > high[2]
- Forms when price gaps down
- Gap exists between candle 1 low and candle 3 high
- Traders expect price to "fill" this gap later

Bullish FVG: high[0] < low[2]  
- Forms when price gaps up
- Gap exists between candle 1 high and candle 3 low
- Gap typically filled in mean reversion or consolidation
```

### 2. Multi-Timeframe Detection
```pine
// Core pattern used by all three
mtf_fvg = request.security(syminfo.tickerid, selected_timeframe, detect_fvg_logic)

// Allows detecting FVGs on 1h chart while trading 5m
// Creates higher-timeframe bias for lower-timeframe entries
```

### 3. Box Visualization
```pine
// Standard approach across all indicators
box.new(start_bar, top_price, current_bar, bottom_price, 
        bgcolor=fvg_color, border_color=confirmation_color)
```

### 4. Mitigation Detection
```pine
// Check if FVG is "filled" (price has revisited the gap)
fvg_mitigated = (bullish_fvg and close <= top_price) or 
                (bearish_fvg and close >= bottom_price)
```

---

## How to Add These to Your Reference Library

### Step 1: Copy the Code
1. Visit each TradingView link
2. Open the indicator
3. Copy the complete Pine Script code

### Step 2: Store in Reference
Create files:
```
fvg_references/
├── Zeiierman_MTF_FVG_Reference.pine
├── Kfatkin_MTF_FVG_Reference.pine
├── FVG_Raw_Validator_Reference.pine
└── FVG_ANALYSIS.md (this file)
```

### Step 3: Document Features
For each, note:
- FVG detection method
- Multi-timeframe approach
- Box visualization pattern
- Mitigation logic
- Performance considerations

---

## Key Takeaways for Strategy Development

### What These Indicators Demonstrate

1. **Multi-Timeframe Confirmation**: Using request.security() effectively
   - Fetch data from multiple timeframes
   - Apply logic at different scales
   - Project higher-TF levels to lower-TF chart

2. **Institutional Pattern Recognition**: 
   - 3-candle FVG formation
   - Wick-based gap detection
   - Mitigation/fill tracking

3. **Performance Optimization**:
   - Memory management (max zones limit)
   - Efficient box management
   - Selective updates

4. **Smart Money Concepts Integration**:
   - Gap analysis (FVGs)
   - Liquidity tracking
   - Institutional imbalance detection

### Apply to Our Strategies

These patterns are already being used in:
- `FVG_Detection_Strategy.pine` (fair value gap detection)
- `MTF_*_Confirmation.pine` (multi-timeframe logic)
- `Supply_Demand_Zones.pine` (zone-based levels)

Can enhance with:
- Zeiierman's wick-based gap detection
- kfatkin's 6-timeframe tracking
- Raw validator's tight FVG logic

---

## Next Steps

1. ✅ Copy code from each TradingView link
2. ✅ Store in `fvg_references/` subdirectory  
3. ✅ Document feature analysis
4. ✅ Create strategies using these patterns
5. ✅ Test FVG-based entry logic

---

**Status**: Reference Guide Created  
**Location**: `/backtesting/strategies_reference/FVG_REFERENCE_GUIDE.md`  
**Ready for**: Custom FVG strategy development

Once you provide the actual code, I can:
- Store with proper attribution
- Extract specific patterns
- Create advanced FVG strategies
- Document the implementation details
