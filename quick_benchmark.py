"""Quick benchmark with fewer games for testing."""

from benchmark import run_benchmark
from main import GreedyAgent, RandomAgent
from mcts import MCTSAgent

def main():
    """Run a quick benchmark."""
    
    print("Quick Benchmark: MCTS vs Greedy")
    print("="*60)
    
    # Test with small number of games and simulations
    num_games = 20
    
    # 1. Greedy vs Random (sanity check)
    print("\n### Sanity Check: Greedy vs Random ###")
    greedy = GreedyAgent()
    random_agent = RandomAgent()
    run_benchmark(greedy, random_agent, num_games, "Greedy", "Random")
    
    # 2. MCTS (50 sims) vs Greedy
    print("\n### Main Test: MCTS-50 vs Greedy ###")
    mcts_50 = MCTSAgent(simulations_per_move=50, player_id=1)
    greedy_p2 = GreedyAgent()
    run_benchmark(mcts_50, greedy_p2, num_games, "MCTS-50", "Greedy")
    
    # 3. MCTS (100 sims) vs Greedy
    print("\n### Main Test: MCTS-100 vs Greedy ###")
    mcts_100 = MCTSAgent(simulations_per_move=100, player_id=1)
    greedy_p2_2 = GreedyAgent()
    run_benchmark(mcts_100, greedy_p2_2, num_games, "MCTS-100", "Greedy")

if __name__ == "__main__":
    main()

