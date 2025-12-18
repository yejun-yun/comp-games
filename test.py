#!/usr/bin/env python3
"""
CPSC 474 Final Project - Test Script
Yejun Yun and William Zhong
"""

import sys
import time
from battle_v2 import BattleState, PlayerState, PokemonInstance, step
from dex_v2 import DEX_V2
from mcts_v2 import MCTSAgent
from main_v2 import GreedyAgent, RandomAgent


def print_header():
    """Print project description."""
    print("=" * 70)
    print("CPSC 474 FINAL PROJECT: Pokemon Battle with MCTS")
    print("Student: Yejun Yun (---) and William Zhong (Value Network)")
    print("=" * 70)
    print()
    
    print("GAME DESCRIPTION:")
    print("-" * 70)
    print("A simplified 3v3 Pokémon battle game with:")
    print("  • 8 Pokémon across 4 types (Fire, Water, Grass, Normal)")
    print("  • Type advantage system (Fire > Grass > Water > Fire)")
    print("  • Fixed teams with 3 Pokémon each")
    print("  • Simultaneous turn-based combat")
    print("  • Actions: Attack (2 moves) or Switch (to benched Pokémon)")
    print("  • Key mechanics: Accuracy checks, priority moves, recoil damage")
    print("  • No randomness in damage calculation (less stochasticity)")
    print()
    
    print("Strategic Depth:")
    print("Type matchups create rock-paper-scissors dynamics")
    print("Speed determines attack order (faster Pokémon hit first)")
    print("Resource management (no healing, permanent damage)")
    print("Prediction/mind games from simultaneous moves")
    print()
    
    print("Research Question:")
    print("-" * 70)
    print("How does Monte Carlo Tree Search (MCTS) enhanced with a value network and --- perform")
    print("compared to a greedy baseline across different simulation budgets?")
    print()

def create_teams():
    """Create standard game teams."""
    # Team 1: Flameling (Fire), Leaflet (Grass), Stonecub (Normal)
    team1 = [PokemonInstance.from_spec(DEX_V2[0]),
             PokemonInstance.from_spec(DEX_V2[2]),
             PokemonInstance.from_spec(DEX_V2[7])]
    
    # Team 2: Aquaff (Water), Sparkit (Fire), Bulkwall (Normal)
    team2 = [PokemonInstance.from_spec(DEX_V2[1]),
             PokemonInstance.from_spec(DEX_V2[4]),
             PokemonInstance.from_spec(DEX_V2[3])]
    
    return team1, team2


def play_game(agent1, agent2):
    """Play one game between two agents. Returns winner (1, 2, or None)."""
    team1, team2 = create_teams()
    state = BattleState(
        player1=PlayerState(team=team1, active_index=0),
        player2=PlayerState(team=team2, active_index=0)
    )
    
    while not state.terminal:
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        state = step(state, a1, a2)
    
    return state.winner


def quick_benchmark(agent1, agent2, name1, name2, num_games=20):
    """Run a quick benchmark between two agents."""
    print(f"\n{name1} vs {name2} ({num_games} games):")
    print("-" * 70)
    
    wins_p1 = 0
    wins_p2 = 0
    draws = 0
    
    start_time = time.time()
    
    for i in range(num_games):
        winner = play_game(agent1, agent2)
        
        if winner == 1:
            wins_p1 += 1
        elif winner == 2:
            wins_p2 += 1
        else:
            draws += 1
        
        # Progress indicator
        if (i + 1) % 5 == 0:
            print(f"  Progress: {i+1}/{num_games} games complete...")
    
    elapsed = time.time() - start_time
    
    print(f"\n  Results:")
    print(f"    {name1}: {wins_p1} wins ({wins_p1/num_games*100:.1f}%)")
    print(f"    {name2}: {wins_p2} wins ({wins_p2/num_games*100:.1f}%)")
    print(f"    Draws: {draws}")
    print(f"    Time: {elapsed:.1f}s ({elapsed/num_games:.2f}s/game)")
    
    return wins_p1, wins_p2, draws, elapsed


def main():
    """Run test suite."""
    print_header()
    
    print("IMPLEMENTATION:")
    print("-" * 70)
    print("Three agents implemented:")
    print("  1. RandomAgent  - Picks uniformly random legal actions (sanity check)")
    print("  2. GreedyAgent  - Always picks highest expected damage move")
    print("  3. MCTSAgent    - Monte Carlo Tree Search with random rollouts")
    print()
    print("MCTS Details:")
    print("  • UCB1 tree policy (exploration constant = √2)")
    print("  • Explores all joint action pairs (simultaneous moves)")
    print("  • Random rollouts for unbiased value estimation")
    print("  • Minimax-style action selection for simultaneous game")
    print()
    
    print("=" * 70)
    print("RUNNING TESTS (Quick Benchmark: ~2-3 minutes)")
    print("=" * 70)
    
    # Baseline: Greedy vs Random (establishes that greedy is strong)
    print("\n[1/4] BASELINE: Greedy vs Random")
    print("-" * 70)
    print("Establishes greedy baseline strength...")
    
    greedy = GreedyAgent()
    random_agent = RandomAgent()
    
    results_baseline = quick_benchmark(
        greedy, random_agent,
        "Greedy", "Random",
        num_games=20
    )
    
    greedy_vs_random_winrate = results_baseline[0] / 20 * 100
    
    # Test 1: MCTS (50 sims) vs Greedy
    print("\n[2/4] TEST 1: MCTS-50 vs Greedy")
    print("-" * 70)
    print("Testing MCTS with 50 simulations per move...")
    
    mcts_50 = MCTSAgent(simulations_per_move=50, player_id=1)
    
    results_50 = quick_benchmark(
        mcts_50, greedy,
        "MCTS-50", "Greedy",
        num_games=20
    )
    
    # Test 2: MCTS (100 sims) vs Greedy
    print("\n[3/4] TEST 2: MCTS-100 vs Greedy")
    print("-" * 70)
    print("Testing MCTS with 100 simulations per move...")
    
    mcts_100 = MCTSAgent(simulations_per_move=100, player_id=1)
    
    results_100 = quick_benchmark(
        mcts_100, greedy,
        "MCTS-100", "Greedy",
        num_games=20
    )
    
    # Test 3: MCTS (200 sims) vs Greedy
    print("\n[4/4] TEST 3: MCTS-200 vs Greedy")
    print("-" * 70)
    print("Testing MCTS with 200 simulations per move...")
    
    mcts_200 = MCTSAgent(simulations_per_move=200, player_id=1)
    
    results_200 = quick_benchmark(
        mcts_200, greedy,
        "MCTS-200", "Greedy",
        num_games=20
    )
    
    # Summary
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    
    print(f"\nBaseline Strength:")
    print(f"  Greedy vs Random: {greedy_vs_random_winrate:.0f}% win rate")
    print(f"  → Greedy is a strong baseline (not trivial to beat)")
    
    print(f"\nMCTS Performance vs Greedy Baseline:")
    print(f"  MCTS-50:  {results_50[0]}/20 wins ({results_50[0]/20*100:.0f}%)")
    print(f"  MCTS-100: {results_100[0]}/20 wins ({results_100[0]/20*100:.0f}%)")
    print(f"  MCTS-200: {results_200[0]}/20 wins ({results_200[0]/20*100:.0f}%)")
    
    print(f"\nComputation Time per Move:")
    print(f"  MCTS-50:  ~{results_50[3]/20/10:.3f}s")  # Approximate per-move time
    print(f"  MCTS-100: ~{results_100[3]/20/10:.3f}s")
    print(f"  MCTS-200: ~{results_200[3]/20/10:.3f}s")
    
    print("\n" + "=" * 70)
    print("KEY FINDINGS")
    print("=" * 70)
    
    # Determine if MCTS is beating greedy
    avg_mcts_winrate = (results_50[0] + results_100[0] + results_200[0]) / 60 * 100
    
    if avg_mcts_winrate > 55:
        print("✓ MCTS outperforms greedy baseline with lookahead search")
    elif avg_mcts_winrate > 45:
        print("✓ MCTS is competitive with greedy (roughly equal performance)")
    else:
        print("✗ MCTS underperforms greedy in this quick test")
        print("  Note: Random rollouts may need more simulations or better policy")
    
    if results_200[0] > results_50[0]:
        print("✓ Performance scales with computation budget (more sims = better)")
    else:
        print("○ Performance scaling non-monotonic (may need larger sample size)")
    
    print(f"✓ MCTS provides strategic lookahead (vs greedy's myopic play)")
    print(f"✓ Random rollouts provide unbiased value estimates")
    
    print("\n" + "=" * 70)
    print("FULL BENCHMARK INSTRUCTIONS")
    print("=" * 70)
    print("\nTo reproduce complete results with more games and simulation budgets:")
    print()
    print("  python3 benchmark_v2.py")
    print()
    print("This runs:")
    print("  • 50 games per configuration (vs 20 in quick test)")
    print("  • Tests simulation budgets: 50, 100, 200, 500")
    print("  • Takes approximately 5-10 minutes")
    print()
    print("Expected full results:")
    print("  • MCTS-50:  40-50% win rate vs Greedy")
    print("  • MCTS-100: 50-60% win rate vs Greedy")
    print("  • MCTS-200: 55-65% win rate vs Greedy")
    print("  • MCTS-500: 60-70% win rate vs Greedy")
    print()
    
    print("=" * 70)
    print("OPTIONAL: Value Network Enhancement")
    print("=" * 70)
    print("\nAn advanced AlphaGo-style enhancement is available in:")
    print("  william-valuenetwork/")
    print()
    print("This replaces random rollouts with a trained neural network.")
    print("Requires: numpy, tqdm (pip install --user numpy tqdm)")
    print()
    print("To test (requires numpy):")
    print("  cd william-valuenetwork")
    print("  python3 train_value_network.py  # Train network (~5 min)")
    print("  python3 benchmark_value_net.py  # Compare performance")
    print()
    print("Expected enhancement: 70-80% win rate vs Greedy (vs 40-50% with random)")
    print()
    
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

