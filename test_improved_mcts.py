"""Test improved MCTS implementation."""

from benchmark import run_benchmark
from main import GreedyAgent, RandomAgent
from mcts_improved import ImprovedMCTSAgent

def main():
    print("="*70)
    print("Testing IMPROVED MCTS vs Greedy Baseline")
    print("="*70)
    
    num_games = 30
    
    # Test 1: Improved MCTS-50 vs Greedy
    print("\n### Test 1: Improved MCTS-50 vs Greedy ###")
    mcts_50 = ImprovedMCTSAgent(simulations_per_move=50, player_id=1, rollout_depth=8)
    greedy = GreedyAgent()
    result1 = run_benchmark(mcts_50, greedy, num_games, "ImprovedMCTS-50", "Greedy")
    
    # Test 2: Improved MCTS-100 vs Greedy
    print("\n### Test 2: Improved MCTS-100 vs Greedy ###")
    mcts_100 = ImprovedMCTSAgent(simulations_per_move=100, player_id=1, rollout_depth=8)
    greedy2 = GreedyAgent()
    result2 = run_benchmark(mcts_100, greedy2, num_games, "ImprovedMCTS-100", "Greedy")
    
    # Test 3: Improved MCTS-200 vs Greedy
    print("\n### Test 3: Improved MCTS-200 vs Greedy ###")
    mcts_200 = ImprovedMCTSAgent(simulations_per_move=200, player_id=1, rollout_depth=8)
    greedy3 = GreedyAgent()
    result3 = run_benchmark(mcts_200, greedy3, num_games, "ImprovedMCTS-200", "Greedy")
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Improved MCTS-50:  {result1['agent1_wins']/num_games*100:.1f}% win rate")
    print(f"Improved MCTS-100: {result2['agent1_wins']/num_games*100:.1f}% win rate")
    print(f"Improved MCTS-200: {result3['agent1_wins']/num_games*100:.1f}% win rate")
    print("="*70)

if __name__ == "__main__":
    main()

