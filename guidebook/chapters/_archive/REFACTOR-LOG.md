# Guidebook Refactoring Log

This file tracks major refactoring operations on the guidebook for ADHD-friendly content curation.

---

## 2025-12-27: Chapter 13 Racecraft Refactor

**Reason:** File hit 707 lines (pain score: 8/10 RED) - too long for ADHD absorption

**Strategy Used:** Split into Micro-Chapters (Strategy A)

### Original Structure
```
13-racecraft.md (707 lines, 13 sections, 5 distinct topics)
```

### New Structure
```
13-racecraft/
├── README.md                      (144 lines - navigation hub)
├── quick-reference.md             (138 lines - race day cheat sheet)
├── 13a-fundamentals.md            (124 lines - mindset & golden rules)
├── 13b-defensive-offensive.md     (229 lines - attack & defense tactics)
├── 13c-cold-tire-contract.md      (230 lines - Lap 1-3 protocol)
├── 13d-meebewegen.md              (250 lines - strategic patience)
└── 13e-race-strategy.md           (199 lines - incidents & management)

Total: 1314 lines (across 7 focused files)
```

### Line Count Comparison

**Original:**
- Single file: 707 lines
- Average section: 54 lines
- Longest section: 207 lines (Meebewegen)

**Refactored:**
- Average file: 188 lines
- Longest file: 250 lines (13d-meebewegen.md)
- Shortest file: 124 lines (13a-fundamentals.md)
- Quick reference: 138 lines (race day use)

**All files within 300-line guideline!** ✅

### Content Distribution

**13a-fundamentals.md** (124 lines)
- Introduction & narrative hook
- The shift from hot lapping to racing
- Golden Rules (Make/Break, Position Hierarchy, Predictability)

**13b-defensive-offensive.md** (229 lines)
- Defensive driving (one-move rule, defending corners)
- Offensive driving (overtake hierarchy, clean pass setup)
- Situational awareness (mirrors, zones)
- Practice drills (shadow lap, AI races)

**13c-cold-tire-contract.md** (230 lines)
- Lap 1: Survival Protocol
- Lap 2: Assessment Protocol
- Lap 3+: Execute Protocol
- When to use vs. not use
- Comparison to Meebewegen

**13d-meebewegen.md** (250 lines)
- The principle & physics
- Master Lonn's discovery (Winton AI race)
- When to use (ideal conditions)
- Practice drills
- ADHD-specific applications

**13e-race-strategy.md** (199 lines)
- Incident management (if hit, if you cause)
- Race strategy basics (sprint vs. endurance)
- Position vs. pace trade-offs
- Practice drills (AI races, shadow laps, replay analysis)
- Master Lonn's next frontier

**quick-reference.md** (138 lines)
- Golden Rules (bullets)
- Lap 1-2-3 protocols (checklists)
- Overtake hierarchy
- Meebewegen quick guide
- Red flags to avoid

**README.md** (144 lines)
- Navigation hub
- Learning path (beginners, race day, specific problems)
- Chapter summaries
- Cross-references

### Cross-References Updated

**Files modified:**
1. `guidebook/chapters/12-mental-game.md` - Next chapter link updated
2. `guidebook/chapters/14-tire-management.md` - Previous chapter link updated
3. `weeks/week03/2025-12-27-11-09-28-race-winton.md` - Meebewegen reference updated

**Links changed:**
- `13-racecraft.md` → `13-racecraft/README.md` (navigation)
- `13-racecraft.md#part-51-meebewegen` → `13-racecraft/13d-meebewegen.md` (specific reference)

### Benefits Achieved

✅ **ADHD-friendly:** Each file = one study session (< 300 lines)  
✅ **Quick reference:** 138-line cheat sheet for race day  
✅ **Easy navigation:** Clear file names, focused topics  
✅ **Searchable:** Specific topics have dedicated files  
✅ **Preserved content:** All 707 lines of content retained, just reorganized  
✅ **Reversible:** Original archived at `_archive/13-racecraft-original.md`

### Pain Score Improvement

**Before:**
- Lines: 707 (4 points)
- Sections: 13 (3 points)
- Depth: 4 levels (1 point)
- **Total: 8/10 (RED)**

**After (per file):**
- Lines: 124-250 (0 points each)
- Sections: 4-8 per file (0 points each)
- Depth: 3 levels max (0 points)
- **Total: 0-1/10 (GREEN)** ✅

### User Feedback

**Master Lonn's trigger:** "It's becoming so long, which is hard to read and absorb for my ADHD brain."

**Solution:** Created `@refactor-long-file.md` command for on-demand refactoring of any file that hits pain threshold.

**Philosophy:** Content should be **curated**, not **accumulated**. Refactor when painful, not on schedule.

---

## Refactoring Guidelines Established

**Pain Score Thresholds:**
- 0-2 points = GREEN (no refactor needed)
- 3-5 points = YELLOW (consider refactoring)
- 6+ points = RED (refactor NOW)

**Length Guidelines:**
- Guidebook chapters: 300 lines MAX
- Session logs: 400 lines MAX
- Week summaries: 200 lines MAX
- Quick references: 50 lines MAX

**Strategies Available:**
- **Strategy A:** Split into Micro-Chapters (multiple distinct topics)
- **Strategy B:** Extract Appendices (core + supplementary material)
- **Strategy C:** Quick Reference + Full Version (dense but coherent)
- **Strategy D:** Consolidate + Remove Redundancy (repeated concepts)

---

## Next Candidates for Refactoring

**Potential files over threshold:**
- `guidebook/chapters/14-tire-management.md` (555 lines)
- `weeks/week03/2025-12-25-13-32-winton-practice.md` (536 lines)
- `.cursor/commands/store-current-session-for-week.md` (224 lines - borderline)

**No rush.** Refactor when they become painful to use, not on a schedule.

---

**Refactored by:** Little Padawan  
**Date:** 2025-12-27  
**Command used:** `@refactor-long-file.md guidebook/chapters/13-racecraft.md`  
**Master Lonn's approval:** ✅ "y"

---

_"Quality over quantity. Better to have 5 focused chapters than 1 massive one."_ 📚✨

