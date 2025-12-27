# Command: Refactor Long File (ADHD-Friendly Content Curation)

## Purpose

Analyze and refactor files that have become too long/complex for ADHD absorption.

**Philosophy:** Content should be curated, not accumulated. When a file hits pain threshold, refactor it.

---

## Usage

```
@refactor-long-file.md <file_path>
```

**Example:**
```
@refactor-long-file.md guidebook/chapters/13-racecraft.md
```

---

## What This Command Does

### Step 1: Analyze Current File

Little Padawan will:
1. **Count lines** (total length)
2. **Identify sections** (headings structure)
3. **Assess complexity** (how many concepts per section)
4. **Check for redundancy** (repeated information)
5. **Calculate pain score** (ADHD absorption difficulty)

**Pain Score Calculation:**
- Lines: 1 point per 100 lines over 300
- Sections: 1 point per section over 10
- Depth: 1 point per heading level over 3
- Redundancy: 2 points if detected

**Pain Threshold:**
- 0-2 points = Fine (no refactor needed)
- 3-5 points = Yellow (consider refactoring)
- 6+ points = Red (refactor NOW)

### Step 2: Propose Refactoring Strategy

Based on analysis, Little Padawan suggests ONE of these strategies:

#### Strategy A: Split into Micro-Chapters
**When:** File has multiple distinct topics (e.g., Chapter 13 covers Cold Tire Contract + Overtaking + Meebewegen)

**Action:**
```
Original: 13-racecraft.md (700 lines, 3 topics)

Becomes:
13-racecraft/
├── quick-reference.md         (50 lines - cheat sheet)
├── 13a-cold-tire-contract.md  (150 lines)
├── 13b-overtaking-defense.md  (200 lines)
├── 13c-meebewegen.md          (150 lines)
└── README.md                  (navigation hub)
```

#### Strategy B: Extract Appendices
**When:** File has core content + lots of supplementary material (examples, data, drills)

**Action:**
```
Original: session-analysis.md (600 lines)

Becomes:
├── session-analysis.md        (300 lines - core analysis)
├── appendix-telemetry.md      (200 lines - detailed data)
└── appendix-drills.md         (100 lines - practice exercises)
```

#### Strategy C: Create Quick Reference + Full Version
**When:** File is dense but coherent (can't easily split topics)

**Action:**
```
Original: 14-tire-management.md (500 lines)

Becomes:
├── 14-tire-management-quick.md  (50 lines - bullets only)
└── 14-tire-management-full.md   (500 lines - keep existing)
```

#### Strategy D: Consolidate + Remove Redundancy
**When:** File has repeated concepts, outdated info, or unnecessary verbosity

**Action:**
1. Identify redundant sections
2. Merge similar content
3. Remove outdated information
4. Tighten prose (cut 30-40%)
5. Keep in single file (but shorter)

### Step 3: Execute Refactor

Little Padawan will:
1. **Create new file structure** (based on chosen strategy)
2. **Move/split content** (preserving all information)
3. **Update cross-references** (fix links in other files)
4. **Create navigation** (README or quick-reference)
5. **Archive original** (move to `_archive/` for safety)

### Step 4: Update References

Check these locations for links to refactored file:
- Other guidebook chapters
- Session logs (weeks/)
- Commands (.cursor/commands/)
- Learning memory (learning_memory.json)

Update any references to point to new structure.

---

## Content Length Guidelines

**Guidebook Chapters:**
- Quick reference: **50 lines MAX**
- Micro-chapter: **150-300 lines** (one focused topic)
- Full chapter: **300 lines MAX** (if single topic)
- If longer → split into micro-chapters

**Session Logs:**
- Session analysis: **400 lines MAX**
- If longer → move deep dives to separate files

**Week Summaries:**
- Summary: **200 lines MAX**
- If longer → you're writing a novel, not a summary

**Commands/Rules:**
- Command: **100 lines MAX**
- Rule doc: **300 lines MAX**

---

## Quick Reference Creation Rules

Every refactored chapter MUST have a quick reference with:

**Structure:**
```markdown
# [Chapter Name] - Quick Reference

## Core Principle (1-2 sentences)

## Key Concepts (bullets only)
- Concept 1
- Concept 2
- Concept 3

## Checklist (actionable items)
- [ ] Action 1
- [ ] Action 2

## When to Use
- Scenario 1
- Scenario 2

## Red Flags (What NOT to do)
- ❌ Anti-pattern 1
- ❌ Anti-pattern 2

→ Full chapter: [link]
```

**Rules:**
- NO prose (bullets/checklists only)
- NO examples (link to full chapter)
- NO theory deep-dives (that's what full version is for)
- 50 lines MAXIMUM

---

## Example Output

**For `guidebook/chapters/13-racecraft.md` (707 lines):**

**Analysis:**
```
File: 13-racecraft.md
Lines: 707
Sections: 15
Topics identified: 4 (Cold Tire Contract, Overtaking, Meebewegen, Incident Management)
Pain Score: 8 (RED - refactor NOW)

Recommendation: Strategy A (Split into Micro-Chapters)
```

**Proposed Structure:**
```
guidebook/chapters/13-racecraft/
├── README.md                  (Navigation hub)
├── quick-reference.md         (50 lines - race day cheat sheet)
├── 13a-cold-tire-contract.md  (180 lines - Laps 1-3 protocol)
├── 13b-overtaking-defense.md  (220 lines - Attack & defend tactics)
├── 13c-meebewegen.md          (200 lines - Strategic patience)
└── appendix-drills.md         (150 lines - Practice exercises)
```

**Execution Plan:**
1. Create directory: `guidebook/chapters/13-racecraft/`
2. Create quick-reference.md (Golden Rules, protocols, checklists)
3. Split content:
   - 13a: Parts 1, 2, 5 (Rules, Defense, Cold Tire Contract)
   - 13b: Parts 3, 4 (Offense, Awareness)
   - 13c: Part 5.1 (Meebewegen + Master Lonn's race)
   - Appendix: Parts 6, 7 (Drills, Strategy)
4. Create README.md (navigation + learning path)
5. Update cross-references (4 files need updating)
6. Archive original to `_archive/13-racecraft-original.md`

**Proceed with refactor? (y/n)**

---

## When to Run This Command

**Triggers to refactor:**
- 🔴 File > 500 lines and multiple topics
- 🔴 You avoid reading a file because it's "too long"
- 🔴 You can't find information in a file anymore
- 🔴 You're about to add MORE to an already long file
- 🟡 File > 400 lines but single coherent topic (consider quick reference)
- 🟡 Someone (you) complains about file length

**Don't refactor if:**
- File < 300 lines (it's fine)
- File is long but you reference it easily (working well)
- File is data/logs (those are meant to be long)

---

## Workflow Integration

**During session storage:**
```bash
# Store session (normal workflow)
@store-current-session-for-week.md

# If session log is getting long
@refactor-long-file.md weeks/weekXX/session-name.md
```

**During guidebook updates:**
```bash
# Add discovery to guidebook
@update-guidebook-chapter.md

# If chapter is now too long
@refactor-long-file.md guidebook/chapters/XX-chapter-name.md
```

**Manual check (weekly):**
```bash
# List files by line count
find guidebook weeks -name "*.md" -exec wc -l {} \; | sort -rn | head -20

# Refactor the long ones
@refactor-long-file.md [file_path]
```

---

## Refactoring Philosophy

**Old way (Accumulation):**
```
Session 1: Add content
Session 2: Add more content  
Session 3: Add even more content
Session 10: File is 1000 lines, unreadable
```

**New way (Curation):**
```
Session 1: Add content
Session 2: Add content
Session 3: File hits 400 lines → REFACTOR
  ├─ Remove redundancy
  ├─ Split if needed
  └─ Create quick reference
Session 4: Add to appropriate micro-chapter
```

**The Rule:**
> "Before you add, ask: Should I refactor first?"

---

## Success Criteria

After refactoring, the file(s) should:
- ✅ Be readable in one sitting (< 300 lines per file)
- ✅ Have clear focus (one topic per file)
- ✅ Have quick reference available (50 lines)
- ✅ Be easy to navigate (clear structure)
- ✅ Preserve all original information (nothing lost)
- ✅ Feel "lighter" to read (ADHD-friendly)

**Master Lonn's test:**
"Can I skim the quick reference in 60 seconds and know what to do?"

If YES → refactor succeeded.
If NO → refactor again.

---

## Notes

- **No rush**: Refactor when file becomes painful, not on a schedule
- **Incremental**: One file at a time, not whole guidebook at once
- **Safe**: Original always archived before refactoring
- **Reversible**: If refactor doesn't help, restore original
- **Quality over quantity**: Better to have 5 focused chapters than 1 massive one

---

**Created:** 2025-12-27  
**By:** Little Padawan (at Master Lonn's very smart suggestion) ✨

