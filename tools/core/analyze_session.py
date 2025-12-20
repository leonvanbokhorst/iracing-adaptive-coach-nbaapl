#!/usr/bin/env python3
"""
Core Tool: Session Analysis (FACTS ONLY)

This tool outputs PURE FACTS as JSON. No interpretation, no coaching.
Little Padawan reads this output and gives it meaning.

Usage:
    python tools/core/analyze_session.py data/session.csv
    
Output: JSON with all session metrics
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.core.data_loader import load_session_data, analyze_session_basic, analyze_sectors


def analyze_session_facts(csv_path):
    """
    Analyze session and return FACTS ONLY (no interpretation)
    
    Returns:
        dict: Pure factual data about the session
    """
    df = load_session_data(csv_path)
    
    if len(df) == 0:
        return {"error": "No valid laps found"}
    
    # Basic facts
    basic = analyze_session_basic(df)
    
    # Sector facts (if available)
    sectors = analyze_sectors(df)
    
    # Data cleaning facts
    total_laps = int(len(df))
    clean_laps = int(df['clean'].sum())
    outliers = int(df['is_outlier'].sum()) if 'is_outlier' in df.columns else 0
    
    if 'Clean' in df.columns:
        incidents = int((df['Clean'] == 0).sum())
    elif 'Inc' in df.columns:
        incidents = int((df['Inc'] > 0).sum())
    else:
        incidents = 0
    
    # Lap time distribution facts
    clean_df = df[df['clean']]
    lap_times = clean_df['LapTime'].tolist()
    
    # Theoretical optimal (best sectors combined)
    theoretical_optimal = None
    if sectors:
        theoretical_optimal = sum(s['best'] for s in sectors.values())
    
    # Build facts dictionary
    facts = {
        "session": {
            "total_laps": total_laps,
            "clean_laps": clean_laps,
            "dirty_laps": total_laps - clean_laps,
            "outliers_filtered": outliers,
            "incidents": incidents
        },
        "lap_times": {
            "best": basic['best_lap'],
            "average": basic['avg_lap'],
            "median": basic['median_lap'],
            "worst": float(clean_df['LapTime'].max()),
            "sigma": basic['sigma'],
            "all_laps": lap_times
        },
        "sectors": {}
    }
    
    # Add sector facts
    if sectors:
        for sector_name, sector_data in sectors.items():
            facts["sectors"][sector_name] = {
                "best": sector_data['best'],
                "average": sector_data['avg'],
                "worst": sector_data['worst'],
                "sigma": sector_data['sigma'],
                "loss_per_lap": sector_data['loss_per_lap'],
                "total_loss": sector_data['total_loss']
            }
        
        facts["theoretical_optimal"] = theoretical_optimal
        facts["gap_to_optimal"] = basic['best_lap'] - theoretical_optimal
    
    return facts


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python analyze_session.py <session.csv>"}))
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    if not Path(csv_path).exists():
        print(json.dumps({"error": f"File not found: {csv_path}"}))
        sys.exit(1)
    
    facts = analyze_session_facts(csv_path)
    
    # Output pure JSON facts
    print(json.dumps(facts, indent=2))


if __name__ == "__main__":
    main()
