"""Data summary and cleaning report utilities"""
import pandas as pd


def get_cleaning_summary(df):
    """Get summary of data cleaning results"""
    total_laps = len(df)
    clean_laps = df['clean'].sum()
    dirty_laps = total_laps - clean_laps
    
    outliers = df['is_outlier'].sum() if 'is_outlier' in df.columns else 0
    # Garage 61 uses 'Clean' column (1=clean, 0=incident)
    if 'Clean' in df.columns:
        incidents = (df['Clean'] == 0).sum()
    elif 'Inc' in df.columns:
        incidents = (df['Inc'] > 0).sum()
    else:
        incidents = 0
    
    summary = {
        'total_laps': total_laps,
        'clean_laps': clean_laps,
        'dirty_laps': dirty_laps,
        'outliers': outliers,
        'incidents': incidents
    }
    
    return summary


def print_cleaning_summary(df):
    """Print human-readable cleaning summary"""
    summary = get_cleaning_summary(df)
    
    print(f"\n📊 Session Data Summary:")
    print(f"   Total laps: {summary['total_laps']}")
    print(f"   Clean laps: {summary['clean_laps']} (used for analysis)")
    print(f"   Dirty laps: {summary['dirty_laps']}", end="")
    
    if summary['dirty_laps'] > 0:
        reasons = []
        if summary['outliers'] > 0:
            reasons.append(f"{summary['outliers']} outlier{'s' if summary['outliers'] > 1 else ''}")
        if summary['incidents'] > 0:
            reasons.append(f"{summary['incidents']} incident{'s' if summary['incidents'] > 1 else ''}")
        
        if reasons:
            print(f" ({', '.join(reasons)})")
        else:
            print()
    else:
        print()
    
    if summary['dirty_laps'] > 0:
        print(f"   ✓ Outliers and partial laps filtered out automatically")
    
    print()


def get_outlier_details(df):
    """Get details about which laps were marked as outliers"""
    if 'is_outlier' not in df.columns:
        return []
    
    outlier_laps = df[df['is_outlier']].copy()
    
    details = []
    for idx, row in outlier_laps.iterrows():
        lap_num = idx + 1
        lap_time = row['LapTime']
        reason = "pit stop or standing still" if lap_time > df['LapTime'].median() else "partial lap"
        
        details.append({
            'lap_number': lap_num,
            'lap_time': lap_time,
            'reason': reason
        })
    
    return details


def print_outlier_details(df):
    """Print details about filtered outliers"""
    details = get_outlier_details(df)
    
    if not details:
        return
    
    print(f"\n🔍 Filtered Outliers:")
    for detail in details:
        print(f"   Lap {detail['lap_number']}: {detail['lap_time']:.2f}s ({detail['reason']})")
    print()
