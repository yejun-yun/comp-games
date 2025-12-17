"""
Train Value Network via Self-Play

Generates training data by playing games and trains the network
to predict game outcomes.
"""

import sys
import os
# Add parent directory to path to import game modules
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
    """
    Play one game with random moves.
    
    Returns:
        List of states encountered, winner (1, 2, or None for draw)
    """
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
    """
    Train value network via self-play.
    
    Args:
        net: Value network to train
        num_games: Number of self-play games
        learning_rate: Learning rate
        batch_size: Number of games before weight update
        epochs_per_batch: Number of training passes over each batch
    """
    
    print(f"Training value network on {num_games} games...")
    print(f"Learning rate: {learning_rate}")
    print(f"Batch size: {batch_size}")
    
    all_losses = []
    win_counts = {1: 0, 2: 0, None: 0}
    
    # Collect training data
    training_data = []
    
    for game_num in tqdm(range(num_games), desc="Playing games"):
        states, winner = play_random_game()
        win_counts[winner] = win_counts.get(winner, 0) + 1
        
        # Create training examples from this game
        for state in states:
            # Target: 1.0 if player 1 wins, 0.0 if player 2 wins, 0.5 for draw
            if winner == 1:
                target_p1 = 1.0
            elif winner == 2:
                target_p1 = 0.0
            else:
                target_p1 = 0.5
            
            # Add both perspectives
            training_data.append((state, 1, target_p1))
            training_data.append((state, 2, 1.0 - target_p1))
    
    print(f"\nCollected {len(training_data)} training examples")
    print(f"Win distribution: P1={win_counts.get(1,0)}, P2={win_counts.get(2,0)}, Draw={win_counts.get(None,0)}")
    
    # Train on collected data
    print(f"\nTraining for {epochs_per_batch} epochs...")
    
    for epoch in range(epochs_per_batch):
        # Shuffle data
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
    """
    Evaluate network accuracy on random games.
    
    Returns:
        Accuracy: fraction of correct predictions
    """
    correct = 0
    total = 0
    
    for _ in tqdm(range(num_games), desc="Evaluating"):
        states, winner = play_random_game()
        
        # Check prediction on final few states
        for state in states[-3:]:
            if state.terminal:
                continue
            
            pred_p1 = net.predict(state, player_id=1)
            
            # Check if prediction matches outcome
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
    """Train and save value network."""
    print("="*60)
    print("VALUE NETWORK TRAINING")
    print("="*60)
    
    # Create network
    net = create_default_network()
    
    # Train
    losses = train_network(
        net,
        num_games=500,  # Start small for testing
        learning_rate=0.005,
        batch_size=64,
        epochs_per_batch=3
    )
    
    # Evaluate
    print("\n" + "="*60)
    print("EVALUATION")
    print("="*60)
    accuracy = evaluate_network(net, num_games=50)
    print(f"\nAccuracy on random play: {accuracy:.2%}")
    
    # Save
    net.save("value_network_v1.pkl")
    print("\n" + "="*60)
    print("Training complete!")
    print("="*60)


if __name__ == "__main__":
    main()

