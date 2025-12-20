# Little Padawan - Adaptive iRacing Coach

**Master Lonn's** personal AI racing coach that learns from data and conversations to help you get faster.

---

## What Is This?

Little Padawan is your adaptive racing coach that:
- 🧠 **Remembers your journey** - Tracks what you're working on and what you've mastered
- 🎯 **Focuses on ONE thing** - No information overload, just what matters
- 💬 **Talks first, visualizes second** - Conversation-driven coaching
- 🛠️ **Builds tools on-demand** - Creates analysis only when it helps you improve
- 📈 **Adapts to you** - Learns your style and what works for you

---

## Quick Start

### 1. Export Your Session Data

From Garage 61 (or iRacing), export your session as CSV with:
- Lap times
- Sector times (if available)
- Incidents

Save it to the `data/` folder.

### 2. Talk to Little Padawan (via Cursor)

```
"Hey Little Padawan, analyze my Rudskogen session"
```

Little Padawan will:
1. Load your session data
2. Check what you're currently working on (from memory)
3. Analyze the data
4. Ask you questions to understand your goals
5. Give you focused coaching

### 3. That's It!

Little Padawan remembers everything and adapts to you over time.

---

## How It Works

### Learning Memory

Little Padawan tracks:
- **Current Focus**: What you're working on right now ("S2 consistency")
- **Mastered Skills**: What you've already nailed
- **Learning Patterns**: What coaching style works for you
- **Session History**: Your progress over time
- **Tool Usage**: Which analyses help you vs which don't

Everything is stored in `learning_memory.json`

### Conversation-Driven

Little Padawan doesn't dump data on you. It asks:
- "What are you working on?"
- "What felt challenging?"
- "Do you want to see charts or just numbers?"

Then gives you **exactly what helps**, nothing more.

### On-Demand Tools

If you need analysis that doesn't exist, Little Padawan creates it on the fly:
- Generates Python script in `tools/generated/`
- Runs it for you
- Tracks if it was helpful
- Keeps it if you use it again, deletes it if you don't

---

## Example Session

```
You: "Hey Little Padawan, analyze my first Rudskogen session"

Little Padawan:
"Welcome to Rudskogen, Master! I see 18 laps, best 90.29s.

Before I dive deeper:
- What's your goal? Consistency or pace first?
- What felt challenging?"

You: "Consistency first. The Angst hill felt scary."

Little Padawan:
"Your instinct is spot on! Sector 2 (the hill):
- Best: 30.85s
- Average: 31.75s (0.9s slower)
- Variance: 0.63s (3x higher than other sectors!)

Let's make S2 consistency your focus.
Goal: S2 average under 31.0s

Want me to show you a chart or are numbers enough?"

You: "Numbers are enough."

Little Padawan:
"Got it! I'll track your S2 progress. Go get 'em! 🏁"

[Updates learning_memory.json with your focus and preference]
```

---

## Folder Structure

```
iracing-adaptive-coach-nbaapl/
├── learning_memory.json          # Your learning journey (tracked by Little Padawan)
├── .cursorrules                   # Little Padawan's coaching instructions
├── data/                          # Put your session CSVs here
├── sessions/                      # Session notes and analysis
├── tools/
│   ├── core/                      # Core utilities (always available)
│   │   └── data_loader.py         # Load sessions, analyze basics
│   └── generated/                 # Tools created on-demand by Little Padawan
└── README.md                      # This file
```

---

## Philosophy

### Start Minimal
Little Padawan doesn't assume what you need. It starts with conversation and builds from there.

### Learn from You
Every session, Little Padawan learns:
- What coaching style works for you
- What analyses help vs overwhelm
- What goals motivate you
- How you improve best

### Focus on ONE Thing
No information overload. One focus area at a time until you master it.

### Build Tools When Needed
Don't pre-build everything "just in case". Create analysis only when it helps you get faster.

### Adapt and Evolve
Little Padawan gets better at coaching you over time by remembering what works.

---

## What Little Padawan Does

✅ Analyzes your session data in context of your goals
✅ Identifies ONE focus area (not everything at once)
✅ Gives specific, actionable coaching
✅ Remembers your journey across sessions
✅ Creates visualizations only when they help
✅ Adapts to your learning style
✅ Celebrates your progress!

## What Little Padawan Doesn't Do

❌ Dump all possible data on you
❌ Create visualizations "just because"
❌ Give vague advice like "practice more"
❌ Forget what you're working on
❌ Assume what you need without asking

---

## Getting Started

1. **Put your session CSV in `data/`**
2. **Open Cursor and say**: `"Hey Little Padawan, analyze my [track] session"`
3. **Answer Little Padawan's questions** about your goals
4. **Get focused coaching** on what to improve
5. **Practice and repeat!**

Little Padawan will remember everything and help you get faster over time.

---

## Tips

### First Session
Little Padawan will ask lots of questions to understand you. Be honest about:
- Your goals (consistency vs pace)
- What you find helpful (charts vs numbers)
- What feels challenging

### After a Few Sessions
Little Padawan will know you better and adapt automatically:
- Remembers your current focus
- Knows your preferred coaching style
- Tracks your progress toward goals

### When You Master Something
Tell Little Padawan! It will:
- Mark the skill as mastered
- Help you pick the next challenge
- Track your growth over time

---

## Example Workflows

### "I Just Did a Practice Session"
```
You: "Analyze my session"
Little Padawan: [Checks current focus, analyzes data]
                "Your S2 consistency improved! 
                 Session 1: avg 31.75s
                 Today: avg 31.18s
                 You're 0.18s from your goal of 31.0s!"
```

### "I Want to Work on Something New"
```
You: "I want to focus on qualifying pace now"
Little Padawan: [Updates current focus]
                "Got it! Let's analyze your theoretical optimal lap.
                 Your best sectors combined: 89.99s
                 Your best lap: 90.29s
                 Gap: 0.30s available
                 
                 Where do you think that 0.3s is?"
```

### "Show Me My Progress"
```
You: "How am I doing overall?"
Little Padawan: [Reviews session history]
                "You've done 8 sessions since Dec 16:
                 
                 Mastered:
                 ✓ Jefferson Circuit baseline (σ = 0.38s)
                 
                 Current Focus:
                 → Rudskogen S2 consistency (3/8 sessions, improving!)
                 
                 Your consistency improvement rate: Fast
                 Your pace improvement rate: Moderate
                 
                 You respond well to: focused practice, specific goals"
```

---

## Need Help?

Little Padawan is here to help you get faster. Just talk to it via Cursor and it will figure out what you need.

**Let's get you on the podium, Master Lonn! 🏁**
