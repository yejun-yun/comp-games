"""
Battle Engine V2: With Accuracy, Priority, and Recoil

Adds strategic depth to prevent trivial "always attack" strategies.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto
import math
import copy
import random

# --- Enums and Constants ---

class ActionType(Enum):
    USE_MOVE_1 = auto()
    USE_MOVE_2 = auto()
    SWITCH_TO_0 = auto()
    SWITCH_TO_1 = auto()
    SWITCH_TO_2 = auto()

TYPE_CHART = {
    "Fire": {"Grass": 2.0, "Water": 0.5, "Fire": 1.0, "Normal": 1.0},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Water": 1.0, "Normal": 1.0},
    "Grass": {"Water": 2.0, "Fire": 0.5, "Grass": 1.0, "Normal": 1.0},
    "Normal": {"Fire": 1.0, "Water": 1.0, "Grass": 1.0, "Normal": 1.0},
}

# --- Data Classes ---

@dataclass
class MoveSpec:
    name: str
    type: str
    base_power: int
    accuracy: int = 100        # 0-100 (percentage)
    priority: int = 0          # -5 to +5 (higher goes first)
    recoil_percent: int = 0    # 0-100 (% of damage dealt taken as recoil)

@dataclass
class PokemonSpec:
    name: str
    type: str
    max_hp: int
    attack: int
    defense: int
    speed: int
    moves: List[MoveSpec]

@dataclass
class PokemonInstance:
    spec: PokemonSpec
    current_hp: int
    fainted: bool = False

    @classmethod
    def from_spec(cls, spec: PokemonSpec) -> 'PokemonInstance':
        return cls(spec=spec, current_hp=spec.max_hp, fainted=False)

@dataclass
class PlayerState:
    team: List[PokemonInstance]
    active_index: int

@dataclass
class BattleState:
    player1: PlayerState
    player2: PlayerState
    terminal: bool = False
    winner: Optional[int] = None
    turn_number: int = 0
    rng_seed: int = 42  # For reproducibility

    def clone(self) -> 'BattleState':
        return copy.deepcopy(self)

# --- Core Logic Functions ---

def get_type_multiplier(attacker_type: str, defender_type: str) -> float:
    return TYPE_CHART.get(attacker_type, {}).get(defender_type, 1.0)

def calculate_damage(move: MoveSpec, attacker: PokemonInstance, defender: PokemonInstance) -> int:
    """Calculate damage (before accuracy check)."""
    multiplier = get_type_multiplier(move.type, defender.spec.type)
    defense = max(defender.spec.defense, 1)
    raw_damage = move.base_power * (attacker.spec.attack / defense) * multiplier
    damage = math.floor(raw_damage)
    return max(int(damage), 1)

def move_hits(move: MoveSpec, rng: random.Random) -> bool:
    """Check if move hits based on accuracy."""
    if move.accuracy >= 100:
        return True
    roll = rng.randint(1, 100)
    return roll <= move.accuracy

def legal_actions_for_player(state: BattleState, player_id: int) -> List[ActionType]:
    """Returns the list of legal actions for the given player."""
    if state.terminal:
        return []

    player_state = state.player1 if player_id == 1 else state.player2
    active_mon = player_state.team[player_state.active_index]
    
    actions = []
    
    if active_mon.fainted:
        for i, mon in enumerate(player_state.team):
            if not mon.fainted and i != player_state.active_index:
                if i == 0: actions.append(ActionType.SWITCH_TO_0)
                elif i == 1: actions.append(ActionType.SWITCH_TO_1)
                elif i == 2: actions.append(ActionType.SWITCH_TO_2)
        return actions

    actions.append(ActionType.USE_MOVE_1)
    actions.append(ActionType.USE_MOVE_2)
    
    for i, mon in enumerate(player_state.team):
        if not mon.fainted and i != player_state.active_index:
            if i == 0: actions.append(ActionType.SWITCH_TO_0)
            elif i == 1: actions.append(ActionType.SWITCH_TO_1)
            elif i == 2: actions.append(ActionType.SWITCH_TO_2)
            
    return actions

def is_switch_action(action: ActionType) -> bool:
    return action in (ActionType.SWITCH_TO_0, ActionType.SWITCH_TO_1, ActionType.SWITCH_TO_2)

def get_switch_index(action: ActionType) -> int:
    if action == ActionType.SWITCH_TO_0: return 0
    if action == ActionType.SWITCH_TO_1: return 1
    if action == ActionType.SWITCH_TO_2: return 2
    raise ValueError("Not a switch action")

def apply_switch(player_state: PlayerState, action: ActionType):
    new_index = get_switch_index(action)
    player_state.active_index = new_index

def check_fainted(pokemon: PokemonInstance):
    if pokemon.current_hp <= 0:
        pokemon.current_hp = 0
        pokemon.fainted = True

def check_game_over(state: BattleState):
    p1_lost = all(p.fainted for p in state.player1.team)
    p2_lost = all(p.fainted for p in state.player2.team)
    
    if p1_lost and p2_lost:
        state.terminal = True
        state.winner = None
    elif p1_lost:
        state.terminal = True
        state.winner = 2
    elif p2_lost:
        state.terminal = True
        state.winner = 1

def step(state: BattleState, action_p1: ActionType, action_p2: ActionType) -> BattleState:
    """
    Returns a new BattleState after applying both actions.
    Now with accuracy, priority, and recoil mechanics!
    """
    next_state = state.clone()
    next_state.turn_number += 1
    
    # Initialize RNG for this turn (deterministic based on state)
    rng = random.Random(state.rng_seed + state.turn_number)
    
    p1 = next_state.player1
    p2 = next_state.player2
    
    # 1. Process Switches (always go first, before priority)
    p1_switching = is_switch_action(action_p1)
    p2_switching = is_switch_action(action_p2)
    
    if p1_switching:
        apply_switch(p1, action_p1)
    if p2_switching:
        apply_switch(p2, action_p2)
    
    # 2. Determine attack order (by PRIORITY, then SPEED)
    p1_attacking = not p1_switching
    p2_attacking = not p2_switching
    
    actions_to_execute = []
    
    if p1_attacking:
        move_idx = 0 if action_p1 == ActionType.USE_MOVE_1 else 1
        move = p1.team[p1.active_index].spec.moves[move_idx]
        actions_to_execute.append((1, action_p1, move.priority))
    
    if p2_attacking:
        move_idx = 0 if action_p2 == ActionType.USE_MOVE_1 else 1
        move = p2.team[p2.active_index].spec.moves[move_idx]
        actions_to_execute.append((2, action_p2, move.priority))
    
    # Sort by priority (higher first), then by speed, then by player ID
    def get_sort_key(action_tuple):
        player_id, action, priority = action_tuple
        p_state = p1 if player_id == 1 else p2
        speed = p_state.team[p_state.active_index].spec.speed
        return (-priority, -speed, player_id)  # Negative for descending
    
    actions_to_execute.sort(key=get_sort_key)
    
    # 3. Execute attacks in priority order
    for player_id, action, priority in actions_to_execute:
        attacker_state = p1 if player_id == 1 else p2
        defender_state = p2 if player_id == 1 else p1
        
        attacker = attacker_state.team[attacker_state.active_index]
        defender = defender_state.team[defender_state.active_index]
        
        # Can't attack if fainted
        if attacker.fainted:
            continue
        
        # Get move
        move_idx = 0 if action == ActionType.USE_MOVE_1 else 1
        move = attacker.spec.moves[move_idx]
        
        # Check accuracy
        if not move_hits(move, rng):
            # Miss! No damage dealt
            continue
        
        # Calculate and apply damage
        damage = calculate_damage(move, attacker, defender)
        defender.current_hp -= damage
        check_fainted(defender)
        
        # Apply recoil if any
        if move.recoil_percent > 0:
            recoil_damage = max(1, int(damage * move.recoil_percent / 100))
            attacker.current_hp -= recoil_damage
            check_fainted(attacker)
    
    # 4. Check game over
    check_game_over(next_state)
    
    return next_state

