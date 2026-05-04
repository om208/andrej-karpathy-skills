#!/usr/bin/env python3
"""
HIGH QUALITY FVG PATTERN ANALYZER
Identifies and analyzes the top 10 high-quality FVG pattern formations
"""

import pandas as pd
import numpy as np
from pathlib import Path

print("\n" + "="*120)
print("HIGH QUALITY FVG PATTERN FORMATION ANALYSIS")
print("Filtering & Analyzing Top 10 Pattern Types Across 1-Minute and 5-Minute Timeframes")
print("="*120)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n[STEP 1] Loading detailed FVG data...")
print("-" * 120)

df_1m = pd.read_csv("analysis/fvg_deep_analysis/1MIN_FVG_DETAILED_DATA.csv")
df_5m = pd.read_csv("analysis/fvg_deep_analysis/5MIN_FVG_DETAILED_DATA.csv")

print(f"✓ Loaded 1-minute: {len(df_1m)} patterns")
print(f"✓ Loaded 5-minute: {len(df_5m)} patterns")

# ============================================================================
# DEFINE HIGH-QUALITY FVG CRITERIA
# ============================================================================

print("\n[STEP 2] Filtering for HIGH-QUALITY FVGs...")
print("-" * 120)

def identify_pattern_type(row):
    """Classify FVG pattern based on characteristics"""

    # Calculate tail ratios
    if row['body2'] > 0:
        upper_tail_ratio = row['upper_tail2'] / row['body2']
        lower_tail_ratio = row['lower_tail2'] / row['body2']
    else:
        return "UNDEFINED"

    # Body ratio characteristics
    outer_avg = (row['body1_ratio'] + row['body3_ratio']) / 2

    # Tail dominance
    upper_dominant = upper_tail_ratio > lower_tail_ratio
    lower_dominant = lower_tail_ratio > upper_tail_ratio

    # Body size categorization
    tiny_body = outer_avg < 0.15  # Very small outer candles
    small_body = outer_avg < 0.25  # Small outer candles
    medium_body = outer_avg < 0.40  # Medium outer candles

    # Move size categorization
    move_size = max(row['max_upside'], row['max_downside'])

    # ========== PATTERN CLASSIFICATION ==========

    # PATTERN 1: IDEAL DOJI UPPER - Small body + upper tail dominant + large move
    if tiny_body and upper_dominant and upper_tail_ratio > 1.5 and move_size > 0:
        return "IDEAL_DOJI_UPPER"

    # PATTERN 2: IDEAL DOJI LOWER - Small body + lower tail dominant + large move
    if tiny_body and lower_dominant and lower_tail_ratio > 1.5 and move_size > 0:
        return "IDEAL_DOJI_LOWER"

    # PATTERN 3: STRONG UPPER BIAS - Small body + strong upper tail + upside move
    if small_body and upper_dominant and upper_tail_ratio > 1.2 and row['larger_move'] == 'UP':
        return "STRONG_UPPER_BIAS"

    # PATTERN 4: STRONG LOWER BIAS - Small body + strong lower tail + downside move
    if small_body and lower_dominant and lower_tail_ratio > 1.2 and row['larger_move'] == 'DOWN':
        return "STRONG_LOWER_BIAS"

    # PATTERN 5: BALANCED UPPER - Medium body + balanced tails + upper move
    if medium_body and upper_dominant and row['larger_move'] == 'UP':
        return "BALANCED_UPPER"

    # PATTERN 6: BALANCED LOWER - Medium body + balanced tails + lower move
    if medium_body and lower_dominant and row['larger_move'] == 'DOWN':
        return "BALANCED_LOWER"

    # PATTERN 7: EXPLOSIVE UPPER - Small body + very high upper tail ratio
    if small_body and upper_tail_ratio > 2.0 and row['max_upside'] > row['max_downside']:
        return "EXPLOSIVE_UPPER"

    # PATTERN 8: EXPLOSIVE LOWER - Small body + very high lower tail ratio
    if small_body and lower_tail_ratio > 2.0 and row['max_downside'] > row['max_upside']:
        return "EXPLOSIVE_LOWER"

    # PATTERN 9: HIDDEN REVERSAL UPPER - Lower tail dominant but upside move
    if lower_dominant and row['larger_move'] == 'UP' and small_body:
        return "HIDDEN_REVERSAL_UPPER"

    # PATTERN 10: HIDDEN REVERSAL LOWER - Upper tail dominant but downside move
    if upper_dominant and row['larger_move'] == 'DOWN' and small_body:
        return "HIDDEN_REVERSAL_LOWER"

    # PATTERN 11: STANDARD UPPER - Standard characteristics + upside move
    if row['larger_move'] == 'UP' and move_size > 0:
        return "STANDARD_UPPER"

    # PATTERN 12: STANDARD LOWER - Standard characteristics + downside move
    if row['larger_move'] == 'DOWN' and move_size > 0:
        return "STANDARD_LOWER"

    return "OTHER"

# Apply pattern classification
print("\nClassifying patterns...")
df_1m['pattern_type'] = df_1m.apply(identify_pattern_type, axis=1)
df_5m['pattern_type'] = df_5m.apply(identify_pattern_type, axis=1)

print(f"✓ 1-minute patterns classified")
print(f"✓ 5-minute patterns classified")

# Filter high-quality patterns (exclude STANDARD and OTHER)
high_quality_types = ['IDEAL_DOJI_UPPER', 'IDEAL_DOJI_LOWER',
                      'STRONG_UPPER_BIAS', 'STRONG_LOWER_BIAS',
                      'EXPLOSIVE_UPPER', 'EXPLOSIVE_LOWER',
                      'HIDDEN_REVERSAL_UPPER', 'HIDDEN_REVERSAL_LOWER',
                      'BALANCED_UPPER', 'BALANCED_LOWER']

df_1m_hq = df_1m[df_1m['pattern_type'].isin(high_quality_types)].copy()
df_5m_hq = df_5m[df_5m['pattern_type'].isin(high_quality_types)].copy()

print(f"\n✓ 1-minute HIGH-QUALITY FVGs: {len(df_1m_hq)} ({len(df_1m_hq)/len(df_1m)*100:.1f}%)")
print(f"✓ 5-minute HIGH-QUALITY FVGs: {len(df_5m_hq)} ({len(df_5m_hq)/len(df_5m)*100:.1f}%)")

# ============================================================================
# ANALYZE TOP 10 PATTERNS
# ============================================================================

print("\n[STEP 3] Analyzing top 10 high-quality pattern formations...")
print("-" * 120)

def analyze_pattern_group(df, pattern_name):
    """Analyze a specific pattern type"""
    patterns = df[df['pattern_type'] == pattern_name]

    if len(patterns) == 0:
        return None

    return {
        'pattern_type': pattern_name,
        'frequency': len(patterns),
        'percentage': len(patterns) / len(df) * 100,
        'max_upside': patterns['max_upside'].max(),
        'max_downside': patterns['max_downside'].max(),
        'avg_upside': patterns[patterns['larger_move'] == 'UP']['max_upside'].mean() if len(patterns[patterns['larger_move'] == 'UP']) > 0 else 0,
        'avg_downside': patterns[patterns['larger_move'] == 'DOWN']['max_downside'].mean() if len(patterns[patterns['larger_move'] == 'DOWN']) > 0 else 0,
        'upside_count': len(patterns[patterns['larger_move'] == 'UP']),
        'downside_count': len(patterns[patterns['larger_move'] == 'DOWN']),
    }

# Analyze all high-quality patterns
all_patterns = {}

for pattern_type in high_quality_types:
    # 1-minute
    pattern_1m = analyze_pattern_group(df_1m_hq, pattern_type)
    if pattern_1m:
        all_patterns[f"{pattern_type}_1M"] = {**pattern_1m, 'timeframe': '1M'}

    # 5-minute
    pattern_5m = analyze_pattern_group(df_5m_hq, pattern_type)
    if pattern_5m:
        all_patterns[f"{pattern_type}_5M"] = {**pattern_5m, 'timeframe': '5M'}

# Sort by frequency to get top 10
sorted_patterns = sorted(all_patterns.items(), key=lambda x: x[1]['frequency'], reverse=True)[:10]

print(f"\nTop 10 High-Quality FVG Pattern Formations:\n")

# ============================================================================
# GENERATE DETAILED REPORT
# ============================================================================

report = []

report.append("\n" + "="*120)
report.append("1-MINUTE TIMEFRAME REPORT")
report.append("="*120)

report.append("\n" + "="*120)
report.append("5-MINUTE TIMEFRAME REPORT")
report.append("="*120)

report.append("\n" + "="*120)
report.append("TOP 10 HIGH-QUALITY FVG PATTERN FORMATIONS")
report.append("="*120)

for idx, (pattern_key, pattern_data) in enumerate(sorted_patterns, 1):
    timeframe = pattern_data['timeframe']
    pattern_type = pattern_data['pattern_type']
    frequency = pattern_data['frequency']
    percentage = pattern_data['percentage']
    max_upside = pattern_data['max_upside']
    max_downside = pattern_data['max_downside']
    avg_upside = pattern_data['avg_upside']
    avg_downside = pattern_data['avg_downside']
    upside_count = pattern_data['upside_count']
    downside_count = pattern_data['downside_count']

    print(f"\n{'='*120}")
    print(f"PATTERN #{idx}: {pattern_type} ({timeframe})")
    print(f"{'='*120}")
    print(f"Frequency:                   {frequency:,} times ({percentage:.2f}%)")
    print(f"Direction Split:             {upside_count} UPSIDE | {downside_count} DOWNSIDE")
    print(f"\nMaximum Move Range:")
    print(f"  Maximum Upside Move:       {max_upside:,.2f} points")
    print(f"  Maximum Downside Move:     {max_downside:,.2f} points")
    print(f"\nAverage Move:")
    if upside_count > 0:
        print(f"  Average Upside Move:       {avg_upside:,.2f} points ({upside_count} patterns)")
    else:
        print(f"  Average Upside Move:       N/A (0 patterns)")
    if downside_count > 0:
        print(f"  Average Downside Move:     {avg_downside:,.2f} points ({downside_count} patterns)")
    else:
        print(f"  Average Downside Move:     N/A (0 patterns)")

    report.append(f"\n{'='*120}")
    report.append(f"PATTERN #{idx}: {pattern_type} ({timeframe})")
    report.append(f"{'='*120}")
    report.append(f"Frequency:                   {frequency:,} times ({percentage:.2f}%)")
    report.append(f"Direction Split:             {upside_count} UPSIDE | {downside_count} DOWNSIDE")
    report.append(f"\nMaximum Move Range:")
    report.append(f"  Maximum Upside Move:       {max_upside:,.2f} points")
    report.append(f"  Maximum Downside Move:     {max_downside:,.2f} points")
    report.append(f"\nAverage Move:")
    if upside_count > 0:
        report.append(f"  Average Upside Move:       {avg_upside:,.2f} points ({upside_count} patterns)")
    else:
        report.append(f"  Average Upside Move:       N/A (0 patterns)")
    if downside_count > 0:
        report.append(f"  Average Downside Move:     {avg_downside:,.2f} points ({downside_count} patterns)")
    else:
        report.append(f"  Average Downside Move:     N/A (0 patterns)")

# Save detailed report
print("\n" + "="*120)
print("SAVING HIGH-QUALITY PATTERN ANALYSIS REPORT")
print("="*120)

report_file = "analysis/fvg_deep_analysis/HIGH_QUALITY_PATTERNS_ANALYSIS.txt"
with open(report_file, 'w') as f:
    f.write("\n" + "="*120 + "\n")
    f.write("HIGH QUALITY FVG PATTERN FORMATION ANALYSIS\n")
    f.write("Top 10 Patterns - 1-Minute and 5-Minute Timeframes\n")
    f.write("="*120 + "\n")
    f.write("\n".join(report))

print(f"\n✓ Report saved to: {report_file}")

# Save pattern statistics to CSV
print("\nSaving detailed pattern statistics...")

stats_data = []
for pattern_key, pattern_data in sorted_patterns:
    stats_data.append({
        'rank': len(stats_data) + 1,
        'pattern_type': pattern_data['pattern_type'],
        'timeframe': pattern_data['timeframe'],
        'frequency': pattern_data['frequency'],
        'percentage': pattern_data['percentage'],
        'max_upside': pattern_data['max_upside'],
        'max_downside': pattern_data['max_downside'],
        'avg_upside': pattern_data['avg_upside'],
        'avg_downside': pattern_data['avg_downside'],
        'upside_count': pattern_data['upside_count'],
        'downside_count': pattern_data['downside_count'],
    })

stats_df = pd.DataFrame(stats_data)
stats_file = "analysis/fvg_deep_analysis/TOP10_PATTERNS_STATISTICS.csv"
stats_df.to_csv(stats_file, index=False)

print(f"✓ Statistics saved to: {stats_file}")

print("\n" + "="*120)
print("HIGH-QUALITY PATTERN ANALYSIS COMPLETE")
print("="*120)
