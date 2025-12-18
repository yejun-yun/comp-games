# RAVE (Rapid Action Value Estimation) for Simultaneous-Move Games

## Overview

RAVE enhances MCTS by sharing action statistics across the search tree using the All-Moves-As-First (AMAF) heuristic: if an action leads to wins later in a simulation, it's likely good earlier too.

## Algorithm

### Standard MCTS Recap

1. **Selection**: Traverse tree using UCB1 until reaching unexpanded node
2. **Expansion**: Add new child node
3. **Rollout**: Random playout to terminal state
4. **Backpropagation**: Update visit/win counts along path

### RAVE Modification

RAVE adds AMAF statistics at each node:

```
amaf_stats[(player, action)] = [visits, wins]
```

Updated whenever `action` appears *anywhere* in a simulation passing through that node.

### Selection Formula

```
beta = sqrt(K / (3*N + K))           # N = child visits, K = tuning parameter
value = (1-beta) * UCB + beta * AMAF
```

- Low visits → beta ≈ 1 → trust AMAF (heuristic guidance)
- High visits → beta ≈ 0 → trust UCB (real data)

## Adaptation for Simultaneous Games

### Problem

Standard RAVE assumes sequential moves. In simultaneous games:
- Both players act at once → joint actions (a1, a2)
- We only control one player's action

### Solution

Only use AMAF for the **controlling player's action**:

```python
my_action = a1 if my_player == 1 else a2
amaf = node.amaf_stats[(my_player, my_action)]
```

**Rationale**: We want to find good actions for *us*. Opponent's AMAF tells us which opponent actions correlated with our wins (i.e., opponent mistakes), which doesn't help us choose better moves.

### Final Action Selection

Uses minimax at root (same as standard MCTS):

```
For each of my actions:
    worst_case = min over opponent responses of win_rate
Select action with best worst_case
```

This assumes opponent plays optimally, making the agent robust.

## Files

- `mcts_rave.py` - Implementation
- `benchmark_rave.py` - Performance comparison vs standard MCTS

## Usage

```python
from mcts_rave import MCTSRAVEAgent

agent = MCTSRAVEAgent(
    simulations_per_move=100,  # Simulation budget
    player_id=1,               # Which player we control
    rave_k=500                 # AMAF decay parameter (lower = faster decay)
)

action = agent.choose_action(state, player_id=1)
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `simulations_per_move` | 1000 | Number of MCTS iterations per decision |
| `rave_k` | 500 | Controls AMAF influence decay. Lower = trust real data sooner |
| `exploration_weight` | 1.414 | UCB exploration constant (sqrt(2)) |

## Research Question

> Does RAVE improve MCTS convergence in simultaneous-move games?

Run `python3 benchmark_rave.py` to compare RAVE vs standard MCTS at various simulation budgets.
