# How to Create Your Video Presentation

## 📚 Overview

I've created comprehensive materials to help you create your 5-minute video presentation for CPSC 474. Here's what you have:

---

## 📁 Files Created for You

### 1. **VIDEO_PRESENTATION_SCRIPT.md** 📝
- Complete narration script for all 13 slides
- Word-for-word dialogue you can read or adapt
- Time allocations for each section
- Total: ~5 minutes 30 seconds

### 2. **SLIDE_CONTENT.md** 🎨
- Ready-to-copy content for PowerPoint/Google Slides
- Bullet points, tables, and visuals suggestions
- Organized by slide number
- Just copy-paste into your presentation software

### 3. **VIDEO_CHECKLIST.md** ✅
- Ensures you address all 7 required questions
- Technical requirements (file size, format, naming)
- Pre-recording, recording, and post-production checklists
- Quality assurance checks

### 4. **DEMO_RECORDING_GUIDE.md** 🎮
- Step-by-step guide to record gameplay footage
- What scenarios to capture
- Editing tips and tools
- Troubleshooting common issues

### 5. **This File (VIDEO_INSTRUCTIONS.md)** 📋
- Quick start guide
- Workflow overview
- Timeline suggestions

---

## 🚀 Quick Start (3-Step Process)

### Step 1: Create Slides (1-2 hours)

1. Open PowerPoint, Google Slides, or Keynote
2. Open `SLIDE_CONTENT.md`
3. Create 13 slides by copying content from that file
4. Add visuals:
   - Type chart diagram (Slide 3)
   - MCTS tree diagram (Slide 6)
   - Results table (Slide 9) - can screenshot from `PROJECT_SUMMARY.md`
   - Your team compositions (can reference `GAME_SETUP.md`)

**Resources**:
- Use simple diagrams (draw.io, Google Drawings, or PowerPoint shapes)
- Keep slides clean and readable
- High contrast (dark text on light background or vice versa)

### Step 2: Record Gameplay Demo (30 minutes)

1. Follow `DEMO_RECORDING_GUIDE.md`
2. Run `python3 main.py` and select mode 7 (MCTS vs Greedy)
3. Record screen while playing
4. Look for interesting turns (strategic switches, type advantages)
5. Edit down to 20-30 seconds
6. Insert into Slide 10

### Step 3: Record Narration & Export (1 hour)

1. Open `VIDEO_PRESENTATION_SCRIPT.md`
2. Practice reading through once
3. Record presentation with voiceover:
   - **PowerPoint**: Slide Show → Record Slide Show
   - **Google Slides**: Use Loom or screen record with voiceover
   - **Keynote**: File → Record Slideshow
4. Hold title slide for 10+ seconds
5. Export as MP4:
   - 720p or 1080p
   - H.264 codec
   - 2-5 Mbps bitrate
6. Check file size (<50 MB ideally)
7. Name file: `WZhong_Mini-Pokemon-Battle.mp4`

---

## ⏱️ Suggested Timeline

### If you have 1 day:
- **Morning**: Create slides (2 hours)
- **Afternoon**: Record demo (30 min), practice narration (30 min)
- **Evening**: Record final video (1 hour), review and submit (30 min)

### If you have 1 week:
- **Day 1-2**: Create slides, gather visuals
- **Day 3**: Record gameplay demo, edit
- **Day 4-5**: Practice narration
- **Day 6**: Record final video
- **Day 7**: Review, polish, submit

---

## ✅ Required Questions Coverage

Your materials address all 7 required questions:

| Question | Covered In |
|----------|-----------|
| What's strategically interesting? | Slide 3 |
| What's challenging for AI? | Slide 4 |
| What simplifications were made? | Slide 5 |
| Why is MCTS reasonable? | Slide 6 |
| What approaches are better/worse? | Slide 7 |
| How does it compare to class? | Slide 8 |
| How do you evaluate? | Slide 9 |

✅ **Gameplay demonstration**: Slide 10  
✅ **Rules reference**: GAME_SETUP.md (can mention in presentation)

---

## 🎯 Key Points to Emphasize

### Your Main Contributions:
1. ✨ **Greedy rollouts** (20-30% → 52% win rate improvement)
2. ✨ **Simultaneous move adaptation** (joint action modeling)
3. ✨ **Strong baseline** (greedy at 94% vs random)
4. ✨ **Deterministic design** (perfect for MCTS)

### Your Key Results:
- MCTS achieves **52% win rate** vs greedy baseline
- Practical performance: **0.4-3.3s** per move
- Lookahead provides measurable advantage
- Rollout quality is critical for MCTS success

---

## 🎨 Slide Design Tips

### Visual Suggestions:

**Slide 3** (Strategic Depth):
```
Fire → Grass → Water → Fire
 ↑                      ↓
 └──────────────────────┘

2× damage when super-effective
0.5× damage when not very effective
```

**Slide 4** (Branching Factor):
```
        Root
       / | | | \
      5 actions per player
    ↓
   25 joint actions
```

**Slide 6** (MCTS Tree):
```
     Selection → Expansion → Simulation → Backpropagation
        UCB1        New node    Greedy       Update stats
```

**Slide 9** (Results Table):
Use the actual table from PROJECT_SUMMARY.md or create a bar chart.

---

## 📹 Recording Software Options

### Free Options:
- **PowerPoint** (Windows/Mac): Built-in recording
- **Google Slides + Loom**: Free screen recording with webcam
- **Keynote** (Mac): Built-in recording
- **OBS Studio**: Free, professional quality

### Paid Options:
- **Camtasia**: Screen recording + editing ($250, free trial)
- **ScreenFlow** (Mac): Similar to Camtasia ($170)

### Recommended for Beginners:
→ **PowerPoint** or **Google Slides + Loom** (easiest)

---

## 🎤 Narration Tips

### Before Recording:
- Practice reading script out loud 2-3 times
- Mark places to pause or emphasize
- Have water nearby
- Eliminate background noise

### During Recording:
- Speak clearly and at moderate pace
- Don't rush (5:30 is fine for target 5:00)
- Pause between slides for breath
- Smile while talking (improves voice tone)
- Re-record any stumbles (edit later)

### Voice Quality:
- Use headphones with mic (AirPods work well)
- Or use laptop mic (usually acceptable)
- Record in a quiet room (closet with clothes dampens echo)

---

## 📤 Submission Checklist

Before submitting, verify:

- [ ] File name: `WZhong_Mini-Pokemon-Battle.mp4`
- [ ] File size: <100 MB (ideally 20-50 MB)
- [ ] Duration: ~5 minutes (±30 seconds is fine)
- [ ] Title slide visible for 10+ seconds
- [ ] All 7 questions addressed
- [ ] Gameplay demo or rules reference included
- [ ] Audio is clear (no distortion, not too quiet)
- [ ] Video plays correctly (test before uploading)
- [ ] Format: MP4 (H.264)

---

## 🆘 Need Help?

### Common Issues:

**Q: File too large (>100 MB)?**
A: 
- Re-export at 720p instead of 1080p
- Reduce bitrate to 2 Mbps
- Use HandBrake to compress (free tool)

**Q: Nervous about narration?**
A:
- Write out exactly what you'll say (script provided!)
- Practice 3-5 times before recording
- Record in short segments, combine later
- Remember: Course staff want to hear your insights, not judge presentation skills

**Q: Gameplay demo isn't interesting?**
A:
- Record 3-5 games, pick best moments
- Edit to show only strategic turns
- Add text overlays to explain what's happening
- Alternatively: Just show the benchmark results table

**Q: Don't have PowerPoint?**
A:
- Use Google Slides (free)
- Use Keynote (free on Mac)
- Use LibreOffice Impress (free)

---

## 🎓 Final Thoughts

You've built a solid project:
- Clean game engine
- Working MCTS implementation
- Meaningful results (52% vs greedy)
- Interesting AI challenges

The video is your chance to explain **why this matters** and **what you learned**.

Focus on:
1. The **greedy rollout insight** (big win)
2. **Simultaneous move challenge** (technical depth)
3. **Tradeoffs** between simplicity and strategy

You've got this! 🚀

---

## 📞 Quick Reference

| Need | File |
|------|------|
| What to say | `VIDEO_PRESENTATION_SCRIPT.md` |
| Slide content | `SLIDE_CONTENT.md` |
| Checklist | `VIDEO_CHECKLIST.md` |
| Record demo | `DEMO_RECORDING_GUIDE.md` |
| Game rules | `GAME_SETUP.md` |
| Project details | `PROJECT_SUMMARY.md` |

---

**File Naming**: `WZhong_Mini-Pokemon-Battle.mp4`

**Submission**: Canvas assignment (course staff will copy to Media Library)

**Due Date**: [Check your course calendar]

---

Good luck with your presentation! 🎬

