"""
Mini Pokemon Battle Simulator V2

Clean version with:
- Accuracy, priority, recoil mechanics
- General MCTS (no opponent modeling)
- Strategic depth
"""

import sys
import random
from typing import List, Tuple
from battle_v2 import (
    BattleState, PlayerState, PokemonInstance, ActionType,
    step, legal_actions_for_player, calculate_damage
)
from dex_v2 import DEX_V2
from mcts_v2 import MCTSAgent

# --- Agents ---

class Agent:
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        raise NotImplementedError

class RandomAgent(Agent):
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        actions = legal_actions_for_player(state, player_id)
        return random.choice(actions)

class GreedyAgent(Agent):
    """Greedy agent that maximizes expected damage."""
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        legal = legal_actions_for_player(state, player_id)
        attacks = [a for a in legal if a in (ActionType.USE_MOVE_1, ActionType.USE_MOVE_2)]
        switches = [a for a in legal if a not in attacks]
        
        if not attacks:
            return random.choice(switches) if switches else legal[0]
        
        my_state = state.player1 if player_id == 1 else state.player2
        opp_state = state.player2 if player_id == 1 else state.player1
        my_active = my_state.team[my_state.active_index]
        opp_active = opp_state.team[opp_state.active_index]
        
        best_action = None
        max_expected = -1
        
        for action in attacks:
            move_idx = 0 if action == ActionType.USE_MOVE_1 else 1
            move = my_active.spec.moves[move_idx]
            base_dmg = calculate_damage(move, my_active, opp_active)
            
            # Expected value = damage * accuracy - recoil penalty
            expected = base_dmg * (move.accuracy / 100)
            if move.recoil_percent > 0:
                expected -= base_dmg * (move.recoil_percent / 100) * 0.5
            
            if expected > max_expected:
                max_expected = expected
                best_action = action
        
        return best_action if best_action else legal[0]

class HumanAgent(Agent):
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        actions = legal_actions_for_player(state, player_id)
        
        print(f"\nPlayer {player_id}, choose your action:")
        
        p_state = state.player1 if player_id == 1 else state.player2
        active_mon = p_state.team[p_state.active_index]
        
        opts = {}
        idx = 1
        
        # Show attacks with details
        for act in actions:
            if act == ActionType.USE_MOVE_1:
                move = active_mon.spec.moves[0]
                print(f"  {idx}. {move.name} (Pwr:{move.base_power} Acc:{move.accuracy}% Pri:{move.priority:+d}" +
                      (f" Recoil:{move.recoil_percent}%)" if move.recoil_percent > 0 else ")"))
                opts[idx] = act
                idx += 1
            elif act == ActionType.USE_MOVE_2:
                move = active_mon.spec.moves[1]
                print(f"  {idx}. {move.name} (Pwr:{move.base_power} Acc:{move.accuracy}% Pri:{move.priority:+d}" +
                      (f" Recoil:{move.recoil_percent}%)" if move.recoil_percent > 0 else ")"))
                opts[idx] = act
                idx += 1
        
        # Show switches
        for act in actions:
            if act in (ActionType.SWITCH_TO_0, ActionType.SWITCH_TO_1, ActionType.SWITCH_TO_2):
                switch_idx = 0 if act == ActionType.SWITCH_TO_0 else (1 if act == ActionType.SWITCH_TO_1 else 2)
                mon = p_state.team[switch_idx]
                print(f"  {idx}. Switch to {mon.spec.name} ({mon.current_hp}/{mon.spec.max_hp} HP)")
                opts[idx] = act
                idx += 1
        
        while True:
            try:
                choice = int(input("Choice: "))
                if choice in opts:
                    return opts[choice]
                print("Invalid choice.")
            except ValueError:
                print("Enter a number.")

# --- Helper Functions ---

def create_teams() -> Tuple[List[PokemonInstance], List[PokemonInstance]]:
    """Create balanced teams from DEX_V2."""
    # Team 1: Flameling, Leaflet, Stonecub
    t1 = [PokemonInstance.from_spec(DEX_V2[0]),
          PokemonInstance.from_spec(DEX_V2[2]),
          PokemonInstance.from_spec(DEX_V2[7])]
    
    # Team 2: Aquaff, Sparkit, Bulkwall
    t2 = [PokemonInstance.from_spec(DEX_V2[1]),
          PokemonInstance.from_spec(DEX_V2[4]),
          PokemonInstance.from_spec(DEX_V2[3])]
    
    return t1, t2

def print_battle_state(state: BattleState):
    print(f"\n--- Turn {state.turn_number} ---")
    
    for pid in [1, 2]:
        p = state.player1 if pid == 1 else state.player2
        active = p.team[p.active_index]
        print(f"Player {pid}: {active.spec.name} ({active.current_hp}/{active.spec.max_hp} HP)")
        bench = [f"{m.spec.name}({m.current_hp}/{m.spec.max_hp})" if not m.fainted 
                 else f"{m.spec.name}(X)" for i, m in enumerate(p.team) if i != p.active_index]
        print(f"  Bench: {', '.join(bench)}")

def main():
    print("Mini Pokemon Battle V2 (with Accuracy/Priority/Recoil)")
    print("="*60)
    
    t1, t2 = create_teams()
    state = BattleState(
        player1=PlayerState(team=t1, active_index=0),
        player2=PlayerState(team=t2, active_index=0),
        rng_seed=random.randint(0, 100000)
    )
    
    print("Mode:")
    print("1. Human vs Human")
    print("2. Human vs Random")
    print("3. Random vs Random")
    print("4. Greedy vs Random")
    print("5. Greedy vs Greedy")
    print("6. MCTS vs Random")
    print("7. MCTS vs Greedy")
    print("8. Human vs MCTS")
    
    mode = input("Select: ").strip()
    
    agent1 = HumanAgent()
    agent2 = HumanAgent()
    
    if mode == '2':
        agent2 = RandomAgent()
    elif mode == '3':
        agent1 = RandomAgent()
        agent2 = RandomAgent()
    elif mode == '4':
        agent1 = GreedyAgent()
        agent2 = RandomAgent()
    elif mode == '5':
        agent1 = GreedyAgent()
        agent2 = GreedyAgent()
    elif mode == '6':
        agent1 = MCTSAgent(simulations_per_move=100, player_id=1)
        agent2 = RandomAgent()
    elif mode == '7':
        agent1 = MCTSAgent(simulations_per_move=100, player_id=1)
        agent2 = GreedyAgent()
    elif mode == '8':
        agent2 = MCTSAgent(simulations_per_move=100, player_id=2)
    
    # Game loop
    while not state.terminal:
        print_battle_state(state)
        
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        
        print(f"\nP1: {a1}, P2: {a2}")
        state = step(state, a1, a2)
    
    print_battle_state(state)
    print(f"\nWinner: Player {state.winner if state.winner else 'Draw'}")

if __name__ == "__main__":
    main()


