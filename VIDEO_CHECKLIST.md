# Video Presentation Checklist

Use this checklist to ensure you address all required questions from the assignment.

---

## ✅ Required Questions to Address

### 1. What is interesting about your game from a strategic point of view?
**Covered in**: Slide 3

**Points addressed**:
- ✅ Type advantage system (Fire-Water-Grass triangle)
- ✅ Speed control and turn order
- ✅ Resource management (no healing)
- ✅ Prediction and simultaneous move mind games
- ✅ Switching strategy

---

### 2. What is challenging about your game in terms of developing an agent?
**Covered in**: Slide 4

**Points addressed**:
- ✅ High branching factor (~25 joint actions)
- ✅ Simultaneous moves (uncertainty about opponent)
- ✅ Strong greedy baseline (hard to beat)
- ✅ Medium-large state space
- ✅ Need for lookahead beyond myopic play

---

### 3. What simplifications have you made to improve probability of success?
**Covered in**: Slide 5

**Points addressed**:
- ✅ Reduced team size (6 → 3 Pokémon)
- ✅ Fixed teams (no team building phase)
- ✅ Fewer moves per Pokémon (4 → 2)
- ✅ Removed randomness (crits, accuracy)
- ✅ Removed status effects, items, abilities
- ✅ Simplified stats (6 → 4)
- ✅ Justification: preserves strategy while reducing complexity

---

### 4. Why is your approach reasonable?
**Covered in**: Slide 6

**Points addressed**:
- ✅ MCTS suits perfect information games
- ✅ Handles moderate depth well (10-20 turns)
- ✅ Doesn't need training data
- ✅ Anytime algorithm (adjustable budget)
- ✅ Key innovation: greedy rollouts
- ✅ Adaptation for simultaneous moves
- ✅ Deterministic game benefits MCTS

---

### 5. What other approaches might be better or worse?
**Covered in**: Slide 7

**Points addressed**:
- ✅ Better: Deep RL + value networks (but requires training)
- ✅ Better: CFR for Nash equilibrium (but computationally expensive)
- ✅ Comparable: Minimax/Alpha-Beta (needs heuristic function)
- ✅ Worse: Pure greedy (no lookahead)
- ✅ Worse: Random (obviously poor)
- ✅ Justification of tradeoffs

---

### 6. Similarities/differences with class projects and examples?
**Covered in**: Slide 8

**Points addressed**:
- ✅ Same core MCTS algorithm (UCB1, 4-step loop)
- ✅ Difference: Simultaneous vs sequential moves
- ✅ Difference: Greedy vs random rollouts
- ✅ Difference: Perspective handling in zero-sum game
- ✅ Difference: Complex state representation vs simple boards
- ✅ Specific comparison to class examples (Tic-Tac-Toe, Connect Four)

---

### 7. How do you plan to evaluate your agent?
**Covered in**: Slide 9

**Points addressed**:
- ✅ Benchmark against greedy baseline
- ✅ Multiple computation budgets tested
- ✅ Sample size (50 games per config)
- ✅ Metrics: win rate, time per move
- ✅ Results table with concrete numbers
- ✅ Future work: larger samples, statistical tests

---

## 📋 Technical Requirements

### File Requirements:
- ✅ File name format: `WZhong_Mini-Pokemon-Battle.mp4`
- ✅ Duration: ~5 minutes (can be slightly longer)
- ✅ File size: Tens of MB (not hundreds)
  - Target: 20-50 MB
  - Use 720p or 1080p, H.264 codec, 2-5 Mbps bitrate

### Content Requirements:
- ✅ Title slide held for 10+ seconds (for Media Library preview)
- ✅ Example of gameplay OR link to rules source
  - **Included**: Gameplay demo in Slide 10
  - **Also available**: GAME_SETUP.md describes all rules
- ✅ Narration or captions (accessibility)

### Presentation Format:
- ✅ PowerPoint, Keynote, Google Slides, or similar
- ✅ Exported as video with voiceover
- ✅ Professional quality

---

## 🎥 Pre-Recording Checklist

### Preparation:
- [ ] Review script (VIDEO_PRESENTATION_SCRIPT.md)
- [ ] Create slides using SLIDE_CONTENT.md
- [ ] Record gameplay demo
  - [ ] Run `python3 main.py`, mode 7 (MCTS vs Greedy)
  - [ ] Capture 5-10 turns showing strategic decisions
  - [ ] Edit to ~30 seconds
- [ ] Practice presentation once
- [ ] Set up quiet recording environment
- [ ] Test microphone quality

### Recording:
- [ ] Record narration with slides
- [ ] Ensure title slide shows for 10+ seconds
- [ ] Insert gameplay demo at Slide 10
- [ ] Check audio levels (not too quiet/loud)
- [ ] Re-record any unclear sections

### Post-Production:
- [ ] Export as MP4 (H.264, 720p or 1080p)
- [ ] Check file size (<50 MB ideally)
- [ ] Verify file name: `WZhong_Mini-Pokemon-Battle.mp4`
- [ ] Watch through once to check quality
- [ ] Add captions if possible (optional but nice)

### Submission:
- [ ] Upload to Canvas assignment
- [ ] Course staff will copy to Media Library

---

## 🎬 Gameplay Demo Recording Commands

```bash
# Option 1: MCTS vs Greedy (recommended)
python3 main.py
# When prompted, enter: 7

# Option 2: MCTS vs Random (shows dominance)
python3 main.py
# When prompted, enter: 6

# Show clear examples of:
# - Type advantages (Leaflet vs Aquaff)
# - Speed control (Sparkit outspeeding)
# - Strategic switching by MCTS
# - HP tracking and damage calculation
```

**What to capture**:
- Turn number
- Both players' active Pokémon and HP
- Actions chosen (MCTS thinking time is visible)
- Damage dealt
- Type effectiveness messages
- At least one strategic switch

**Editing tips**:
- Speed up boring turns (1.5-2× speed)
- Add text annotations for key moments
- Highlight type advantages with arrows/circles
- Show 3-5 interesting turns (not entire game)

---

## 📊 Optional: Show Benchmark Results

If you have time (5-10 seconds), you can show:

```bash
python3 final_benchmark.py
```

This will display the results table. You can screenshot this and show briefly in Slide 9.

---

## ⏱️ Time Budget

| Section | Target Time |
|---------|-------------|
| Introduction (Slides 1-2) | 40s |
| Strategic Interest (Slide 3) | 45s |
| Challenges (Slide 4) | 40s |
| Simplifications (Slide 5) | 40s |
| Why MCTS (Slide 6) | 50s |
| Alternatives (Slide 7) | 45s |
| Class Comparison (Slide 8) | 45s |
| Evaluation (Slide 9) | 45s |
| Demo (Slide 10) | 30s |
| Results (Slide 11) | 40s |
| Future Work (Slide 12) | 20s |
| Closing (Slide 13) | 10s |
| **Total** | **~5:30** |

You can trim 30 seconds by:
- Shortening demo to 20s
- Combining Slides 11-12 (Results + Future Work)
- Speaking slightly faster

---

## 🔍 Final Quality Check

Before submitting, verify:
- ✅ All 7 required questions addressed
- ✅ Gameplay footage or rules reference included
- ✅ Clear narration/captions
- ✅ Title slide preview (10+ seconds)
- ✅ Professional quality (no background noise, clear slides)
- ✅ File size reasonable (<100 MB)
- ✅ Correct file name format
- ✅ Video plays correctly before upload

---

## 💡 Pro Tips

1. **Energy**: Speak with enthusiasm! This is cool work.
2. **Pacing**: Pause briefly between slides for comprehension.
3. **Visuals**: Use diagrams/screenshots liberally (not just text).
4. **Demo**: The gameplay footage is engaging—make it count!
5. **Conciseness**: Better to be clear and slightly under 5 min than rushed.
6. **Backup**: Keep your raw recordings in case you need to re-export.

---

## 📚 Reference Files

- `VIDEO_PRESENTATION_SCRIPT.md` - Full narration script
- `SLIDE_CONTENT.md` - Slide-by-slide content to copy into PowerPoint
- `GAME_SETUP.md` - Complete game rules (reference)
- `PROJECT_SUMMARY.md` - Project overview (reference)
- `README.md` - Quick reference (reference)

Good luck! 🎓

