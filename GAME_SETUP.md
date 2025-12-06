# Game Setup: Mini Pokémon Battle

## Overview

This is a simplified 3v3 Pokémon battle with fixed teams and deterministic mechanics.

---

## Pokémon Pool (DEX)

There are **8 Pokémon** available in the game, distributed across 4 types:

### Fire Type (2 Pokémon)

#### 1. Flameling

- **HP**: 60
- **Attack**: 18
- **Defense**: 10
- **Speed**: 14
- **Moves**:
  - Ember (Fire, Power 16) - Super effective vs Grass
  - Quick Jab (Normal, Power 10)

#### 2. Sparkit

- **HP**: 50
- **Attack**: 19 (highest attack!)
- **Defense**: 9 (glass cannon)
- **Speed**: 16 (fastest!)
- **Moves**:
  - Flame Dash (Fire, Power 18) - Strongest Fire move
  - Scratch (Normal, Power 10)

### Water Type (2 Pokémon)

#### 3. Aquaff

- **HP**: 65
- **Attack**: 16
- **Defense**: 12
- **Speed**: 12
- **Moves**:
  - Splash Shot (Water, Power 16) - Super effective vs Fire
  - Body Slam (Normal, Power 12)

#### 4. Torrento

- **HP**: 70
- **Attack**: 15
- **Defense**: 14 (bulky)
- **Speed**: 10
- **Moves**:
  - Water Jet (Water, Power 17)
  - Headbutt (Normal, Power 13)

### Grass Type (2 Pokémon)

#### 5. Leaflet

- **HP**: 55
- **Attack**: 17
- **Defense**: 11
- **Speed**: 13
- **Moves**:
  - Vine Whip (Grass, Power 16) - Super effective vs Water
  - Tackle (Normal, Power 11)

#### 6. Sprouty

- **HP**: 58
- **Attack**: 16
- **Defense**: 12
- **Speed**: 15 (second fastest)
- **Moves**:
  - Leaf Slice (Grass, Power 17)
  - Bash (Normal, Power 12)

### Normal Type (2 Pokémon)

#### 7. Bulkwall

- **HP**: 80 (highest HP!)
- **Attack**: 14
- **Defense**: 16 (highest defense!)
- **Speed**: 8 (slow tank)
- **Moves**:
  - Heavy Slam (Normal, Power 18) - Strongest Normal move
  - Guard Strike (Normal, Power 12)

#### 8. Stonecub

- **HP**: 75
- **Attack**: 15
- **Defense**: 15 (balanced tank)
- **Speed**: 9
- **Moves**:
  - Rock Punch (Normal, Power 17)
  - Steady Blow (Normal, Power 13)

---

## Team Compositions

### Team 1 (Player 1)

1. **Flameling** (Fire)
2. **Leaflet** (Grass)
3. **Stonecub** (Normal)

**Strategy**: Balanced team with type coverage (Fire/Grass/Normal). Stonecub provides bulk.

### Team 2 (Player 2)

1. **Aquaff** (Water)
2. **Sparkit** (Fire)
3. **Bulkwall** (Normal)

**Strategy**: Strong defensive core (Bulkwall) with offensive threats (Sparkit).

---

## Type Chart

Classic Fire-Water-Grass triangle:

| Attacker → Defender | Fire | Water | Grass | Normal |
| ------------------- | ---- | ----- | ----- | ------ |
| **Fire**            | 1.0x | 0.5x  | 2.0x  | 1.0x   |
| **Water**           | 2.0x | 1.0x  | 0.5x  | 1.0x   |
| **Grass**           | 0.5x | 2.0x  | 1.0x  | 1.0x   |
| **Normal**          | 1.0x | 1.0x  | 1.0x  | 1.0x   |

- **Super Effective (2.0x)**: Fire → Grass, Water → Fire, Grass → Water
- **Not Very Effective (0.5x)**: Fire → Water, Water → Grass, Grass → Fire
- **Neutral (1.0x)**: Everything else

---

## Damage Formula

```python
damage = floor(base_power × (attack / defense) × type_multiplier)
damage = max(damage, 1)  # Minimum 1 damage
```

**Example**: Sparkit's Flame Dash (Power 18) vs Leaflet (Defense 11)

- Base damage = 18 × (19/11) × 2.0 = 61.9
- Final damage = floor(61.9) = **61 HP**
- This nearly one-shots Leaflet (55 HP)!

---

## Move Properties

Every Pokémon has **exactly 2 moves**:

1. **Typed Move**: Matches the Pokémon's type (or is typed for coverage)
2. **Normal Move**: Always neutral damage

**Key Properties**:

- 100% accuracy (all moves always hit)
- No critical hits
- No status effects (no burn, poison, paralysis, etc.)
- No recharge or cooldown
- Deterministic damage (no random variance)

---

## Battle Mechanics

### Team Size

- Each player has **3 Pokémon**
- Only 1 active at a time
- 2 on the bench

### Actions Per Turn

Players simultaneously choose:

1. **Attack**: Use Move 1 or Move 2
2. **Switch**: Swap to a benched Pokémon (if available)

### Turn Resolution Order

1. **Switches go first** (both players if both switch)
2. **Attacks resolve by Speed**:
   - Higher Speed attacks first
   - Ties: Player 1 goes first
   - If a Pokémon faints, it can't attack back

### Fainting

- When HP reaches 0, the Pokémon faints
- Fainted Pokémon cannot be switched to or attack
- If active Pokémon faints, must switch next turn

### Win Condition

- Game ends when all 3 Pokémon on one side faint
- If both faint simultaneously: **Draw**

---

## Strategic Depth

Despite simplifications, the game has interesting strategic elements:

### 1. Type Advantage

- Switching to resist opponent's moves
- Using super-effective attacks (2x damage)

### 2. Speed Control

- Fast Pokémon (Sparkit, Sprouty) can KO before taking damage
- Slow tanks (Bulkwall) need to survive the first hit

### 3. HP Management

- When to keep damaged Pokémon in vs switching
- Preserving key type matchups

### 4. Prediction

- Anticipating opponent switches
- Baiting switches with weak attacks

### 5. Resource Management

- Each Pokémon can only faint once
- No healing (damage is permanent)
- Managing which Pokémon to sacrifice

---

## Design Choices

### Why These Teams?

The fixed teams were chosen to create balanced matchups:

**Team 1 Advantages**:

- Leaflet beats Aquaff (Grass > Water)
- Stonecub is a reliable tank

**Team 2 Advantages**:

- Aquaff beats Flameling (Water > Fire)
- Bulkwall has highest HP/Defense
- Sparkit has highest Attack/Speed

**Result**: Neither team has overwhelming advantage, making strategy important.

### Why Fixed Stats?

Small integer stats (HP: 50-80, Attack: 14-19, Defense: 9-16) make damage calculations:

- Easy to compute mentally
- Meaningful differences between Pokémon
- Fast to simulate for AI

### Why No Randomness?

Removing critical hits, accuracy, and damage variance makes the game:

- **Deterministic**: Same state + actions = same outcome
- **Debuggable**: Easy to trace errors
- **Fair for AI**: MCTS/search don't need to average over random outcomes
- **Reproducible**: Experiments give consistent results

---

## Statistics Summary

| Metric                 | Value                            |
| ---------------------- | -------------------------------- |
| Total Pokémon          | 8                                |
| Types                  | 4 (Fire, Water, Grass, Normal)   |
| Pokémon per Team       | 3                                |
| Moves per Pokémon      | 2                                |
| Actions per Turn       | 5 (2 attacks + 3 switch targets) |
| Joint Actions per Turn | ~25 (5 × 5)                      |
| HP Range               | 50-80                            |
| Attack Range           | 14-19                            |
| Defense Range          | 9-16                             |
| Speed Range            | 8-16                             |
| Move Power Range       | 10-18                            |

This creates a **manageable but non-trivial** state space perfect for MCTS experiments!
