"""Quick test to verify MCTS works."""

from battle import BattleState, PlayerState
from main import create_teams, RandomAgent, GreedyAgent
from mcts import MCTSAgent

def test_mcts_basic():
    """Test that MCTS can choose an action."""
    print("Testing MCTS basic functionality...")
    
    t1, t2 = create_teams()
    p1_state = PlayerState(team=t1, active_index=0)
    p2_state = PlayerState(team=t2, active_index=0)
    state = BattleState(player1=p1_state, player2=p2_state)
    
    # Create MCTS agent with small simulation count for speed
    mcts = MCTSAgent(simulations_per_move=10, player_id=1)
    
    # Get an action
    action = mcts.choose_action(state, 1)
    print(f"MCTS chose action: {action}")
    print("✓ MCTS basic test passed!")
    
def test_mcts_vs_random():
    """Test a quick game of MCTS vs Random."""
    print("\nTesting MCTS vs Random (1 game)...")
    
    from benchmark import run_single_game
    
    mcts = MCTSAgent(simulations_per_move=50, player_id=1)
    random_agent = RandomAgent()
    
    winner = run_single_game(mcts, random_agent, verbose=False)
    print(f"Winner: Player {winner}")
    print("✓ MCTS vs Random test completed!")

if __name__ == "__main__":
    test_mcts_basic()
    test_mcts_vs_random()
    print("\n✓ All tests passed!")

