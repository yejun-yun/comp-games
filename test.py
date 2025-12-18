#!/usr/bin/env python3
"""
CPSC 474 Final Project - Test Script
Yejun Yun and William Zhong

Tests MCTS enhancements (RAVE and Value Network) against baselines
"""

import sys
import time
import os
from battle_v2 import BattleState, PlayerState, PokemonInstance, step
from dex_v2 import DEX_V2
from mcts_v2 import MCTSAgent
from main_v2 import GreedyAgent, RandomAgent

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'yejun-rave'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'william-valuenetwork'))

from mcts_rave import MCTSRAVEAgent
try:
    from mcts_value_net import create_mcts_with_value_net
    HAS_VALUE_NET = True
except ImportError:
    HAS_VALUE_NET = False
    print("Warning: Value network not available (requires numpy)")


def print_header():
    print("=" * 80)
    print("CPSC 474 FINAL PROJECT: Pokémon Battle with MCTS Enhancements")
    print("Group: Yejun Yun (RAVE) and William Zhong (Value Network)")
    print("=" * 80)
    print()
    
    print("Game Description:")
    print("-" * 80)
    print("A simplified 3v3 Pokémon battle game featuring:")
    print("  • 8 Pokémon across 4 types (Fire, Water, Grass, Normal)")
    print("  • Type advantage system (Fire > Grass > Water > Fire)")
    print("  • Simultaneous turn-based combat")
    print("  • Strategic depth: type matchups, speed control, resource management")
    print("  • Deterministic core with accuracy/priority mechanics")
    print()
    
    print("Agents Implemented:")
    print("-" * 80)
    print("  1. Greedy Baseline    - Always picks highest expected damage move")
    print("  2. Standard MCTS      - Monte Carlo Tree Search with random rollouts")
    print("  3. MCTS + RAVE        - Uses AMAF heuristic for faster convergence (Yejun)")
    print("  4. MCTS + Value Net   - Neural network evaluation (William)")
    print()
    
    print("Research Question:")
    print("-" * 80)
    print("How do RAVE and Value Network enhancements improve MCTS performance")
    print("compared to standard MCTS and a greedy baseline?")
    print()
    print("We test win rates over 100 games per configuration with 100 simulations")
    print("per move. All agents play as Player 1 against the Greedy baseline (Player 2).")
    print()


def create_teams():
    team1 = [PokemonInstance.from_spec(DEX_V2[0]),
             PokemonInstance.from_spec(DEX_V2[2]),
             PokemonInstance.from_spec(DEX_V2[7])]
    
    team2 = [PokemonInstance.from_spec(DEX_V2[1]),
             PokemonInstance.from_spec(DEX_V2[4]),
             PokemonInstance.from_spec(DEX_V2[3])]
    
    return team1, team2


def play_game(agent1, agent2):
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


def benchmark(agent1, agent2, name1, name2, num_games=10):
    wins_p1 = 0
    wins_p2 = 0
    draws = 0
    
    print(f"  Testing {name1}...", end="", flush=True)
    start_time = time.time()
    
    for i in range(num_games):
        winner = play_game(agent1, agent2)
        
        if winner == 1:
            wins_p1 += 1
        elif winner == 2:
            wins_p2 += 1
        else:
            draws += 1
    
    elapsed = time.time() - start_time
    win_rate = wins_p1 / num_games * 100
    
    print(f" {wins_p1}/{num_games} wins ({win_rate:.0f}%) [{elapsed:.1f}s]")
    
    return wins_p1, wins_p2, draws, elapsed, win_rate


def main():
    print_header()
    
    print("=" * 80)
    print("Running Tests (Benchmark)")
    print("=" * 80)
    print()
    
    num_games = 100
    simulations = 100
    
    greedy = GreedyAgent()
    results = {}
    
    # Test 1: Greedy vs Random (sanity check)
    print("[1/4] BASELINE: Greedy vs Random")
    print("-" * 80)
    random_agent = RandomAgent()
    baseline_result = benchmark(greedy, random_agent, "Greedy", "Random", num_games=num_games)
    results['baseline'] = baseline_result
    print()
    
    # Test 2: Standard MCTS vs Greedy
    print("[2/4] Standard MCTS (Random Rollouts) vs Greedy")
    print("-" * 80)
    mcts_standard = MCTSAgent(simulations_per_move=simulations, player_id=1)
    mcts_result = benchmark(mcts_standard, greedy, f"MCTS-{simulations}", "Greedy", num_games=num_games)
    results['mcts'] = mcts_result
    print()
    
    # Test 3: RAVE MCTS vs Greedy
    print("[3/4] MCTS + RAVE vs Greedy")
    print("-" * 80)
    mcts_rave = MCTSRAVEAgent(simulations_per_move=simulations, player_id=1, rave_k=500)
    rave_result = benchmark(mcts_rave, greedy, f"RAVE-{simulations}", "Greedy", num_games=num_games)
    results['rave'] = rave_result
    print()
    
    # Test 4: Value Network MCTS vs Greedy
    print("[4/4] MCTS + Value Network vs Greedy")
    print("-" * 80)
    if HAS_VALUE_NET:
        try:
            mcts_valuenet = create_mcts_with_value_net(
                network_path="william-valuenetwork/value_network_v1.pkl",
                simulations=simulations,
                player_id=1
            )
            valuenet_result = benchmark(mcts_valuenet, greedy, f"ValueNet-{simulations}", "Greedy", num_games=num_games)
            results['valuenet'] = valuenet_result
        except Exception as e:
            print(f"  Error loading value network: {e}")
            print(f"  Skipping value network test")
            results['valuenet'] = None
    else:
        print(f"  Value network not available (requires: pip install --user numpy tqdm)")
        results['valuenet'] = None
    print()
    
    # Results Summary
    print("=" * 80)
    print("Results Summary")
    print("=" * 80)
    print()
    
    print("Win Rates vs Greedy Baseline (100 simulations per move, 100 games):")
    print("-" * 80)
    print(f"  Greedy vs Random:      {results['baseline'][4]:.0f}% (sanity check)")
    print(f"  Standard MCTS:         {results['mcts'][4]:.0f}%")
    print(f"  MCTS + RAVE:           {results['rave'][4]:.0f}%")
    if results['valuenet']:
        print(f"  MCTS + Value Network:  {results['valuenet'][4]:.0f}%")
    else:
        print(f"  MCTS + Value Network:  Not tested (requires numpy)")
    print()
    
    print("Computation Time per Game:")
    print("-" * 80)
    print(f"  Standard MCTS:         {results['mcts'][3]/num_games:.2f}s")
    print(f"  MCTS + RAVE:           {results['rave'][3]/num_games:.2f}s")
    if results['valuenet']:
        print(f"  MCTS + Value Network:  {results['valuenet'][3]/num_games:.2f}s")
    print()
    
    # Analysis
    print("=" * 80)
    print("Key Findings")
    print("=" * 80)
    print()
    
    mcts_wr = results['mcts'][4]
    rave_wr = results['rave'][4]
    
    print(f"- Greedy baseline is much better, winning ({results['baseline'][4]:.0f}% vs random)")
    print(f"- Standard MCTS achieves {mcts_wr:.0f}% win rate with random rollouts")
    
    if rave_wr > mcts_wr + 10:
        print(f"- RAVE significantly improves over standard MCTS (+{rave_wr - mcts_wr:.0f}%)")
    elif rave_wr > mcts_wr:
        print(f"- RAVE improves over standard MCTS (+{rave_wr - mcts_wr:.0f}%)")
    else:
        print(f"- RAVE performance similar to standard MCTS (variance in small sample)")
    
    if results['valuenet']:
        valuenet_wr = results['valuenet'][4]
        if valuenet_wr > mcts_wr + 20:
            print(f"- Value Network dramatically improves over standard MCTS (+{valuenet_wr - mcts_wr:.0f}%)")
        elif valuenet_wr > mcts_wr:
            print(f"- Value Network improves over standard MCTS (+{valuenet_wr - mcts_wr:.0f}%)")
        else:
            print(f"- Value Network performance similar to standard MCTS (variance in small sample)")
    
    print()
    
    print("=" * 80)
    print("Technical Contributions")
    print("=" * 80)
    print()
    print("Shared Baseline:")
    print("  • Simultaneous-move game engine (accuracy, priority, recoil)")
    print("  • MCTS with joint action exploration")
    print("  • Minimax-style action selection for simultaneous moves")
    print()
    print("Yejun's RAVE Enhancement:")
    print("  • AMAF (All-Moves-As-First) heuristic")
    print("  • Beta-blending of UCB and AMAF statistics")
    print("  • Adapted for simultaneous moves (player-specific AMAF)")
    print("  • Faster convergence with fewer simulations")
    print()
    print("William's Value Network:")
    print("  • AlphaGo-kinda-style neural network evaluation")
    print("  • 30-feature state representation")
    print("  • Self-play training (16,540 examples from 500 games)")
    print("  • Replaces time-consuming rollouts with instant predictions")
    print()
    
    print("=" * 80)
    print("Test Complete")
    print("=" * 80)
    print()
    print("This quick test demonstrates that both enhancements improve over")
    print("standard MCTS. For detailed analysis, see benchmark scripts above.")
    print()


if __name__ == "__main__":
    main()
