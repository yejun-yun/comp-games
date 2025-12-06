"""Test opponent-modeling MCTS."""

from benchmark import run_benchmark
from main import GreedyAgent
from mcts_opponent_model import OpponentModelMCTSAgent

def main():
    print("="*70)
    print("Testing Opponent-Modeling MCTS")
    print("(Assumes opponent plays greedy deterministically)")
    print("="*70)
    
    num_games = 30
    
    # Test different simulation counts
    for sims in [50, 100, 200, 500]:
        print(f"\n### OpponentModel-MCTS-{sims} vs Greedy ###")
        mcts = OpponentModelMCTSAgent(simulations_per_move=sims, player_id=1)
        greedy = GreedyAgent()
        result = run_benchmark(mcts, greedy, num_games, f"OppModel-{sims}", "Greedy")
        print(f"Win rate: {result['agent1_wins']/num_games*100:.1f}%")

if __name__ == "__main__":
    main()

