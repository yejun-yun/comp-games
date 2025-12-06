# Gameplay Demo Recording Guide

This guide will help you record compelling gameplay footage for your video presentation.

---

## 🎯 Goal

Capture 3-5 interesting turns that demonstrate:
1. Strategic decision-making by MCTS
2. Type advantage system
3. Speed mechanics
4. HP/damage tracking
5. Why MCTS beats greedy

**Target length**: 20-30 seconds (edit from longer recording)

---

## 🎮 Recording Setup

### Step 1: Start Screen Recording

**macOS**:
```bash
# QuickTime method:
# 1. Open QuickTime Player
# 2. File → New Screen Recording
# 3. Select recording area (or full screen)
# 4. Click record button

# OR use built-in shortcut:
# Cmd + Shift + 5 (opens screen recording controls)
```

**Windows**:
```bash
# Windows Game Bar:
# Win + G (opens Game Bar)
# Click record button

# OR use OBS Studio (free):
# Download from obsproject.com
```

**Linux**:
```bash
# SimpleScreenRecorder or OBS Studio
```

### Step 2: Launch Game

```bash
cd /Users/williamzhong/Desktop/comp-games
python3 main.py
```

### Step 3: Select Mode

When prompted, enter: **7** (MCTS vs Greedy)

This pits your MCTS agent against the greedy baseline, showcasing strategic superiority.

---

## 📹 What to Capture

### Example Turn Sequence to Record:

**Turn 1-2**: Opening
- Show initial teams
- MCTS makes first decision (may attack or set up)
- Greedy attacks with max damage

**Turn 3-4**: Type Advantage
- Look for a turn where type matchups matter
- Example: Leaflet (Grass) vs Aquaff (Water) = super-effective
- Or: Aquaff (Water) vs Flameling (Fire) = super-effective

**Turn 5-6**: Strategic Switch
- **This is the key moment!**
- MCTS switches to a favorable matchup
- Greedy stays in and takes damage
- This shows lookahead vs myopia

**Turn 7-8**: Speed Control (if it happens)
- Fast Pokémon (Sparkit) KOs opponent before taking damage
- Shows importance of speed stat

**Turn 9-10**: Endgame (optional)
- Final KO
- MCTS wins

---

## 🎬 Ideal Demonstration Moments

### Scenario 1: Type-Advantage Switch (BEST)

**Setup**: MCTS has Leaflet, opponent has Aquaff (Water type)

**What happens**:
1. MCTS switches Leaflet in
2. Greedy uses Water move (resisted, 0.5× damage)
3. MCTS uses Vine Whip (super-effective, 2× damage)
4. Greedy takes massive damage

**Narration**:
> "Notice how MCTS switches to Leaflet against the opponent's Aquaff. This is strategic type-advantage play—Grass beats Water. The greedy agent just picks max damage without considering type matchups."

---

### Scenario 2: Preserving Key Pokemon

**Setup**: MCTS has damaged Pokemon that could survive one more turn

**What happens**:
1. MCTS switches out damaged Pokemon to preserve it
2. Greedy stays in and attacks
3. MCTS brings in counter and KOs later

**Narration**:
> "Here MCTS switches to preserve its damaged Pokémon for later, while greedy stays in myopically. This is multi-turn planning."

---

### Scenario 3: Speed-Based KO

**Setup**: Sparkit (Speed 16) vs slower opponent

**What happens**:
1. Sparkit attacks first (due to higher speed)
2. Opponent faints before attacking
3. Clean KO without taking damage

**Narration**:
> "Sparkit's high speed lets it attack first and KO the opponent before taking damage. Speed control is crucial in this game."

---

## 🎥 Recording Tips

### Before Recording:
- [ ] Close unnecessary windows/apps
- [ ] Disable notifications (Do Not Disturb mode)
- [ ] Make terminal window full screen or large enough to read
- [ ] Ensure good terminal font size (14-16pt)
- [ ] Set terminal theme to high contrast (dark mode works well)

### During Recording:
- [ ] Let each turn display for 2-3 seconds before proceeding
- [ ] Record 10-15 turns (you'll edit down to 5-6)
- [ ] If you get a boring game, restart and record again
- [ ] Look for games where MCTS makes interesting switches

### After Recording:
- [ ] Watch the full recording
- [ ] Identify the 3-5 most interesting turns
- [ ] Edit/trim to 20-30 seconds
- [ ] Add text overlays if desired (optional):
  - "Type Advantage: 2× damage"
  - "MCTS switches strategically"
  - "Speed: Sparkit attacks first"

---

## ✂️ Editing Your Demo

### Option 1: Simple Trim (No Editor Needed)

**macOS QuickTime**:
1. Open recorded video in QuickTime
2. Edit → Trim
3. Drag handles to select best 30 seconds
4. File → Export

**Windows Photos App**:
1. Open video in Photos
2. Click "Edit & Create" → "Trim"
3. Select best segment
4. Save

### Option 2: Advanced Editing (iMovie/DaVinci Resolve)

1. Import full recording
2. Cut out boring turns
3. Speed up repetitive parts (1.5-2×)
4. Add text annotations:
   - "Turn 3: Type Advantage"
   - "MCTS switches to Leaflet (Grass) vs Aquaff (Water)"
   - "Super-effective: 2× damage"
5. Export as MP4

---

## 📊 Alternative: Show Benchmark Results

If you can't get a good gameplay recording, you can instead show:

```bash
python3 final_benchmark.py
```

This displays the results table. Record the terminal output for ~10 seconds showing:
- MCTS vs Greedy across different simulation budgets
- Win rates
- Time per move

**Narration**:
> "Here are the benchmark results across 50 games per configuration. MCTS achieves 52% win rate at 50 and 500 simulations, outperforming the greedy baseline."

---

## 🎤 Narration During Demo

### Option 1: Live Narration

Record voiceover while gameplay plays:

> "Let me show you an example game between MCTS and the greedy agent. In turn 3, MCTS strategically switches to Leaflet to counter the opponent's Aquaff. This type-advantage play deals double damage. The greedy agent can't see this because it only maximizes immediate damage without lookahead."

### Option 2: Text Overlays (Silent Demo)

If narrating feels awkward, add text:
- "MCTS switches for type advantage"
- "Grass beats Water (2× damage)"
- "Greedy stays in and takes massive damage"

---

## 🎯 Success Criteria

Your demo is good if it shows:
- ✅ Clear game state (HP visible)
- ✅ Both players' actions
- ✅ At least one strategic switch by MCTS
- ✅ Damage numbers visible
- ✅ Type effectiveness in action
- ✅ MCTS making a non-obvious move that pays off

---

## 🚨 Troubleshooting

### Problem: MCTS doesn't make interesting moves

**Solution**: Record 2-3 games and pick the best one. With randomness in exploration, some games are more interesting than others.

### Problem: Game ends too quickly

**Solution**: That's actually fine! Just record multiple short games and pick the most strategic turns from each.

### Problem: Terminal text too small in recording

**Solution**: 
```bash
# Increase font size before recording
# Terminal → Preferences → Profiles → Text
# Set font to 16-18pt
```

### Problem: Recording file is huge (>500 MB)

**Solution**: 
- Use screen recording at 720p (not 4K)
- Record only the terminal window, not full screen
- Compress after recording using HandBrake (free tool)

---

## 📱 Quick Reference: Screen Recording Shortcuts

| OS | Shortcut | Tool |
|----|----------|------|
| macOS | Cmd+Shift+5 | Built-in |
| Windows | Win+G | Game Bar |
| Windows | Win+Alt+R | Start/stop recording |

---

## 🎬 Final Demo Checklist

Before inserting into your presentation:
- [ ] Duration: 20-30 seconds
- [ ] Shows at least one strategic MCTS decision
- [ ] Text is readable
- [ ] No personal info visible (desktop icons, etc.)
- [ ] File size reasonable (<20 MB for 30s clip)
- [ ] Format: MP4 (H.264)
- [ ] Audio muted or has narration

---

## 💡 Pro Tip: Multiple Takes

It's totally fine to record 5-10 games and pick the best moments. Look for:
- Games where MCTS wins clearly
- Turns with type advantages
- Moments where MCTS switches and greedy doesn't
- Clear HP changes that demonstrate damage

You're telling a story: **"MCTS thinks ahead and makes smarter decisions than greedy."**

---

Good luck with your recording! 🎥

