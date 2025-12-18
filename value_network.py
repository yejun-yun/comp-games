import numpy as np
import pickle
from typing import List, Tuple
from battle_v2 import BattleState, PokemonInstance, PlayerState


class ValueNetwork:
    def __init__(self, input_size: int = 30, hidden_sizes: List[int] = [64, 32]):
        self.layer_sizes = [input_size] + hidden_sizes + [1]
        self.weights = []
        self.biases = []
        
        for i in range(len(self.layer_sizes) - 1):
            fan_in = self.layer_sizes[i]
            fan_out = self.layer_sizes[i + 1]
            limit = np.sqrt(6.0 / (fan_in + fan_out))
            
            w = np.random.uniform(-limit, limit, (fan_in, fan_out))
            b = np.zeros((1, fan_out))
            
            self.weights.append(w)
            self.biases.append(b)
    
    def extract_features(self, state: BattleState, player_id: int = 1) -> np.ndarray:
        features = []
        
        my_state = state.player1 if player_id == 1 else state.player2
        opp_state = state.player2 if player_id == 1 else state.player1
        
        for mon in my_state.team:
            hp_ratio = mon.current_hp / mon.spec.max_hp if not mon.fainted else 0.0
            features.append(hp_ratio)
        
        for mon in opp_state.team:
            hp_ratio = mon.current_hp / mon.spec.max_hp if not mon.fainted else 0.0
            features.append(hp_ratio)
        
        my_active = my_state.team[my_state.active_index]
        opp_active = opp_state.team[opp_state.active_index]
        
        type_map = {"Fire": [1,0,0,0], "Water": [0,1,0,0], 
                    "Grass": [0,0,1,0], "Normal": [0,0,0,1]}
        features.extend(type_map.get(my_active.spec.type, [0,0,0,0]))
        features.extend(type_map.get(opp_active.spec.type, [0,0,0,0]))
        
        features.append(my_active.spec.attack / 20.0)
        features.append(my_active.spec.defense / 20.0)
        features.append(my_active.spec.speed / 20.0)
        features.append(my_active.current_hp / my_active.spec.max_hp if not my_active.fainted else 0.0)
        
        features.append(opp_active.spec.attack / 20.0)
        features.append(opp_active.spec.defense / 20.0)
        features.append(opp_active.spec.speed / 20.0)
        features.append(opp_active.current_hp / opp_active.spec.max_hp if not opp_active.fainted else 0.0)
        
        from battle_v2 import get_type_multiplier
        my_advantage = get_type_multiplier(my_active.spec.type, opp_active.spec.type)
        opp_advantage = get_type_multiplier(opp_active.spec.type, my_active.spec.type)
        type_advantage = (my_advantage - opp_advantage) / 2.0  # -1 to 1
        features.append(type_advantage)
        
        speed_diff = my_active.spec.speed - opp_active.spec.speed
        speed_advantage = np.tanh(speed_diff / 5.0)  # Normalize to -1 to 1
        features.append(speed_advantage)
        
        my_alive = sum(1 for m in my_state.team if not m.fainted) / 3.0
        opp_alive = sum(1 for m in opp_state.team if not m.fainted) / 3.0
        features.append(my_alive)
        features.append(opp_alive)
        
        my_max_priority = max(move.priority for move in my_active.spec.moves) / 5.0
        opp_max_priority = max(move.priority for move in opp_active.spec.moves) / 5.0
        features.append(my_max_priority)
        features.append(opp_max_priority)
        
        my_total_hp = sum(m.current_hp for m in my_state.team)
        opp_total_hp = sum(m.current_hp for m in opp_state.team)
        total = my_total_hp + opp_total_hp
        hp_ratio = my_total_hp / total if total > 0 else 0.5
        features.append(hp_ratio)
        
        features.append(min(state.turn_number / 30.0, 1.0))
        
        return np.array(features, dtype=np.float32).reshape(1, -1)
    
    def relu(self, x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)
    
    def sigmoid(self, x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))
    
    def forward(self, x: np.ndarray) -> float:
        activation = x
        
        for i in range(len(self.weights) - 1):
            activation = activation @ self.weights[i] + self.biases[i]
            activation = self.relu(activation)
        
        activation = activation @ self.weights[-1] + self.biases[-1]
        output = self.sigmoid(activation)
        
        return float(output[0, 0])
    
    def predict(self, state: BattleState, player_id: int = 1) -> float: 
        features = self.extract_features(state, player_id)
        return self.forward(features)
    
    def train_step(self, features: np.ndarray, target: float, learning_rate: float = 0.01):
        activations = [features]
        activation = features
        
        for i in range(len(self.weights) - 1):
            z = activation @ self.weights[i] + self.biases[i]
            activation = self.relu(z)
            activations.append(activation)
        
        z_out = activation @ self.weights[-1] + self.biases[-1]
        output = self.sigmoid(z_out)
        
        error = output - target
        
        delta = error * output * (1 - output)  # Sigmoid derivative
        
        weight_grads = []
        bias_grads = []
        
        weight_grads.append(activations[-1].T @ delta)
        bias_grads.append(delta)
        
        for i in range(len(self.weights) - 2, -1, -1):
            delta = (delta @ self.weights[i + 1].T) * (activations[i + 1] > 0)  # ReLU derivative
            weight_grads.insert(0, activations[i].T @ delta)
            bias_grads.insert(0, delta)
        
        for i in range(len(self.weights)):
            self.weights[i] -= learning_rate * weight_grads[i]
            self.biases[i] -= learning_rate * bias_grads[i]
        
        return float(error ** 2)
    
    def save(self, filepath: str):
        with open(filepath, 'wb') as f:
            pickle.dump({
                'weights': self.weights,
                'biases': self.biases,
                'layer_sizes': self.layer_sizes
            }, f)
        print(f"Value network saved to {filepath}")
    
    def load(self, filepath: str):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.weights = data['weights']
            self.biases = data['biases']
            self.layer_sizes = data['layer_sizes']
        print(f"Value network loaded from {filepath}")


def create_default_network() -> ValueNetwork:
    return ValueNetwork(input_size=30, hidden_sizes=[64, 32])


if __name__ == "__main__":
    from dex_v2 import DEX_V2
    from battle_v2 import PokemonInstance, PlayerState, BattleState
    
    team1 = [PokemonInstance.from_spec(DEX_V2[0]),
             PokemonInstance.from_spec(DEX_V2[2]),
             PokemonInstance.from_spec(DEX_V2[7])]
    
    team2 = [PokemonInstance.from_spec(DEX_V2[1]),
             PokemonInstance.from_spec(DEX_V2[4]),
             PokemonInstance.from_spec(DEX_V2[3])]
    
    state = BattleState(
        player1=PlayerState(team=team1, active_index=0),
        player2=PlayerState(team=team2, active_index=0)
    )
    
    net = create_default_network()
    features = net.extract_features(state, player_id=1)
    print(f"Feature vector shape: {features.shape}")
    print(f"Feature vector: {features}")
    
    prediction = net.predict(state, player_id=1)
    print(f"\nInitial prediction (random weights): {prediction:.3f}")
    
    loss = net.train_step(features, target=1.0, learning_rate=0.01)
    print(f"Training loss: {loss:.4f}")
    
    prediction_after = net.predict(state, player_id=1)
    print(f"Prediction after training: {prediction_after:.3f}")

