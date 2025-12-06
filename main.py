import sys
import random
from typing import List, Optional, Tuple
from battle import (
    PokemonSpec, MoveSpec, PokemonInstance, PlayerState, BattleState,
    ActionType, step, legal_actions_for_player, calculate_damage
)
import battle
from mcts import MCTSAgent

# --- Dex Definition ---

DEX = [
    PokemonSpec(
        name="Flameling",
        type="Fire",
        max_hp=60,
        attack=18,
        defense=10,
        speed=14,
        moves=[
            MoveSpec(name="Ember", type="Fire", base_power=16),
            MoveSpec(name="Quick Jab", type="Normal", base_power=10),
        ],
    ),
    PokemonSpec(
        name="Aquaff",
        type="Water",
        max_hp=65,
        attack=16,
        defense=12,
        speed=12,
        moves=[
            MoveSpec(name="Splash Shot", type="Water", base_power=16),
            MoveSpec(name="Body Slam", type="Normal", base_power=12),
        ],
    ),
    PokemonSpec(
        name="Leaflet",
        type="Grass",
        max_hp=55,
        attack=17,
        defense=11,
        speed=13,
        moves=[
            MoveSpec(name="Vine Whip", type="Grass", base_power=16),
            MoveSpec(name="Tackle", type="Normal", base_power=11),
        ],
    ),
    PokemonSpec(
        name="Bulkwall",
        type="Normal",
        max_hp=80,
        attack=14,
        defense=16,
        speed=8,
        moves=[
            MoveSpec(name="Heavy Slam", type="Normal", base_power=18),
            MoveSpec(name="Guard Strike", type="Normal", base_power=12),
        ],
    ),
    PokemonSpec(
        name="Sparkit",
        type="Fire",
        max_hp=50,
        attack=19,
        defense=9,
        speed=16,
        moves=[
            MoveSpec(name="Flame Dash", type="Fire", base_power=18),
            MoveSpec(name="Scratch", type="Normal", base_power=10),
        ],
    ),
    PokemonSpec(
        name="Torrento",
        type="Water",
        max_hp=70,
        attack=15,
        defense=14,
        speed=10,
        moves=[
            MoveSpec(name="Water Jet", type="Water", base_power=17),
            MoveSpec(name="Headbutt", type="Normal", base_power=13),
        ],
    ),
    PokemonSpec(
        name="Sprouty",
        type="Grass",
        max_hp=58,
        attack=16,
        defense=12,
        speed=15,
        moves=[
            MoveSpec(name="Leaf Slice", type="Grass", base_power=17),
            MoveSpec(name="Bash", type="Normal", base_power=12),
        ],
    ),
    PokemonSpec(
        name="Stonecub",
        type="Normal",
        max_hp=75,
        attack=15,
        defense=15,
        speed=9,
        moves=[
            MoveSpec(name="Rock Punch", type="Normal", base_power=17),
            MoveSpec(name="Steady Blow", type="Normal", base_power=13),
        ],
    ),
]

# --- Agents ---

class Agent:
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        raise NotImplementedError

class RandomAgent(Agent):
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        actions = legal_actions_for_player(state, player_id)
        return random.choice(actions)

class GreedyAgent(Agent):
    """
    A baseline greedy agent that:
    - If attacking: picks the move with highest immediate damage.
    - If must switch: picks a random valid switch (simple baseline).
    - If can switch but doesn't have to: rarely switches (only if random factor? No, deterministic for now).
      For this simple version, it always attacks if possible, unless it's a sophisticated greedy.
      Let's implement: Always attack if possible with max damage move. If must switch, pick random.
    """
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        legal = legal_actions_for_player(state, player_id)
        
        # Separate attacks and switches
        attacks = [a for a in legal if a in (ActionType.USE_MOVE_1, ActionType.USE_MOVE_2)]
        switches = [a for a in legal if a not in attacks]
        
        if not attacks:
            # Must switch
            return random.choice(switches)
            
        # If can attack, evaluate damage
        # We need to know who the opponent active pokemon is
        my_state = state.player1 if player_id == 1 else state.player2
        opp_state = state.player2 if player_id == 1 else state.player1
        
        my_active = my_state.team[my_state.active_index]
        opp_active = opp_state.team[opp_state.active_index]
        
        best_action = None
        max_damage = -1
        
        for action in attacks:
            move_idx = 0 if action == ActionType.USE_MOVE_1 else 1
            move = my_active.spec.moves[move_idx]
            # Calculate damage against current opponent active
            dmg = calculate_damage(move, my_active, opp_active)
            if dmg > max_damage:
                max_damage = dmg
                best_action = action
                
        return best_action

class HumanAgent(Agent):
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        actions = legal_actions_for_player(state, player_id)
        
        print(f"\nPlayer {player_id}, choose your action:")
        
        # Display options
        opts = {}
        
        p_state = state.player1 if player_id == 1 else state.player2
        active_mon = p_state.team[p_state.active_index]
        
        attack_options = []
        switch_options = []
        
        for act in actions:
            if act == ActionType.USE_MOVE_1:
                attack_options.append((act, active_mon.spec.moves[0].name))
            elif act == ActionType.USE_MOVE_2:
                attack_options.append((act, active_mon.spec.moves[1].name))
            elif act in (ActionType.SWITCH_TO_0, ActionType.SWITCH_TO_1, ActionType.SWITCH_TO_2):
                idx = 0
                if act == ActionType.SWITCH_TO_1: idx = 1
                if act == ActionType.SWITCH_TO_2: idx = 2
                mon_name = p_state.team[idx].spec.name
                switch_options.append((act, mon_name))

        idx_counter = 1
        
        if attack_options:
            print("  Attacks:")
            for act, name in attack_options:
                print(f"    {idx_counter}. {name}")
                opts[idx_counter] = act
                idx_counter += 1
                
        if switch_options:
            print("  Switches:")
            for act, name in switch_options:
                print(f"    {idx_counter}. Switch to {name}")
                opts[idx_counter] = act
                idx_counter += 1
        
        while True:
            try:
                choice = input("Enter choice number: ")
                c = int(choice)
                if c in opts:
                    return opts[c]
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a number.")


# --- Helper Functions ---

def create_teams() -> Tuple[List[PokemonInstance], List[PokemonInstance]]:
    # Fixed teams for now as per spec
    # Team 1: Flameling, Leaflet, Stonecub
    t1_specs = [DEX[0], DEX[2], DEX[7]]
    # Team 2: Aquaff, Sparkit, Bulkwall
    t2_specs = [DEX[1], DEX[4], DEX[3]]
    
    team1 = [PokemonInstance.from_spec(s) for s in t1_specs]
    team2 = [PokemonInstance.from_spec(s) for s in t2_specs]
    return team1, team2

def print_battle_state(state: BattleState):
    print(f"\n--- Turn {state.turn_number} ---")
    
    def print_player(p_state: PlayerState, label: str):
        active = p_state.team[p_state.active_index]
        print(f"{label}:")
        print(f"  Active: {active.spec.name} ({active.current_hp}/{active.spec.max_hp} HP) {active.spec.type}")
        bench = []
        for i, mon in enumerate(p_state.team):
            if i != p_state.active_index:
                status = "Fainted" if mon.fainted else f"{mon.current_hp}/{mon.spec.max_hp} HP"
                bench.append(f"{mon.spec.name} ({status})")
        print(f"  Bench: {', '.join(bench)}")

    print_player(state.player1, "Player 1")
    print_player(state.player2, "Player 2")

def main():
    print("Mini Pokemon Battle Simulator")
    print("-----------------------------")
    
    t1, t2 = create_teams()
    p1_state = PlayerState(team=t1, active_index=0)
    p2_state = PlayerState(team=t2, active_index=0)
    
    state = BattleState(player1=p1_state, player2=p2_state)
    
    # Setup Agents
    # Mode selection
    print("Select Mode:")
    print("1. Human vs Human")
    print("2. Human vs Random")
    print("3. Random vs Random")
    print("4. Greedy vs Random")
    print("5. Greedy vs Greedy")
    print("6. MCTS vs Random")
    print("7. MCTS vs Greedy")
    print("8. Human vs MCTS")
    
    mode = input("Enter mode: ").strip()
    
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
        
    # Game Loop
    while not state.terminal:
        print_battle_state(state)
        
        # Get actions
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        
        print(f"\nP1 chose {a1}")
        print(f"P2 chose {a2}")
        
        state = step(state, a1, a2)
        
    print_battle_state(state)
    print(f"\nGame Over! Winner: Player {state.winner}")
    if state.winner is None:
        print("It's a draw!")

if __name__ == "__main__":
    main()
