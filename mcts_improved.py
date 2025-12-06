"""
Improved MCTS Agent with:
1. Evaluation function (HP-based heuristic)
2. Depth-limited rollouts
3. Better opponent modeling (assumes greedy opponent)
4. Minimax-style action selection
"""

import math
import random
from typing import Dict, Tuple, Optional, List
from battle import (
    BattleState, ActionType, step, legal_actions_for_player, 
    calculate_damage, get_type_multiplier
)

def evaluate_position(state: BattleState, for_player: int) -> float:
    """
    Evaluate a position from a player's perspective.
    Returns value in range [0, 1] where 1 is winning, 0 is losing.
    """
    if state.terminal:
        if state.winner == for_player:
            return 1.0
        elif state.winner is None:
            return 0.5
        else:
            return 0.0
    
    my_state = state.player1 if for_player == 1 else state.player2
    opp_state = state.player2 if for_player == 1 else state.player1
    
    # Calculate total HP
    my_total_hp = sum(p.current_hp for p in my_state.team)
    opp_total_hp = sum(p.current_hp for p in opp_state.team)
    
    # Count alive Pokémon (heavily weighted)
    my_alive = sum(1 for p in my_state.team if not p.fainted)
    opp_alive = sum(1 for p in opp_state.team if not p.fainted)
    
    # Type advantage of active Pokémon
    my_active = my_state.team[my_state.active_index]
    opp_active = opp_state.team[opp_state.active_index]
    
    type_advantage = 0.0
    if not my_active.fainted and not opp_active.fainted:
        # Check if we have type advantage
        for move in my_active.spec.moves:
            multiplier = get_type_multiplier(move.type, opp_active.spec.type)
            if multiplier > 1.5:
                type_advantage += 0.05
                
        # Check if opponent has type advantage
        for move in opp_active.spec.moves:
            multiplier = get_type_multiplier(move.type, my_active.spec.type)
            if multiplier > 1.5:
                type_advantage -= 0.05
    
    # Weighted evaluation
    # Alive count is most important (30% each)
    alive_score = (my_alive - opp_alive) / 6.0  # Range: [-1, 1]
    
    # HP difference (30%)
    total_hp = my_total_hp + opp_total_hp
    if total_hp > 0:
        hp_score = (my_total_hp - opp_total_hp) / total_hp  # Range: [-1, 1]
    else:
        hp_score = 0.0
    
    # Combine
    raw_score = 0.5 + 0.3 * alive_score + 0.3 * hp_score + type_advantage
    
    # Clamp to [0, 1]
    return max(0.0, min(1.0, raw_score))


def greedy_action(state: BattleState, player_id: int) -> ActionType:
    """Choose a greedy action (max immediate damage)."""
    legal = legal_actions_for_player(state, player_id)
    
    attacks = [a for a in legal if a in (ActionType.USE_MOVE_1, ActionType.USE_MOVE_2)]
    switches = [a for a in legal if a not in attacks]
    
    if not attacks:
        return random.choice(switches) if switches else legal[0]
        
    my_state = state.player1 if player_id == 1 else state.player2
    opp_state = state.player2 if player_id == 1 else state.player1
    
    my_active = my_state.team[my_state.active_index]
    opp_active = opp_state.team[opp_state.active_index]
    
    best_action = None
    max_damage = -1
    
    for action in attacks:
        move_idx = 0 if action == ActionType.USE_MOVE_1 else 1
        move = my_active.spec.moves[move_idx]
        dmg = calculate_damage(move, my_active, opp_active)
        if dmg > max_damage:
            max_damage = dmg
            best_action = action
            
    return best_action if best_action else legal[0]


class MCTSNodeImproved:
    def __init__(self, state: BattleState, parent: Optional['MCTSNodeImproved'] = None, 
                 my_player: int = 1):
        self.state = state
        self.parent = parent
        self.my_player = my_player  # Which player we're optimizing for
        self.children: Dict[Tuple[ActionType, ActionType], 'MCTSNodeImproved'] = {}
        
        # Statistics
        self.visits = 0
        self.value_sum = 0.0  # Sum of values from my_player's perspective
        
    def is_fully_expanded(self) -> bool:
        if self.state.terminal:
            return True
            
        legal_p1 = legal_actions_for_player(self.state, 1)
        legal_p2 = legal_actions_for_player(self.state, 2)
        total_actions = len(legal_p1) * len(legal_p2)
        return len(self.children) >= total_actions
    
    def is_terminal(self) -> bool:
        return self.state.terminal
    
    def get_untried_action(self) -> Optional[Tuple[ActionType, ActionType]]:
        legal_p1 = legal_actions_for_player(self.state, 1)
        legal_p2 = legal_actions_for_player(self.state, 2)
        all_joint_actions = [(a1, a2) for a1 in legal_p1 for a2 in legal_p2]
        untried = [ja for ja in all_joint_actions if ja not in self.children]
        return random.choice(untried) if untried else None
    
    def best_child(self, exploration_weight: float = math.sqrt(2)) -> 'MCTSNodeImproved':
        """Select best child using UCB1."""
        best_score = -float('inf')
        best_child = None
        
        for child in self.children.values():
            if child.visits == 0:
                return child
            
            # UCB1
            avg_value = child.value_sum / child.visits
            exploration = exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            ucb_score = avg_value + exploration
            
            if ucb_score > best_score:
                best_score = ucb_score
                best_child = child
        
        return best_child
    
    def expand(self, joint_action: Tuple[ActionType, ActionType]) -> 'MCTSNodeImproved':
        new_state = step(self.state, joint_action[0], joint_action[1])
        child = MCTSNodeImproved(new_state, parent=self, my_player=self.my_player)
        self.children[joint_action] = child
        return child


class ImprovedMCTSAgent:
    def __init__(self, simulations_per_move: int = 1000, player_id: int = 1,
                 rollout_depth: int = 8):
        """
        Args:
            simulations_per_move: Number of MCTS simulations
            player_id: Which player this agent is
            rollout_depth: Max depth for rollouts before using evaluation
        """
        self.simulations_per_move = simulations_per_move
        self.player_id = player_id
        self.rollout_depth = rollout_depth
    
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        """Choose best action using improved MCTS."""
        root = MCTSNodeImproved(state, my_player=player_id)
        
        # Run simulations
        for _ in range(self.simulations_per_move):
            self._simulate(root)
        
        # Use minimax-style selection: For each of our actions,
        # find the worst-case value assuming opponent plays best response
        legal_actions = legal_actions_for_player(state, player_id)
        opp_player = 2 if player_id == 1 else 1
        legal_opp_actions = legal_actions_for_player(state, opp_player)
        
        best_action = None
        best_value = -float('inf')
        
        for my_action in legal_actions:
            # For this action, find worst case across opponent responses
            worst_value = float('inf')
            total_visits = 0
            
            for opp_action in legal_opp_actions:
                if player_id == 1:
                    joint_action = (my_action, opp_action)
                else:
                    joint_action = (opp_action, my_action)
                
                if joint_action in root.children:
                    child = root.children[joint_action]
                    if child.visits > 0:
                        child_value = child.value_sum / child.visits
                        worst_value = min(worst_value, child_value)
                        total_visits += child.visits
            
            # If we have data for this action, use worst-case value
            if total_visits > 0 and worst_value < float('inf'):
                # Weight by visit count (more visited = more reliable)
                if worst_value > best_value or (worst_value == best_value and total_visits > 0):
                    best_value = worst_value
                    best_action = my_action
        
        # Fallback: pick most visited action
        if best_action is None:
            action_visits = {}
            for my_action in legal_actions:
                visits = 0
                for opp_action in legal_opp_actions:
                    if player_id == 1:
                        joint_action = (my_action, opp_action)
                    else:
                        joint_action = (opp_action, my_action)
                    if joint_action in root.children:
                        visits += root.children[joint_action].visits
                action_visits[my_action] = visits
            
            best_action = max(legal_actions, key=lambda a: action_visits.get(a, 0))
        
        return best_action
    
    def _simulate(self, node: MCTSNodeImproved) -> float:
        """Run one MCTS simulation."""
        # Selection
        current = node
        while not current.is_terminal() and current.is_fully_expanded():
            current = current.best_child()
        
        # Expansion
        if not current.is_terminal():
            untried = current.get_untried_action()
            if untried:
                current = current.expand(untried)
        
        # Evaluation (depth-limited rollout + heuristic)
        value = self._evaluate(current.state, depth=0)
        
        # Backpropagation
        while current is not None:
            current.visits += 1
            current.value_sum += value
            current = current.parent
        
        return value
    
    def _evaluate(self, state: BattleState, depth: int) -> float:
        """Evaluate position with depth-limited rollout."""
        if state.terminal:
            return evaluate_position(state, self.player_id)
        
        if depth >= self.rollout_depth:
            # Use heuristic evaluation
            return evaluate_position(state, self.player_id)
        
        # One-step greedy rollout
        a1 = greedy_action(state, 1)
        a2 = greedy_action(state, 2)
        next_state = step(state, a1, a2)
        
        return self._evaluate(next_state, depth + 1)

