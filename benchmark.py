"""
Benchmark script to compare agent performance.

Runs multiple games between different agents and reports win rates.
"""

import sys
import time
from typing import List, Tuple, Dict
from battle import BattleState, PlayerState, PokemonInstance, step, legal_actions_for_player
from main import Agent, RandomAgent, GreedyAgent, create_teams
from mcts import MCTSAgent

def run_single_game(agent1: Agent, agent2: Agent, verbose: bool = False) -> int:
    """
    Run a single game between two agents.
    
    Returns:
        1 if agent1 wins, 2 if agent2 wins, 0 if draw
    """
    t1, t2 = create_teams()
    p1_state = PlayerState(team=t1, active_index=0)
    p2_state = PlayerState(team=t2, active_index=0)
    state = BattleState(player1=p1_state, player2=p2_state)
    
    turn_count = 0
    max_turns = 100  # Prevent infinite games
    
    while not state.terminal and turn_count < max_turns:
        a1 = agent1.choose_action(state, 1)
        a2 = agent2.choose_action(state, 2)
        
        if verbose:
            print(f"Turn {state.turn_number}: P1={a1}, P2={a2}")
        
        state = step(state, a1, a2)
        turn_count += 1
    
    if state.terminal:
        if verbose:
            print(f"Game ended: Winner = Player {state.winner}")
        return state.winner if state.winner else 0
    else:
        if verbose:
            print("Game reached max turns, calling it a draw")
        return 0

def run_benchmark(
    agent1: Agent,
    agent2: Agent,
    num_games: int = 100,
    agent1_name: str = "Agent1",
    agent2_name: str = "Agent2",
    verbose: bool = False
) -> Dict:
    """
    Run multiple games and return statistics.
    
    Returns:
        Dict with keys: 'agent1_wins', 'agent2_wins', 'draws', 'total_games'
    """
    results = {
        'agent1_wins': 0,
        'agent2_wins': 0,
        'draws': 0,
        'total_games': num_games
    }
    
    print(f"\n{'='*60}")
    print(f"Running benchmark: {agent1_name} vs {agent2_name}")
    print(f"Number of games: {num_games}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    for i in range(num_games):
        if (i + 1) % 10 == 0:
            print(f"Progress: {i + 1}/{num_games} games completed...")
        
        winner = run_single_game(agent1, agent2, verbose=verbose)
        
        if winner == 1:
            results['agent1_wins'] += 1
        elif winner == 2:
            results['agent2_wins'] += 1
        else:
            results['draws'] += 1
    
    elapsed_time = time.time() - start_time
    
    # Print results
    print(f"\n{'='*60}")
    print(f"RESULTS: {agent1_name} vs {agent2_name}")
    print(f"{'='*60}")
    print(f"{agent1_name} wins: {results['agent1_wins']} ({results['agent1_wins']/num_games*100:.1f}%)")
    print(f"{agent2_name} wins: {results['agent2_wins']} ({results['agent2_wins']/num_games*100:.1f}%)")
    print(f"Draws: {results['draws']} ({results['draws']/num_games*100:.1f}%)")
    print(f"Total time: {elapsed_time:.2f}s")
    print(f"Avg time per game: {elapsed_time/num_games:.3f}s")
    print(f"{'='*60}\n")
    
    return results

def main():
    """Run various benchmarks."""
    
    print("Mini Pokémon Battle - Agent Benchmark")
    print("="*60)
    
    # Configuration
    num_games = 100
    
    # 1. Greedy vs Random (Baseline)
    print("\n### BENCHMARK 1: Greedy vs Random ###")
    greedy = GreedyAgent()
    random_agent = RandomAgent()
    run_benchmark(greedy, random_agent, num_games, "Greedy", "Random")
    
    # 2. MCTS (100 sims) vs Random
    print("\n### BENCHMARK 2: MCTS-100 vs Random ###")
    mcts_100 = MCTSAgent(simulations_per_move=100, player_id=1)
    run_benchmark(mcts_100, random_agent, num_games, "MCTS-100", "Random")
    
    # 3. MCTS (100 sims) vs Greedy
    print("\n### BENCHMARK 3: MCTS-100 vs Greedy ###")
    mcts_100_p1 = MCTSAgent(simulations_per_move=100, player_id=1)
    greedy_p2 = GreedyAgent()
    run_benchmark(mcts_100_p1, greedy_p2, num_games, "MCTS-100", "Greedy")
    
    # 4. MCTS scaling experiment: vary simulation count
    print("\n### BENCHMARK 4: MCTS Scaling (vs Greedy) ###")
    simulation_counts = [10, 50, 100, 200, 500]
    
    for sim_count in simulation_counts:
        mcts = MCTSAgent(simulations_per_move=sim_count, player_id=1)
        greedy = GreedyAgent()
        results = run_benchmark(
            mcts, greedy, 
            num_games=50,  # Fewer games for high sim counts
            agent1_name=f"MCTS-{sim_count}",
            agent2_name="Greedy"
        )
        
        # Save for plotting later if desired
        print(f"MCTS-{sim_count}: Win rate = {results['agent1_wins']/results['total_games']*100:.1f}%")

if __name__ == "__main__":
    main()

