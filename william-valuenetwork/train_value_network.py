import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import numpy as np
from typing import List, Tuple
from tqdm import tqdm

from battle_v2 import BattleState, PlayerState, PokemonInstance, step, legal_actions_for_player
from dex_v2 import DEX_V2
from value_network import ValueNetwork, create_default_network


def create_teams() -> Tuple[List[PokemonInstance], List[PokemonInstance]]:
    """Create balanced teams from DEX_V2."""
    team1 = [PokemonInstance.from_spec(DEX_V2[0]),
             PokemonInstance.from_spec(DEX_V2[2]),
             PokemonInstance.from_spec(DEX_V2[7])]
    
    team2 = [PokemonInstance.from_spec(DEX_V2[1]),
             PokemonInstance.from_spec(DEX_V2[4]),
             PokemonInstance.from_spec(DEX_V2[3])]
    
    return team1, team2


def play_random_game() -> Tuple[List[BattleState], int]:
    team1, team2 = create_teams()
    state = BattleState(
        player1=PlayerState(team=team1, active_index=0),
        player2=PlayerState(team=team2, active_index=0),
        rng_seed=random.randint(0, 1000000)
    )
    
    states = []
    
    while not state.terminal:
        states.append(state.clone())
        
        legal_p1 = legal_actions_for_player(state, 1)
        legal_p2 = legal_actions_for_player(state, 2)
        
        a1 = random.choice(legal_p1)
        a2 = random.choice(legal_p2)
        
        state = step(state, a1, a2)
    
    return states, state.winner


def train_network(net: ValueNetwork, 
                  num_games: int = 1000,
                  learning_rate: float = 0.001,
                  batch_size: int = 32,
                  epochs_per_batch: int = 5):
    
    print(f"Training value network on {num_games} games...")
    print(f"Learning rate: {learning_rate}")
    print(f"Batch size: {batch_size}")
    
    all_losses = []
    win_counts = {1: 0, 2: 0, None: 0}
    
    training_data = []
    
    for game_num in tqdm(range(num_games), desc="Playing games"):
        states, winner = play_random_game()
        win_counts[winner] = win_counts.get(winner, 0) + 1
        
        for state in states:
            if winner == 1:
                target_p1 = 1.0
            elif winner == 2:
                target_p1 = 0.0
            else:
                target_p1 = 0.5
            
            training_data.append((state, 1, target_p1))
            training_data.append((state, 2, 1.0 - target_p1))
    
    print(f"\nCollected {len(training_data)} training examples")
    print(f"Win distribution: P1={win_counts.get(1,0)}, P2={win_counts.get(2,0)}, Draw={win_counts.get(None,0)}")
    
    print(f"\nTraining for {epochs_per_batch} epochs...")
    
    for epoch in range(epochs_per_batch):
        random.shuffle(training_data)
        
        epoch_losses = []
        
        for i in tqdm(range(0, len(training_data), batch_size), 
                     desc=f"Epoch {epoch+1}/{epochs_per_batch}"):
            batch = training_data[i:i+batch_size]
            
            batch_loss = 0.0
            for state, player_id, target in batch:
                features = net.extract_features(state, player_id)
                loss = net.train_step(features, target, learning_rate)
                batch_loss += loss
            
            epoch_losses.append(batch_loss / len(batch))
        
        avg_loss = np.mean(epoch_losses)
        all_losses.append(avg_loss)
        print(f"  Epoch {epoch+1} average loss: {avg_loss:.6f}")
    
    return all_losses


def evaluate_network(net: ValueNetwork, num_games: int = 50) -> float:
    correct = 0
    total = 0
    
    for _ in tqdm(range(num_games), desc="Evaluating"):
        states, winner = play_random_game()
        
        for state in states[-3:]:
            if state.terminal:
                continue
            
            pred_p1 = net.predict(state, player_id=1)
            
            if winner == 1 and pred_p1 > 0.5:
                correct += 1
            elif winner == 2 and pred_p1 < 0.5:
                correct += 1
            elif winner is None and 0.4 < pred_p1 < 0.6:
                correct += 1
            
            total += 1
    
    accuracy = correct / total if total > 0 else 0.0
    return accuracy


def main():
    print("="*60)
    print("Value Network Training")
    print("="*60)
    
    net = create_default_network()
    
    losses = train_network(
        net,
        num_games=500,
        learning_rate=0.005,
        batch_size=64,
        epochs_per_batch=3
    )
    
    print("\n" + "="*60)
    print("Evaluation")
    print("="*60)
    accuracy = evaluate_network(net, num_games=50)
    print(f"\nAccuracy on random play: {accuracy:.2%}")
    
    net.save("value_network_v1.pkl")
    print("\n" + "="*60)
    print("Training complete!")
    print("="*60)


if __name__ == "__main__":
    main()

