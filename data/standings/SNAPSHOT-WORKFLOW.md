# Weekly Standings Snapshot Workflow

## Why Snapshots?

To create progression visualizations (iRating charts, position climb graphs, percentile trends), we need **historical CSV snapshots** from each week.

If you overwrite the same standings CSV every week, we lose the historical data needed for trend analysis.

---

## The Workflow (After Each Week)

### Step 1: Download Updated Standings

Download the latest season standings CSV from iRacing after each race week ends.

File typically named: `season-driver_Formula_1600_Rookie_Series_-_2026_Season_1_ccid_4016_rwnum_all_div_all_club_all-N.csv`

### Step 2: Save to Main Location

Save/move to: `data/standings/`

This is your **current working file**.

### Step 3: Create Weekly Snapshot

**CRITICAL STEP:** Save a dated snapshot copy:

```bash
# Create week folder if needed
mkdir -p data/standings/week03

# Copy snapshot
cp data/standings/season-driver_*.csv data/standings/week03/season-standings-week03.csv
```

**Format:**
- Folder: `data/standings/weekXX/`
- Filename: `season-standings-weekXX.csv`

### Step 4: Run Analysis

Now run the standings analysis:

```bash
# Generate standings report
uv run python tools/coach/generate_weekly_standings_report.py 3 data/standings/season-driver_*.csv 1238

# Generate visualizations
uv run python tools/coach/visualize_irating_distribution.py data/standings/season-driver_*.csv 981717 weeks/week03
```

### Step 5: Generate Progression (if 2+ weeks)

Once you have 2+ weekly snapshots, generate progression charts:

```bash
uv run python tools/coach/visualize_standings_progression.py \
    data/standings/week01/season-standings-week01.csv \
    data/standings/week02/season-standings-week02.csv \
    data/standings/week03/season-standings-week03.csv
```

This creates:
- `weeks/progression/assets/irating_progression.png`
- `weeks/progression/assets/position_climb.png`
- `weeks/progression/assets/percentile_progression.png`

---

## Quick Reference Commands

### Week 03 Example

```bash
# 1. Create folder
mkdir -p data/standings/week03

# 2. Save snapshot (after downloading latest CSV)
cp data/standings/season-driver_*.csv data/standings/week03/season-standings-week03.csv

# 3. Analyze standings
uv run python tools/coach/generate_weekly_standings_report.py 3 data/standings/season-driver_*.csv 1238
uv run python tools/coach/visualize_irating_distribution.py data/standings/season-driver_*.csv 981717 weeks/week03

# 4. Generate progression (3 weeks of data now!)
uv run python tools/coach/visualize_standings_progression.py \
    data/standings/week02/season-standings-week02.csv \
    data/standings/week03/season-standings-week03.csv
```

---

## File Structure

```
data/standings/
├── season-driver_*.csv              ← Current working file (updated weekly)
├── week01/
│   └── season-standings-week01.csv  ← Week 01 snapshot (missing - overwritten)
├── week02/
│   └── season-standings-week02.csv  ← Week 02 snapshot (saved!)
├── week03/
│   └── season-standings-week03.csv  ← Week 03 snapshot (to be created)
└── ...
```

---

## Note About Week 01

Week 01 snapshot was lost (overwritten before we established this workflow).

**Impact:**
- Can't generate full progression charts back to Week 01
- Week 02 is our new baseline for visualizations
- Narrative progression report (Week 01→02) created from standings reports

**Going Forward:**
Starting Week 03, we'll have complete CSV snapshots for full progression visualization!

---

## Remember

📸 **Snapshot BEFORE analysis**  
📊 **One snapshot per week**  
📈 **Enables beautiful progression charts!**

