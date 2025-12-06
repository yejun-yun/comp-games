"""
CPSC 474 Final Project: Mini Pokémon Battle Simulator Engine

This module implements the core game logic, data structures, and rules for a simplified
Pokémon-style battle game. It is designed to be deterministic and easy for AI agents to use.

Key components:
- Data Classes: PokemonSpec, PokemonInstance, PlayerState, BattleState
- Logic: step(), legal_actions_for_player(), calculate_damage()
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from enum import Enum, auto
import math
import copy

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
    type: str        # "Fire", "Water", "Grass", "Normal"
    base_power: int

@dataclass
class PokemonSpec:
    name: str
    type: str        # "Fire", "Water", "Grass", "Normal"
    max_hp: int
    attack: int
    defense: int
    speed: int
    moves: List[MoveSpec]   # exactly 2 moves

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
    team: List[PokemonInstance]   # length 3
    active_index: int             # 0, 1, or 2

@dataclass
class BattleState:
    player1: PlayerState
    player2: PlayerState
    terminal: bool = False     # True if game over
    winner: Optional[int] = None   # 1, 2, or None
    turn_number: int = 0

    def clone(self) -> 'BattleState':
        return copy.deepcopy(self)

# --- Core Logic Functions ---

def get_type_multiplier(attacker_type: str, defender_type: str) -> float:
    return TYPE_CHART.get(attacker_type, {}).get(defender_type, 1.0)

def calculate_damage(move: MoveSpec, attacker: PokemonInstance, defender: PokemonInstance) -> int:
    # damage = floor(base_power * (attack / defense) * type_multiplier)
    # damage = max(damage, 1)
    
    multiplier = get_type_multiplier(move.type, defender.spec.type)
    # Avoid division by zero just in case, though specs say small integers (likely > 0)
    defense = max(defender.spec.defense, 1)
    
    raw_damage = move.base_power * (attacker.spec.attack / defense) * multiplier
    damage = math.floor(raw_damage)
    return max(int(damage), 1)

def legal_actions_for_player(state: BattleState, player_id: int) -> List[ActionType]:
    """
    Returns the list of legal actions for the given player.
    """
    if state.terminal:
        return []

    player_state = state.player1 if player_id == 1 else state.player2
    active_mon = player_state.team[player_state.active_index]
    
    actions = []
    
    # If active pokemon is fainted, MUST switch
    if active_mon.fainted:
        # Can only switch to non-fainted pokemon
        for i, mon in enumerate(player_state.team):
            if not mon.fainted and i != player_state.active_index:
                if i == 0: actions.append(ActionType.SWITCH_TO_0)
                elif i == 1: actions.append(ActionType.SWITCH_TO_1)
                elif i == 2: actions.append(ActionType.SWITCH_TO_2)
        return actions

    # If active pokemon is NOT fainted, can attack or switch
    
    # Attacks
    actions.append(ActionType.USE_MOVE_1)
    actions.append(ActionType.USE_MOVE_2)
    
    # Switches
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
    # Validate (though step assumes valid actions passed in context of engine)
    if player_state.team[new_index].fainted:
        # Fallback or error? Requirements say "provided that Pokémon is not fainted"
        # We assume the agent/CLI filtered legal moves. 
        # But for robustness, we might check. Let's trust legal_actions for now
        # or fail hard if invalid.
        pass
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
        state.winner = None # Draw
    elif p1_lost:
        state.terminal = True
        state.winner = 2
    elif p2_lost:
        state.terminal = True
        state.winner = 1

def step(state: BattleState, action_p1: ActionType, action_p2: ActionType) -> BattleState:
    """
    Returns a new BattleState after applying both actions.
    """
    next_state = state.clone()
    next_state.turn_number += 1
    
    p1 = next_state.player1
    p2 = next_state.player2
    
    # 1. Process Switches
    p1_switching = is_switch_action(action_p1)
    p2_switching = is_switch_action(action_p2)
    
    if p1_switching:
        apply_switch(p1, action_p1)
    if p2_switching:
        apply_switch(p2, action_p2)
        
    # If a player was forced to switch because of faint, they don't get to attack *after* the switch 
    # in the same turn usually in Pokemon. 
    # BUT: Requirements say: "If a player’s active Pokémon is fainted at the start of a turn: They must choose a switch action. Attack actions are not legal."
    # And "If one player switched and the other attacked: Switch happens first. Then the attack hits the new active Pokémon."
    # This implies the switcher consumes their turn switching.
    
    # 2. Process Attacks
    # Only if the player didn't switch AND their active mon is alive (it should be if they chose attack)
    # Note: If they were forced to switch, they are switching. 
    
    # Determine execution order for attacks
    # If both attack, check speed
    p1_attacking = not p1_switching
    p2_attacking = not p2_switching
    
    first_attacker = None
    second_attacker = None
    first_action = None
    second_action = None
    first_target = None
    second_target = None
    
    # Identify if attacks happen
    if p1_attacking and p2_attacking:
        s1 = p1.team[p1.active_index].spec.speed
        s2 = p2.team[p2.active_index].spec.speed
        
        if s1 > s2:
            first_attacker, first_action, first_target = p1, action_p1, p2
            second_attacker, second_action, second_target = p2, action_p2, p1
        elif s2 > s1:
            first_attacker, first_action, first_target = p2, action_p2, p1
            second_attacker, second_action, second_target = p1, action_p1, p2
        else:
            # Tie break: Player 1 attacks first
            first_attacker, first_action, first_target = p1, action_p1, p2
            second_attacker, second_action, second_target = p2, action_p2, p1
            
    elif p1_attacking and not p2_attacking:
        first_attacker, first_action, first_target = p1, action_p1, p2
    elif p2_attacking and not p1_attacking:
        first_attacker, first_action, first_target = p2, action_p2, p1
        
    # Execute First Attack
    if first_attacker:
        active_mon = first_attacker.team[first_attacker.active_index]
        target_mon = first_target.team[first_target.active_index]
        
        # Ensure attacker is alive (could be dead if mechanics allowed other things, but here simultaneous)
        # Actually, standard Pokemon: if p1 attacks and p2 attacks, and p1 kills p2, p2 does not attack.
        # Requirements: "If a Pokémon’s HP reaches 0: Mark it as fainted."
        # Implicit: Fainted pokemon cannot attack.
        
        if not active_mon.fainted:
            move_idx = 0 if first_action == ActionType.USE_MOVE_1 else 1
            move = active_mon.spec.moves[move_idx]
            dmg = calculate_damage(move, active_mon, target_mon)
            target_mon.current_hp -= dmg
            check_fainted(target_mon)
            
    # Execute Second Attack
    if second_attacker:
        active_mon = second_attacker.team[second_attacker.active_index]
        target_mon = second_target.team[second_target.active_index]
        
        # Key check: Is the attacker still alive?
        if not active_mon.fainted:
            move_idx = 0 if second_action == ActionType.USE_MOVE_1 else 1
            move = active_mon.spec.moves[move_idx]
            dmg = calculate_damage(move, active_mon, target_mon)
            target_mon.current_hp -= dmg
            check_fainted(target_mon)

    # 3. Check Game Over
    check_game_over(next_state)
    
    return next_state
