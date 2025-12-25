#!/usr/bin/env python3
"""
Track Map Generator with Sector Coloring
Creates beautiful track maps from Garage61 telemetry exports.

Usage:
    # Default (3 sectors)
    uv run python tools/core/generate_track_map.py path/to/telemetry.csv
    
    # 4 sectors (like iRacing uses)
    uv run python tools/core/generate_track_map.py path/to/telemetry.csv --sectors 0.25 0.5 0.75
    
    # Custom output path
    uv run python tools/core/generate_track_map.py path/to/telemetry.csv --output track-map.png
    
    # 5 sectors
    uv run python tools/core/generate_track_map.py path/to/telemetry.csv --sectors 0.2 0.4 0.6 0.8
    
    # With corner numbers
    uv run python tools/core/generate_track_map.py path/to/telemetry.csv --corners 0.08 0.15 0.21 0.27 0.35 0.45

The tool reads GPS coordinates from telemetry and creates a track map
with sectors color-coded and labeled. Supports any number of sectors!
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# Base colors for styling
COLORS = {
    'start_finish': '#e74c3c',# Red accent
    'sector_line': '#8c8c8c', # Mid-gray
    'background': '#FFFFFF',  # White figure background
    'track_bg': '#F5F7FA',    # Light panel background
    'track_outline': '#d0d7e2' # Soft outline for context
}

# Sector colors - vibrant and distinct (expandable for any number of sectors)
SECTOR_COLORS = [
    '#1f78b4',  # Blue
    '#e38f14',  # Orange
    '#2ca25f',  # Green
    '#9467bd',  # Purple
    '#d62728',  # Red
    '#8c564b',  # Brown
    '#e377c2',  # Pink
    '#7f7f7f',  # Gray
    '#bcbd22',  # Olive
    '#17becf',  # Cyan
]


def load_telemetry(csv_path: Path) -> pd.DataFrame:
    """Load telemetry CSV and validate required columns."""
    df = pd.read_csv(csv_path)
    
    required = ['Lat', 'Lon', 'LapDistPct']
    missing = [col for col in required if col not in df.columns]
    
    if missing:
        print(f"❌ Missing required columns: {missing}")
        print(f"   Available columns: {list(df.columns)}")
        sys.exit(1)
    
    return df


def extract_track_data(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Extract and clean GPS coordinates and lap distance percentage."""
    # Filter out any invalid data
    valid = (
        (df['Lat'].notna()) & 
        (df['Lon'].notna()) & 
        (df['LapDistPct'].notna()) &
        (df['LapDistPct'] >= 0) &
        (df['LapDistPct'] <= 1)
    )
    
    df_clean = df[valid].copy()
    
    # Sort by lap distance to ensure continuous line
    df_clean = df_clean.sort_values('LapDistPct')
    
    lat = df_clean['Lat'].values
    lon = df_clean['Lon'].values
    dist_pct = df_clean['LapDistPct'].values
    
    return lat, lon, dist_pct


def find_sector_boundaries(dist_pct: np.ndarray, sector_splits: list[float]) -> list[int]:
    """Find indices where sectors change."""
    boundaries = []
    for split in sector_splits:
        # Find the index closest to this split point
        idx = np.argmin(np.abs(dist_pct - split))
        boundaries.append(idx)
    return boundaries


def create_track_map(
    lat: np.ndarray,
    lon: np.ndarray, 
    dist_pct: np.ndarray,
    sector_splits: list[float],
    title: str = "Track Map",
    output_path: Path | None = None,
    corner_positions: list[float] | None = None,
):
    """Create the track map visualization with sector coloring.
    
    Args:
        lat: Latitude coordinates
        lon: Longitude coordinates
        dist_pct: Lap distance percentage (0-1)
        sector_splits: List of split points (e.g., [0.25, 0.5, 0.75] for 4 sectors)
        title: Map title
        output_path: Where to save the output
        corner_positions: Optional list of corner positions as fractions (e.g., [0.08, 0.15, 0.21, ...] for T1, T2, T3, ...)
    """
    
    # Convert to relative coordinates (meters-ish, for better aspect ratio)
    # Using simple equirectangular projection
    lat_center = np.mean(lat)
    lon_center = np.mean(lon)
    
    # Convert to approximate meters
    lat_scale = 111320  # meters per degree latitude
    lon_scale = 111320 * np.cos(np.radians(lat_center))  # meters per degree longitude
    
    x = (lon - lon_center) * lon_scale
    y = (lat - lat_center) * lat_scale
    
    # Number of sectors = number of splits + 1
    num_sectors = len(sector_splits) + 1
    
    # Set up the figure with light theme to match other graphs
    fig, ax = plt.subplots(figsize=(12, 10), facecolor=COLORS['background'])
    ax.set_facecolor(COLORS['track_bg'])
    
    # Plot track outline (soft reference line)
    ax.plot(x, y, color=COLORS['track_outline'], linewidth=8, alpha=0.6, solid_capstyle='round')
    
    # Plot each sector with thick colored lines
    linewidth = 6
    
    # Create masks and plot for each sector dynamically
    sector_boundaries = [0.0] + sector_splits + [1.0]
    
    for i in range(num_sectors):
        start = sector_boundaries[i]
        end = sector_boundaries[i + 1]
        
        # Create mask for this sector
        mask = (dist_pct >= start) & (dist_pct < end)
        
        # Get color (cycle through available colors if we have more sectors than colors)
        color = SECTOR_COLORS[i % len(SECTOR_COLORS)]
        
        # Plot this sector
        if np.any(mask):
            ax.plot(x[mask], y[mask], color=color, 
                    linewidth=linewidth, solid_capstyle='round', 
                    label=f'S{i+1}')
    
    # Mark sector boundaries with small dots
    if sector_splits:
        boundaries = find_sector_boundaries(dist_pct, sector_splits)
        
        for idx in boundaries:
            ax.scatter([x[idx]], [y[idx]], color='white', 
                       s=40, zorder=10, marker='o', edgecolors=COLORS['sector_line'], linewidths=1.5)
    
    # Mark corners if provided
    if corner_positions:
        for i, corner_pct in enumerate(corner_positions, start=1):
            # Find closest point on track to this corner position
            idx = np.argmin(np.abs(dist_pct - corner_pct))
            
            # Plot corner marker (dark circle with white edge)
            ax.scatter([x[idx]], [y[idx]], color='#2C3E50', 
                      s=200, zorder=12, marker='o', edgecolors='white', linewidths=2.5)
            
            # Add corner label (white text centered on marker)
            ax.annotate(f'{i}', (x[idx], y[idx]), 
                       textcoords="offset points", 
                       xytext=(0, 0),  # Centered on marker
                       fontsize=9, 
                       color='white', 
                       fontweight='bold',
                       ha='center', 
                       va='center',
                       zorder=13)
    
    # Mark start/finish line (checkered line perpendicular to track)
    # Calculate track direction at S/F (use first few points)
    dx_track = x[5] - x[0]
    dy_track = y[5] - y[0]
    track_length = np.sqrt(dx_track**2 + dy_track**2)
    
    # Perpendicular direction (rotate 90 degrees)
    dx_perp = -dy_track / track_length
    dy_perp = dx_track / track_length
    
    # Line length (scaled to track width, approximately)
    line_length = 40  # meters (scaled down to half)
    
    # Draw checkered finish line (5 segments: black-white-black-white-black)
    num_segments = 5
    segment_length = line_length / num_segments
    
    for i in range(num_segments):
        offset_start = -line_length/2 + i * segment_length
        offset_end = -line_length/2 + (i + 1) * segment_length
        
        x_start = x[0] + dx_perp * offset_start
        y_start = y[0] + dy_perp * offset_start
        x_end = x[0] + dx_perp * offset_end
        y_end = y[0] + dy_perp * offset_end
        
        color = 'black' if i % 2 == 0 else 'white'
        ax.plot([x_start, x_end], [y_start, y_end], 
                color=color, linewidth=4, solid_capstyle='butt', zorder=15)
    
    # Add thin border to make white segments visible
    x_line_start = x[0] + dx_perp * (-line_length/2)
    y_line_start = y[0] + dy_perp * (-line_length/2)
    x_line_end = x[0] + dx_perp * (line_length/2)
    y_line_end = y[0] + dy_perp * (line_length/2)
    ax.plot([x_line_start, x_line_end], [y_line_start, y_line_end], 
            color='#2C3E50', linewidth=5, solid_capstyle='butt', zorder=14, alpha=0.8)
    
    # Add direction arrow (at 25% of lap)
    arrow_idx = np.argmin(np.abs(dist_pct - 0.25))
    arrow_idx_next = min(arrow_idx + 5, len(x) - 1)
    
    dx = x[arrow_idx_next] - x[arrow_idx]
    dy = y[arrow_idx_next] - y[arrow_idx]
    
    ax.annotate('', xy=(x[arrow_idx] + dx*2, y[arrow_idx] + dy*2), 
                xytext=(x[arrow_idx], y[arrow_idx]),
                arrowprops=dict(arrowstyle='->', color='white', lw=2))
    
    # Title and styling
    ax.set_title(title, fontsize=18, fontweight='bold', color='#2C3E50', pad=20)
    
    # Equal aspect ratio for proper track shape
    ax.set_aspect('equal')
    
    # Remove axes for cleaner look
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Create legend - positioned at bottom, outside track (S/F already labeled on map)
    legend_elements = [
        mpatches.Patch(facecolor=SECTOR_COLORS[i % len(SECTOR_COLORS)], label=f'S{i+1}')
        for i in range(num_sectors)
    ]
    
    # Adjust ncol based on number of sectors (max 5 per row)
    ncol = min(num_sectors, 5)
    
    ax.legend(handles=legend_elements, loc='lower center', fontsize=11,
              facecolor='white', edgecolor='#d0d7e2',
              labelcolor='#2C3E50', framealpha=0.95, ncol=ncol,
              bbox_to_anchor=(0.5, -0.06))
    
    plt.tight_layout()
    
    # Save or show
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                   facecolor=COLORS['background'], edgecolor='none')
        print(f"✅ Saved track map to: {output_path}")
    else:
        plt.show()
    
    return fig


def main():
    parser = argparse.ArgumentParser(
        description="Generate track map with sector coloring from telemetry"
    )
    parser.add_argument("csv_file", type=Path, help="Path to Garage61 telemetry CSV")
    parser.add_argument("--output", "-o", type=Path, help="Output PNG path")
    parser.add_argument("--title", "-t", type=str, default=None, 
                       help="Map title (auto-detected from filename if not provided)")
    parser.add_argument("--sectors", nargs='+', type=float, default=[0.55, 0.77],
                       metavar='SPLIT',
                       help="Sector split points as fractions (e.g., '0.25 0.5 0.75' for 4 sectors, default: 0.55 0.77 for 3 sectors)")
    parser.add_argument("--corners", nargs='*', type=float, default=None,
                       metavar='POSITION',
                       help="Corner positions as fractions (e.g., '0.08 0.15 0.21' for T1, T2, T3, ...)")
    
    args = parser.parse_args()
    
    if not args.csv_file.exists():
        print(f"❌ File not found: {args.csv_file}")
        sys.exit(1)
    
    # Auto-detect title from filename if not provided
    if args.title is None:
        # Try to extract track name from Garage61 filename format
        filename = args.csv_file.stem
        if " - " in filename:
            parts = filename.split(" - ")
            # Format: "Garage 61 - Driver - Car - Track - Time - ID"
            if len(parts) >= 4:
                args.title = parts[3]  # Track name
            else:
                args.title = filename
        else:
            args.title = filename
    
    # Auto-detect output path if not provided
    if args.output is None:
        args.output = args.csv_file.parent / f"{args.csv_file.stem}-track-map.png"
    
    print(f"📍 Loading telemetry from: {args.csv_file}")
    df = load_telemetry(args.csv_file)
    
    print(f"📊 Found {len(df)} data points")
    
    lat, lon, dist_pct = extract_track_data(df)
    print(f"🗺️  Extracted {len(lat)} valid GPS coordinates")
    
    num_sectors = len(args.sectors) + 1
    print(f"🎨 Generating track map: {args.title}")
    print(f"   {num_sectors} sectors with splits at: {', '.join([f'{s*100:.1f}%' for s in args.sectors])}")
    
    if args.corners:
        print(f"   {len(args.corners)} corners marked")
    
    create_track_map(
        lat=lat,
        lon=lon,
        dist_pct=dist_pct,
        sector_splits=args.sectors,
        title=args.title,
        output_path=args.output,
        corner_positions=args.corners,
    )
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

