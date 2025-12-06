# Slide-by-Slide Content for Presentation

Copy this content into your presentation software (PowerPoint, Google Slides, Keynote)

---

## SLIDE 1: Title Slide
**Hold for 10+ seconds for Media Library preview**

```
Mini Pokémon Battle with Monte Carlo Tree Search

A Simplified Strategic Battle Game for AI Research

William Zhong
CPSC 474 Final Project
```

---

## SLIDE 2: Game Overview

**Title**: Game Overview

**Content**:
- 3v3 Pokémon team battles
- 8 unique Pokémon: Fire, Water, Grass, Normal types
- Simultaneous turn-based combat
- Each Pokémon has 2 moves
- Actions: Attack or Switch
- **Key Feature**: Completely deterministic (no randomness)

**Visual suggestion**: Screenshot of game interface or team composition diagram

---

## SLIDE 3: Strategic Depth

**Title**: What Makes This Game Strategically Interesting?

**Content**:
1. **Type Advantage**
   - Fire > Grass > Water > Fire triangle
   - 2× damage when super-effective, 0.5× when resisted

2. **Speed Control**
   - Fast Pokémon (Sparkit: Speed 16) attack first
   - Can KO before taking damage

3. **Resource Management**
   - No healing, damage is permanent
   - Decide when to sacrifice vs. preserve

4. **Prediction & Mind Games**
   - Simultaneous moves = anticipate switches
   - Bait opponent into bad matchups

**Visual suggestion**: Type chart diagram, speed comparison

---

## SLIDE 4: AI Development Challenges

**Title**: Challenges for AI Development

**Content**:
- **High branching factor**: ~25 joint actions per turn
  - 5 actions/player × 5 actions/player = 25 combinations

- **Simultaneous moves**: Must model opponent uncertainty
  - Standard MCTS assumes sequential turns

- **Strong greedy baseline**: 94% win rate vs random
  - AI needs sophisticated lookahead to improve

- **Medium-large state space**: Thousands of reachable states
  - 6 Pokémon × HP values × positions × active status

**Visual suggestion**: Tree diagram showing branching factor

---

## SLIDE 5: Simplifications

**Title**: Simplifications for Feasibility

**Table**:
| Aspect | Full Pokémon | My Version |
|--------|-------------|------------|
| Team Size | 6 Pokémon | 3 Pokémon |
| Stats | 6 stats | 4 stats |
| Moves | 4 moves | 2 moves |
| Randomness | Crits, accuracy | None |
| Status | Burn, poison, etc. | None |
| Items | Yes | None |
| Team Selection | Choose from 100s | Fixed teams |

**Why These Work**:
- Preserves core strategic mechanics
- Reduces state space to manageable size
- Deterministic = better for MCTS
- Completable in project timeline

---

## SLIDE 6: Why MCTS is Reasonable

**Title**: Why Monte Carlo Tree Search?

**Content**:
✅ **Perfect information game** - MCTS excels here

✅ **Moderate depth** - Games end in 10-20 turns

✅ **Deterministic** - No wasted simulations on randomness

✅ **Anytime algorithm** - Adjustable computation budget

**Key Innovation: Greedy Rollouts**
- Random rollouts: 20-30% win rate
- Greedy rollouts: 52% win rate
- **Lesson**: Rollout quality is critical!

**Simultaneous Move Adaptation**:
- Model all joint action pairs as tree edges
- Aggregate stats across opponent responses

**Visual suggestion**: MCTS tree diagram with selection/simulation/backprop

---

## SLIDE 7: Alternative Approaches

**Title**: Other Approaches: Better or Worse?

**Content**:

**Better (but harder)**:
- 🧠 **Deep RL + Value Networks**: Train via self-play (AlphaZero-style)
- 🎯 **Counterfactual Regret Minimization**: Find Nash equilibrium

**Comparable**:
- ♟️ **Minimax/Alpha-Beta**: Needs good heuristic evaluation function

**Worse**:
- 😞 **Pure Greedy**: No lookahead (40-48% vs MCTS)
- 🎲 **Random**: Only 6% vs Greedy

**MCTS Advantages**:
- No training data needed
- Works with modest computation
- Handles simultaneous moves naturally

---

## SLIDE 8: Comparison to Class Examples

**Title**: Similarities & Differences from Class MCTS

**Two Columns**:

**Similarities**:
- UCB1 tree policy (exploration/exploitation)
- Same 4-step loop: Select, Expand, Simulate, Backprop
- Track wins/visits for each node

**Key Differences**:

1. **Simultaneous Moves** (vs Sequential)
   - Class: Tic-Tac-Toe, Connect Four alternate turns
   - My game: Model all joint (P1, P2) action pairs

2. **Greedy Rollouts** (vs Random)
   - Class: Random simulations
   - My game: Greedy policy for better value estimates

3. **Perspective Handling**
   - Zero-sum game with simultaneous moves
   - Carefully track whose perspective for UCB/selection

4. **Complex State**
   - Not just board positions
   - HP, teams, active indices, fainted status

**Visual suggestion**: Code snippet or tree diagram comparing approaches

---

## SLIDE 9: Evaluation Strategy

**Title**: How I Evaluate the Agent

**Content**:

**Benchmark Design**:
- MCTS vs Greedy baseline
- 50 games per configuration
- Varied computation budgets

**Results**:
| Simulations | Win Rate | Time/Move |
|-------------|----------|-----------|
| 25          | 40%      | ~0.2s     |
| 50          | 52% ✓    | ~0.4s     |
| 100         | 50%      | ~0.8s     |
| 200         | 38%      | ~1.7s     |
| 500         | 52% ✓    | ~3.3s     |

**Key Findings**:
- ✅ MCTS beats greedy at 50-500 simulations
- ✅ Practical for interactive play (<1s moves)
- ⚠️ Some variance (need larger sample size)

**Future**: 100-200 games, statistical significance testing

---

## SLIDE 10: Live Demo

**Title**: Gameplay Example

**Content**:
[Screen recording showing 3-5 turns]

**What to highlight**:
- HP tracking
- Type advantages (Grass vs Water)
- MCTS strategic switching
- Greedy's myopic damage maximization
- Turn resolution (speed matters)

**Narration points**:
- "MCTS switches to favorable matchup"
- "Greedy just picks max damage"
- "Leaflet resists Water move (0.5×)"

---

## SLIDE 11: Results & Conclusions

**Title**: Key Findings

**Content**:

✅ **MCTS outperforms greedy with lookahead**
   - 52% win rate with 50-500 simulations

✅ **Rollout quality is critical**
   - Random: 20-30% → Greedy: 52%

✅ **Game is tractable but strategic**
   - ~10 hours implementation
   - Rich enough for interesting AI

✅ **Practical for interactive play**
   - 0.4-3.3s per move

**Contribution**:
Demonstrates MCTS effectiveness in simplified strategic battle games with simultaneous moves and type mechanics.

---

## SLIDE 12: Future Extensions

**Title**: Future Work

**Content**:

**AI Improvements**:
- Train value networks (replace rollouts)
- Reinforcement learning (PPO, DQN)
- Tune exploration constant
- Opening book for first moves

**Game Features**:
- Status conditions (burn, poison)
- Items and abilities
- More Pokémon and types
- Team composition optimizer

**Evaluation**:
- Larger sample sizes (200+ games)
- Statistical significance testing
- Tournament between multiple agents

---

## SLIDE 13: Thank You

**Title**: Thank You!

**Content**:
```
Questions?

Project Code Available:
- battle.py - Game engine
- mcts.py - MCTS implementation
- final_benchmark.py - Evaluation framework

William Zhong
CPSC 474 Fall 2024
```

---

## NOTES FOR RECORDING

### Recording Tips:
1. Use a good microphone (AirPods work well)
2. Record in a quiet room
3. Speak clearly and at moderate pace
4. Practice once before final recording
5. Use narration or captions (accessibility)

### Software Options:
- **PowerPoint**: File → Export → Create Video (with narration)
- **Google Slides**: Present → Presenter view → Record
- **Keynote**: File → Record Slideshow
- **Screen recording**: Loom, OBS, QuickTime

### Gameplay Demo Recording:
```bash
# Terminal command to record game:
python3 main.py
# Choose mode 7: MCTS vs Greedy
# Play 5-10 turns
# Use screen recording software to capture
```

### Export Settings:
- Format: MP4 (H.264)
- Resolution: 1280×720 or 1920×1080
- Frame rate: 30 fps
- Bitrate: 2-5 Mbps
- Target size: 20-50 MB for 5 minutes

### File Naming:
`WZhong_Mini-Pokemon-Battle.mp4`

### Accessibility:
- Add captions if possible
- Clear title slide for preview
- High contrast slides

