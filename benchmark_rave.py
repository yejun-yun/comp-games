import time
import random

from battle_v2 import BattleState, PlayerState, PokemonInstance, step
from dex_v2 import DEX_V2
from main_v2 import GreedyAgent, RandomAgent
from mcts_v2 import MCTSAgent
from mcts_rave import MCTSRAVEAgent, MCTSRAVEGreedyAgent


def create_teams():
    t1 = [PokemonInstance.from_spec(DEX_V2[0]),
          PokemonInstance.from_spec(DEX_V2[2]),
          PokemonInstance.from_spec(DEX_V2[7])]
    t2 = [PokemonInstance.from_spec(DEX_V2[1]),
          PokemonInstance.from_spec(DEX_V2[4]),
          PokemonInstance.from_spec(DEX_V2[3])]
    return t1, t2


def run_single_game(agent1, agent2) -> int:
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


def run_benchmark(agent1, agent2, num_games: int, name1: str, name2: str) -> dict:
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

    return {
        "p1_wins": wins_1,
        "p2_wins": wins_2,
        "draws": draws,
        "time": elapsed,
        "win_rate": wins_1 / num_games * 100
    }


def main():
    print("\n" + "="*60)
    print("RAVE Enhancement Benchmark")
    print("="*60)

    num_games = 50
    budgets = [50, 100, 200]

    mcts_results = []
    rave_results = []

    for sims in budgets:
        print(f"\n\n{'#'*60}")
        print(f"# SIMULATION BUDGET: {sims}")
        print(f"{'#'*60}")

        print("\n--- Standard MCTS ---")
        mcts = MCTSAgent(simulations_per_move=sims, player_id=1)
        greedy = GreedyAgent()
        mcts_result = run_benchmark(mcts, greedy, num_games, f"MCTS-{sims}", "Greedy")
        mcts_results.append((sims, mcts_result))

        print("\n--- MCTS + RAVE ---")
        rave = MCTSRAVEAgent(simulations_per_move=sims, player_id=1, rave_k=500)
        greedy = GreedyAgent()
        rave_result = run_benchmark(rave, greedy, num_games, f"RAVE-{sims}", "Greedy")
        rave_results.append((sims, rave_result))

    print(f"\n\n{'#'*60}")
    print("# HEAD-TO-HEAD: MCTS+RAVE vs Standard MCTS")
    print(f"{'#'*60}")

    for sims in [100, 200]:
        mcts = MCTSAgent(simulations_per_move=sims, player_id=1)
        rave = MCTSRAVEAgent(simulations_per_move=sims, player_id=2, rave_k=500)
        run_benchmark(mcts, rave, num_games, f"MCTS-{sims}", f"RAVE-{sims}")

    print(f"\n\n{'#'*60}")
    print("# RAVE_K PARAMETER TUNING (at 100 simulations)")
    print(f"{'#'*60}")

    k_values = [100, 500, 1000, 3000]
    k_results = []

    for k in k_values:
        rave = MCTSRAVEAgent(simulations_per_move=100, player_id=1, rave_k=k)
        greedy = GreedyAgent()
        result = run_benchmark(rave, greedy, num_games, f"RAVE(k={k})", "Greedy")
        k_results.append((k, result))

    print("\n\n" + "="*60)
    print("SUMMARY")
    print("="*60)

    print("\n--- Win Rate vs Greedy ---")
    print(f"{'Budget':<10} {'MCTS':<15} {'RAVE':<15} {'Difference':<15}")
    print("-" * 55)
    for (sims, mcts_r), (_, rave_r) in zip(mcts_results, rave_results):
        diff = rave_r['win_rate'] - mcts_r['win_rate']
        sign = "+" if diff >= 0 else ""
        print(f"{sims:<10} {mcts_r['win_rate']:<14.1f}% {rave_r['win_rate']:<14.1f}% {sign}{diff:.1f}%")

    print("\n--- Time per Game ---")
    print(f"{'Budget':<10} {'MCTS':<15} {'RAVE':<15}")
    print("-" * 40)
    for (sims, mcts_r), (_, rave_r) in zip(mcts_results, rave_results):
        mcts_time = mcts_r['time'] / num_games
        rave_time = rave_r['time'] / num_games
        print(f"{sims:<10} {mcts_time:<14.3f}s {rave_time:<14.3f}s")

    print("\n--- RAVE_K Parameter Effect (100 sims) ---")
    print(f"{'K value':<10} {'Win Rate':<15}")
    print("-" * 25)
    for k, result in k_results:
        print(f"{k:<10} {result['win_rate']:<14.1f}%")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()
