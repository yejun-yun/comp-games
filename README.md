# Mini Pokémon Battle Simulator

A simplified Pokémon battle engine for CPSC 474 Final Project.

## Overview

This project implements a deterministic, simplified 3v3 Pokémon battle engine with AI agents.

### Game Features

- **8 Pokémon** in total pool (2 Fire, 2 Water, 2 Grass, 2 Normal)
- **Fixed teams**: Each player gets 3 Pokémon from the pool
- **2 moves per Pokémon**: One typed move + one Normal move
- **Type chart**: Classic Fire > Grass > Water > Fire triangle
- **Simultaneous turns**: Both players choose actions at once
- **No randomness**: Deterministic damage, no critical hits, 100% accuracy
- **AI Agents**: Random, Greedy, and MCTS

📖 **See [GAME_SETUP.md](GAME_SETUP.md) for complete Pokémon stats, movesets, and team compositions.**

## Research Question

**How does MCTS performance scale with computation budget compared to a greedy baseline?**

Results show **dramatic scaling**: MCTS improves from 56% to **92% win rate** as simulation
budget increases from 50 to 1000. The key breakthrough was **opponent modeling** - explicitly
assuming the opponent plays greedy instead of exploring all joint actions.

## Files

### Core Engine

- `battle.py`: Game engine with data structures and logic
- `main.py`: CLI interface with agent implementations (Random, Greedy, Human, MCTS)

### AI Agents

- `mcts.py`: Monte Carlo Tree Search agent with greedy rollout policy

### Benchmarking

- `benchmark.py`: Framework for running agent comparisons
- `final_benchmark.py`: Comprehensive performance analysis
- `quick_benchmark.py`: Fast testing script
- `test_mcts.py`: Unit tests for MCTS

## How to Run

### Play the Game

```bash
python3 main.py
```

Select from modes: Human vs Human/Random/MCTS, or Greedy/MCTS vs Random/Greedy.

### Run Benchmarks

```bash
# Quick test (20 games each)
python3 quick_benchmark.py

# Comprehensive benchmark (50 games, multiple simulation budgets)
python3 final_benchmark.py
```

### Test MCTS

```bash
python3 test_mcts.py
```

## Project Structure

### Core Engine (`battle.py`)

- `PokemonSpec`: Defines static stats for a Pokémon
- `PokemonInstance`: Tracks runtime state (current HP, fainted status)
- `BattleState`: Complete game state (teams, active mons, winner)
- `step(state, action_p1, action_p2)`: Advances the game by one turn
- `legal_actions_for_player(state, player_id)`: Returns valid moves
- `calculate_damage(move, attacker, defender)`: Damage formula

### Agents

#### RandomAgent

Picks random legal actions. Baseline for testing.

#### GreedyAgent

Always chooses the move that deals maximum immediate damage.
Achieves 94% win rate vs Random.

#### MCTSAgent

Monte Carlo Tree Search with:

- UCB1 tree policy for exploration/exploitation
- Greedy rollout policy for value estimation
- Supports configurable simulation budget
- Achieves 52% win rate vs Greedy (at 50-500 simulations)

## Results Summary

### Improved MCTS with Opponent Modeling

| Agent | Simulations | Win Rate vs Greedy |
| ----- | ----------- | ------------------ |
| MCTS  | 50          | 56.0%              |
| MCTS  | 100         | 66.0%              |
| MCTS  | 200         | 78.0%              |
| MCTS  | 500         | 86.0%              |
| **MCTS**  | **1000**    | **92.0%** ✨       |

**Key Finding**: MCTS with opponent modeling achieves **92% win rate** vs Greedy!

The breakthrough was modeling the opponent explicitly as greedy instead of exploring
all joint actions. This reduced tree branching from ~25 to ~5 actions per node,
allowing much deeper and more focused search.

## Future Extensions

- Deeper MCTS with value network evaluation
- Reinforcement learning agents (DQN, PPO)
- Team composition optimization
- Additional game mechanics (status effects, items)
