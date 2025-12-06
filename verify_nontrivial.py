"""
Quick verification that the game has non-trivial dynamics.
"""

from battle_v2 import BattleState, PlayerState, PokemonInstance, step, ActionType, legal_actions_for_player
from dex_v2 import DEX_V2
from main_v2 import GreedyAgent
import random

class AlwaysMove1:
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        legal = legal_actions_for_player(state, player_id)
        return ActionType.USE_MOVE_1 if ActionType.USE_MOVE_1 in legal else legal[0]

def run_game(agent1, agent2):
    t1 = [PokemonInstance.from_spec(DEX_V2[0]),
          PokemonInstance.from_spec(DEX_V2[2]),
          PokemonInstance.from_spec(DEX_V2[7])]
    t2 = [PokemonInstance.from_spec(DEX_V2[1]),
          PokemonInstance.from_spec(DEX_V2[4]),
          PokemonInstance.from_spec(DEX_V2[3])]
    
    state = BattleState(
        player1=PlayerState(team=t1, active_index=0),
        player2=PlayerState(team=t2, active_index=0),
        rng_seed=random.randint(0, 100000)
    )
    
    turns = 0
    while not state.terminal and turns < 100:
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        state = step(state, a1, a2)
        turns += 1
    
    return state.winner

def main():
    print("Verifying game is non-trivial...")
    print("Testing: Always-Move-1 vs Greedy")
    
    always1 = AlwaysMove1()
    greedy = GreedyAgent()
    
    wins = 0
    games = 20
    
    for i in range(games):
        winner = run_game(always1, greedy)
        if winner == 1:
            wins += 1
    
    wr = wins / games * 100
    
    print(f"\nResults: Always-Move-1 wins {wins}/{games} ({wr:.1f}%)")
    
    if wr < 30:
        print("\n✓ SUCCESS: Game is non-trivial!")
        print("  Trivial strategy loses to strategic play")
    else:
        print("\n⚠️  WARNING: Game may still have trivial dynamics")
    
    print(f"\nExpected MCTS performance:")
    print(f"  MCTS explores ~25 joint actions per node")
    print(f"  Should beat Greedy through deeper search")
    print(f"  No opponent modeling - fair competition")

if __name__ == "__main__":
    main()

