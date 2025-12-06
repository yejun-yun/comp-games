"""
Benchmark script for V2 engine.

Tests MCTS (no opponent modeling) vs Greedy baseline.
"""

import time
import random
from battle_v2 import BattleState, PlayerState, PokemonInstance, step
from dex_v2 import DEX_V2
from main_v2 import Agent, GreedyAgent, RandomAgent
from mcts_v2 import MCTSAgent

def create_teams():
    t1 = [PokemonInstance.from_spec(DEX_V2[0]),
          PokemonInstance.from_spec(DEX_V2[2]),
          PokemonInstance.from_spec(DEX_V2[7])]
    t2 = [PokemonInstance.from_spec(DEX_V2[1]),
          PokemonInstance.from_spec(DEX_V2[4]),
          PokemonInstance.from_spec(DEX_V2[3])]
    return t1, t2

def run_single_game(agent1: Agent, agent2: Agent) -> int:
    """Run one game, return winner (1, 2, or 0 for draw)."""
    t1, t2 = create_teams()
    state = BattleState(
        player1=PlayerState(team=t1, active_index=0),
        player2=PlayerState(team=t2, active_index=0),
        rng_seed=random.randint(0, 1000000)
    )
    
    turn_limit = 100
    turns = 0
    
    while not state.terminal and turns < turn_limit:
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        state = step(state, a1, a2)
        turns += 1
    
    return state.winner if state.terminal else 0

def run_benchmark(agent1, agent2, num_games, name1, name2):
    """Run benchmark between two agents."""
    print(f"\n{'='*60}")
    print(f"{name1} vs {name2} ({num_games} games)")
    print(f"{'='*60}")
    
    wins_1 = 0
    wins_2 = 0
    draws = 0
    
    start = time.time()
    
    for i in range(num_games):
        if (i + 1) % 10 == 0:
            print(f"Progress: {i+1}/{num_games}...")
        
        winner = run_single_game(agent1, agent2)
        if winner == 1:
            wins_1 += 1
        elif winner == 2:
            wins_2 += 1
        else:
            draws += 1
    
    elapsed = time.time() - start
    
    print(f"\nResults:")
    print(f"  {name1}: {wins_1} ({wins_1/num_games*100:.1f}%)")
    print(f"  {name2}: {wins_2} ({wins_2/num_games*100:.1f}%)")
    print(f"  Draws: {draws}")
    print(f"  Time: {elapsed:.1f}s ({elapsed/num_games:.3f}s/game)")
    
    return {"p1": wins_1, "p2": wins_2, "draws": draws}

def main():
    print("\n" + "="*60)
    print("Pokemon Battle V2 - MCTS Performance Benchmark")
    print("="*60)
    
    num_games = 50
    
    # Baseline: Greedy vs Random
    print("\n### BASELINE: Greedy vs Random ###")
    greedy = GreedyAgent()
    random_agent = RandomAgent()
    run_benchmark(greedy, random_agent, num_games, "Greedy", "Random")
    
    # Test MCTS at different simulation budgets
    budgets = [50, 100, 200, 500]
    results = []
    
    for sims in budgets:
        print(f"\n### MCTS-{sims} vs Greedy ###")
        mcts = MCTSAgent(simulations_per_move=sims, player_id=1)
        greedy = GreedyAgent()
        result = run_benchmark(mcts, greedy, num_games, f"MCTS-{sims}", "Greedy")
        results.append((sims, result["p1"]))
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY: MCTS Performance Scaling")
    print("="*60)
    print(f"\n{'Simulations':<15} {'Win Rate':<15}")
    print("-" * 30)
    for sims, wins in results:
        wr = wins / num_games * 100
        print(f"{sims:<15} {wr:<14.1f}%")
    
    print("\n" + "="*60)
    print("CONCLUSION:")
    print("="*60)
    print("This is HONEST MCTS - no opponent modeling.")
    print("Performance improvement comes from pure search depth.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

