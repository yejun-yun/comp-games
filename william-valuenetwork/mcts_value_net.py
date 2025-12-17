"""
MCTS with Value Network

Enhanced MCTS that uses a learned value network instead of random rollouts.
Similar to AlphaGo Zero's approach.
"""

import sys
import os
# Add parent directory to path to import game modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
import random
from typing import Dict, Tuple, Optional
from battle_v2 import BattleState, ActionType, step, legal_actions_for_player
from value_network import ValueNetwork


class MCTSNodeValueNet:
    """MCTS node that uses value network for evaluation."""
    
    def __init__(self, state: BattleState, parent: Optional['MCTSNodeValueNet'] = None,
                 my_player: int = 1):
        self.state = state
        self.parent = parent
        self.my_player = my_player
        
        # Children indexed by JOINT actions
        self.children: Dict[Tuple[ActionType, ActionType], 'MCTSNodeValueNet'] = {}
        
        self.visits = 0
        self.value_sum = 0.0  # Sum of values (from value network)
        self.prior = 0.0  # Could use policy network here
    
    def is_fully_expanded(self) -> bool:
        if self.state.terminal:
            return True
        legal_p1 = legal_actions_for_player(self.state, 1)
        legal_p2 = legal_actions_for_player(self.state, 2)
        total = len(legal_p1) * len(legal_p2)
        return len(self.children) >= total
    
    def get_untried_action(self) -> Optional[Tuple[ActionType, ActionType]]:
        legal_p1 = legal_actions_for_player(self.state, 1)
        legal_p2 = legal_actions_for_player(self.state, 2)
        all_joint = [(a1, a2) for a1 in legal_p1 for a2 in legal_p2]
        untried = [ja for ja in all_joint if ja not in self.children]
        return random.choice(untried) if untried else None
    
    def best_child(self, exploration_weight: float = 1.414) -> 'MCTSNodeValueNet':
        best_score = -float('inf')
        best_child = None
        
        for child in self.children.values():
            if child.visits == 0:
                return child
            
            # UCB with value network
            value = child.value_sum / child.visits
            exploration = exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            ucb = value + exploration
            
            if ucb > best_score:
                best_score = ucb
                best_child = child
        
        return best_child
    
    def expand(self, joint_action: Tuple[ActionType, ActionType]) -> 'MCTSNodeValueNet':
        """Expand with joint action."""
        new_state = step(self.state, joint_action[0], joint_action[1])
        child = MCTSNodeValueNet(new_state, parent=self, my_player=self.my_player)
        self.children[joint_action] = child
        return child


class MCTSAgentValueNet:
    """
    MCTS Agent with Value Network Evaluation.
    
    Uses a neural network to evaluate leaf positions instead of random rollouts.
    Much faster and stronger than rollout-based MCTS.
    """
    
    def __init__(self, value_network: ValueNetwork, 
                 simulations_per_move: int = 1000, 
                 player_id: int = 1,
                 exploration_weight: float = 1.414):
        self.value_network = value_network
        self.simulations_per_move = simulations_per_move
        self.player_id = player_id
        self.exploration_weight = exploration_weight
    
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        """
        Choose best action using MCTS with value network.
        
        Uses minimax-style selection for simultaneous moves.
        """
        root = MCTSNodeValueNet(state, my_player=player_id)
        
        # Run simulations
        for _ in range(self.simulations_per_move):
            self._simulate(root)
        
        legal_actions = legal_actions_for_player(state, player_id)
        opp_player = 2 if player_id == 1 else 1
        legal_opp = legal_actions_for_player(state, opp_player)
        
        best_action = None
        best_worst_case = -float('inf')
        
        # For each of MY actions, find the worst-case outcome
        for my_action in legal_actions:
            worst_case_value = float('inf')
            total_visits = 0
            
            # Check all opponent responses
            for opp_action in legal_opp:
                if player_id == 1:
                    joint = (my_action, opp_action)
                else:
                    joint = (opp_action, my_action)
                
                if joint in root.children:
                    child = root.children[joint]
                    if child.visits > 0:
                        # Value from my perspective
                        avg_value = child.value_sum / child.visits
                        
                        # Track worst case
                        worst_case_value = min(worst_case_value, avg_value)
                        total_visits += child.visits
            
            # Pick action with best worst-case
            if total_visits > 0 and worst_case_value < float('inf'):
                if worst_case_value > best_worst_case:
                    best_worst_case = worst_case_value
                    best_action = my_action
        
        # Fallback: most visited
        if best_action is None:
            action_visits = {}
            for my_action in legal_actions:
                visits = 0
                for opp_action in legal_opp:
                    joint = (my_action, opp_action) if player_id == 1 else (opp_action, my_action)
                    if joint in root.children:
                        visits += root.children[joint].visits
                action_visits[my_action] = visits
            best_action = max(legal_actions, key=lambda a: action_visits.get(a, 0))
        
        return best_action
    
    def _simulate(self, node: MCTSNodeValueNet) -> float:
        """Run one MCTS simulation with value network evaluation."""
        # Selection: traverse tree until leaf
        current = node
        while not current.state.terminal and current.is_fully_expanded():
            current = current.best_child(self.exploration_weight)
        
        # Expansion: if not terminal and not fully expanded, expand
        if not current.state.terminal:
            untried = current.get_untried_action()
            if untried:
                current = current.expand(untried)
        
        # Evaluation: use value network instead of rollout!
        if current.state.terminal:
            # Terminal state: exact value
            if current.state.winner == self.player_id:
                value = 1.0
            elif current.state.winner is None:
                value = 0.5
            else:
                value = 0.0
        else:
            # Non-terminal: use value network
            value = self.value_network.predict(current.state, self.player_id)
        
        # Backpropagation: update all ancestors
        while current is not None:
            current.visits += 1
            current.value_sum += value
            current = current.parent
        
        return value


# Convenience function for easy import
def create_mcts_with_value_net(network_path: str = "value_network_v1.pkl",
                               simulations: int = 1000,
                               player_id: int = 1) -> MCTSAgentValueNet:
    """
    Create MCTS agent with pre-trained value network.
    
    Args:
        network_path: Path to saved value network
        simulations: Number of MCTS simulations per move
        player_id: Player ID (1 or 2)
    
    Returns:
        MCTSAgentValueNet ready to play
    """
    from value_network import create_default_network
    
    net = create_default_network()
    try:
        net.load(network_path)
        print(f"Loaded value network from {network_path}")
    except FileNotFoundError:
        print(f"Warning: {network_path} not found. Using random initialization.")
        print("Train a network first with: python3 train_value_network.py")
    
    return MCTSAgentValueNet(net, simulations_per_move=simulations, player_id=player_id)


if __name__ == "__main__":
    # Test the value network MCTS
    from dex_v2 import DEX_V2
    from battle_v2 import PokemonInstance, PlayerState
    
    print("Testing MCTS with Value Network...")
    
    # Create game state
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
    
    # Create agent (will use random network if not trained)
    agent = create_mcts_with_value_net(simulations=100, player_id=1)
    
    print("\nChoosing action with value network MCTS (100 sims)...")
    action = agent.choose_action(state, 1)
    print(f"Selected action: {action}")
    print("\nValue network MCTS working!")

