# Season Standings Data

This folder contains weekly season standings CSVs downloaded from iRacing.

## Directory Structure

```
data/standings/
└── season-driver_Formula_1600_Rookie_Series_*.csv
```

## Weekly Workflow

After each race week ends:

### 1. Download Standings from iRacing
- Go to iRacing website
- Navigate to Series Standings
- Download CSV for Formula 1600 Rookie Series

### 2. Generate Weekly Report
```bash
uv run python tools/coach/generate_weekly_standings_report.py <week_number> data/standings/season-driver_*.csv 1238
```

### 3. Report Output
Report is automatically saved to:
- `weeks/week<XX>/standings-report.md`

## Master Lonn's Tracking Info

- **Customer ID:** 981717
- **Starting iRating (S01 2026):** 1238
- **Series:** Formula 1600 Rookie Series
- **Country:** NL (Netherlands)

## What the Report Includes

- Overall position and percentile rankings
- iRating progression (from starting 1238)
- Division analysis and comparison
- Dutch drivers ranking
- Incident rate analysis
- Statistical correlations
- Goals and targets for progression
- Week-over-week changes (when multiple weeks available)

## Tips

- Download standings **after the week officially ends** (Sunday night/Monday morning)
- Keep the iRacing default filename format for consistency
- The tool automatically detects your stats using custid 981717
- Starting iRating (1238) is used to track progress week-over-week

### Progression Visualizations

Create charts showing your season trajectory (requires 1+ weeks):

```bash
# Single week
uv run python tools/coach/visualize_standings_progression.py data/standings/
```

Generates:
- `weeks/progression/irating_progression.png` - iRating trajectory with trends
- `weeks/progression/position_climb.png` - Position changes over time
- `weeks/progression/percentile_progression.png` - Percentile rankings across metrics
- `weeks/progression/progression-report.md` - Summary report with all charts
