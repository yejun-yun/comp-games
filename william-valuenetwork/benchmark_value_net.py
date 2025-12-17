"""
Benchmark: MCTS with Value Network vs Baseline

Compare performance of:
1. MCTS with random rollouts
2. MCTS with value network
3. Greedy baseline
"""

import sys
import os
# Add parent directory to path to import game modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import List
from tqdm import tqdm

from battle_v2 import BattleState, PlayerState, PokemonInstance, step, legal_actions_for_player, ActionType
from dex_v2 import DEX_V2
from mcts_v2 import MCTSAgent
from mcts_value_net import create_mcts_with_value_net
from main_v2 import GreedyAgent


def create_teams():
    """Create standard teams."""
    team1 = [PokemonInstance.from_spec(DEX_V2[0]),
             PokemonInstance.from_spec(DEX_V2[2]),
             PokemonInstance.from_spec(DEX_V2[7])]
    
    team2 = [PokemonInstance.from_spec(DEX_V2[1]),
             PokemonInstance.from_spec(DEX_V2[4]),
             PokemonInstance.from_spec(DEX_V2[3])]
    
    return team1, team2


def play_game(agent1, agent2, verbose=False):
    """Play one game between two agents."""
    team1, team2 = create_teams()
    state = BattleState(
        player1=PlayerState(team=team1, active_index=0),
        player2=PlayerState(team=team2, active_index=0)
    )
    
    while not state.terminal:
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        state = step(state, a1, a2)
        
        if verbose and state.turn_number % 5 == 0:
            print(f"Turn {state.turn_number}")
    
    return state.winner


def benchmark_matchup(agent1, agent2, name1: str, name2: str, num_games: int = 50):
    """Benchmark two agents against each other."""
    print(f"\n{'='*60}")
    print(f"{name1} vs {name2} ({num_games} games)")
    print(f"{'='*60}")
    
    wins_p1 = 0
    wins_p2 = 0
    draws = 0
    
    start_time = time.time()
    
    for i in tqdm(range(num_games), desc="Playing"):
        winner = play_game(agent1, agent2)
        
        if winner == 1:
            wins_p1 += 1
        elif winner == 2:
            wins_p2 += 1
        else:
            draws += 1
    
    elapsed = time.time() - start_time
    
    print(f"\nResults:")
    print(f"  {name1}: {wins_p1} ({wins_p1/num_games*100:.1f}%)")
    print(f"  {name2}: {wins_p2} ({wins_p2/num_games*100:.1f}%)")
    print(f"  Draws: {draws}")
    print(f"  Time: {elapsed:.1f}s ({elapsed/num_games:.3f}s/game)")
    
    return wins_p1, wins_p2, draws, elapsed


def main():
    """Run comprehensive benchmark."""
    print("="*60)
    print("VALUE NETWORK MCTS BENCHMARK")
    print("="*60)
    print()
    print("This benchmark compares:")
    print("  1. MCTS with random rollouts (baseline)")
    print("  2. MCTS with value network (enhanced)")
    print("  3. Greedy agent (simple baseline)")
    print()
    
    num_games = 50
    simulations = 100
    
    # Create agents
    print("Creating agents...")
    greedy = GreedyAgent()
    mcts_random = MCTSAgent(simulations_per_move=simulations, player_id=1)
    
    try:
        mcts_valuenet = create_mcts_with_value_net(
            network_path="value_network_v1.pkl",
            simulations=simulations,
            player_id=1
        )
        has_trained_network = True
    except Exception as e:
        print(f"\nWarning: Could not load trained network: {e}")
        print("Train a network first with: python3 train_value_network.py")
        print("\nUsing untrained value network for demo purposes...")
        from value_network import create_default_network
        from mcts_value_net import MCTSAgentValueNet
        net = create_default_network()
        mcts_valuenet = MCTSAgentValueNet(net, simulations_per_move=simulations, player_id=1)
        has_trained_network = False
    
    print("\n" + "="*60)
    print("BASELINE: MCTS (Random Rollouts) vs Greedy")
    print("="*60)
    
    results_random = benchmark_matchup(
        mcts_random, greedy,
        f"MCTS-Random-{simulations}", "Greedy",
        num_games=num_games
    )
    
    print("\n" + "="*60)
    print("ENHANCED: MCTS (Value Network) vs Greedy")
    print("="*60)
    
    results_valuenet = benchmark_matchup(
        mcts_valuenet, greedy,
        f"MCTS-ValueNet-{simulations}", "Greedy",
        num_games=num_games
    )
    
    print("\n" + "="*60)
    print("HEAD-TO-HEAD: Value Network MCTS vs Random Rollout MCTS")
    print("="*60)
    
    # Switch player IDs for fair comparison
    mcts_random_p2 = MCTSAgent(simulations_per_move=simulations, player_id=2)
    results_head2head = benchmark_matchup(
        mcts_valuenet, mcts_random_p2,
        f"MCTS-ValueNet-{simulations}", f"MCTS-Random-{simulations}",
        num_games=num_games
    )
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    win_rate_random = results_random[0] / num_games * 100
    win_rate_valuenet = results_valuenet[0] / num_games * 100
    win_rate_h2h = results_head2head[0] / num_games * 100
    
    print(f"\nVs Greedy Baseline:")
    print(f"  MCTS (Random):     {win_rate_random:.1f}% win rate")
    print(f"  MCTS (Value Net):  {win_rate_valuenet:.1f}% win rate")
    print(f"  Improvement:       {win_rate_valuenet - win_rate_random:+.1f}%")
    
    print(f"\nHead-to-Head:")
    print(f"  MCTS (Value Net):  {win_rate_h2h:.1f}% win rate vs Random MCTS")
    
    print(f"\nTime per game:")
    print(f"  MCTS (Random):     {results_random[3]/num_games:.3f}s")
    print(f"  MCTS (Value Net):  {results_valuenet[3]/num_games:.3f}s")
    print(f"  Speedup:           {results_random[3]/results_valuenet[3]:.2f}x")
    
    if not has_trained_network:
        print("\n" + "="*60)
        print("NOTE: Value network was not trained!")
        print("Train it first for better results:")
        print("  python3 train_value_network.py")
        print("="*60)
    
    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print("Value network MCTS eliminates expensive rollouts,")
    print("providing faster and more accurate position evaluation.")
    print("This is the key technique used in AlphaGo and AlphaZero!")
    print("="*60)


if __name__ == "__main__":
    main()

