"""
General MCTS for Pokemon Battle V2

This is the HONEST version that doesn't assume opponent behavior.
Explores all joint actions fairly.
"""

import math
import random
from typing import Dict, Tuple, Optional, List
from battle_v2 import BattleState, ActionType, step, legal_actions_for_player, calculate_damage

def greedy_action(state: BattleState, player_id: int) -> ActionType:
    """Choose greedy action for rollouts (max expected damage)."""
    legal = legal_actions_for_player(state, player_id)
    attacks = [a for a in legal if a in (ActionType.USE_MOVE_1, ActionType.USE_MOVE_2)]
    
    if not attacks:
        return random.choice(legal) if legal else ActionType.USE_MOVE_1
    
    my_state = state.player1 if player_id == 1 else state.player2
    opp_state = state.player2 if player_id == 1 else state.player1
    my_active = my_state.team[my_state.active_index]
    opp_active = opp_state.team[opp_state.active_index]
    
    best_action = None
    max_expected = -1
    
    for action in attacks:
        move_idx = 0 if action == ActionType.USE_MOVE_1 else 1
        move = my_active.spec.moves[move_idx]
        base_dmg = calculate_damage(move, my_active, opp_active)
        
        # Expected value accounting for accuracy and recoil
        expected = base_dmg * (move.accuracy / 100)
        if move.recoil_percent > 0:
            expected -= base_dmg * (move.recoil_percent / 100) * 0.5  # Recoil penalty
        
        if expected > max_expected:
            max_expected = expected
            best_action = action
    
    return best_action if best_action else legal[0]


class MCTSNode:
    """MCTS node that explores ALL joint actions (no opponent assumptions)."""
    
    def __init__(self, state: BattleState, parent: Optional['MCTSNode'] = None,
                 my_player: int = 1):
        self.state = state
        self.parent = parent
        self.my_player = my_player
        
        # Children indexed by JOINT actions (both players)
        self.children: Dict[Tuple[ActionType, ActionType], 'MCTSNode'] = {}
        
        self.visits = 0
        self.wins = 0
        self.draws = 0
    
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
    
    def best_child(self, exploration_weight: float = 1.414) -> 'MCTSNode':
        best_score = -float('inf')
        best_child = None
        
        for child in self.children.values():
            if child.visits == 0:
                return child
            
            win_rate = child.wins / child.visits
            exploration = exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            ucb = win_rate + exploration
            
            if ucb > best_score:
                best_score = ucb
                best_child = child
        
        return best_child
    
    def expand(self, joint_action: Tuple[ActionType, ActionType]) -> 'MCTSNode':
        """Expand with joint action (fair version - no assumptions)."""
        new_state = step(self.state, joint_action[0], joint_action[1])
        child = MCTSNode(new_state, parent=self, my_player=self.my_player)
        self.children[joint_action] = child
        return child


class MCTSAgent:
    """
    General MCTS Agent - NO opponent modeling.
    
    This is the fair/honest version that doesn't assume opponent behavior.
    """
    
    def __init__(self, simulations_per_move: int = 1000, player_id: int = 1):
        self.simulations_per_move = simulations_per_move
        self.player_id = player_id
    
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        """
        Choose best action using MINIMAX-style selection.
        
        For each of our actions, assume opponent plays their best response.
        Pick the action with the best worst-case outcome.
        
        This fixes the bug where naive averaging gets worse with more simulations!
        """
        root = MCTSNode(state, my_player=player_id)
        
        # Run simulations
        for _ in range(self.simulations_per_move):
            self._simulate(root)
        
        legal_actions = legal_actions_for_player(state, player_id)
        opp_player = 2 if player_id == 1 else 1
        legal_opp = legal_actions_for_player(state, opp_player)
        
        best_action = None
        best_worst_case = -float('inf')
        
        # For each of MY actions, find the worst-case outcome
        # (i.e., opponent's best response)
        for my_action in legal_actions:
            worst_case_value = float('inf')
            total_visits = 0
            
            # Check all opponent responses
            for opp_action in legal_opp:
                # Construct joint action
                if player_id == 1:
                    joint = (my_action, opp_action)
                else:
                    joint = (opp_action, my_action)
                
                if joint in root.children:
                    child = root.children[joint]
                    if child.visits > 0:
                        # Calculate win rate from my perspective
                        if player_id == 1:
                            win_rate = child.wins / child.visits
                        else:
                            win_rate = (child.visits - child.wins) / child.visits
                        
                        # Track worst case (best for opponent)
                        worst_case_value = min(worst_case_value, win_rate)
                        total_visits += child.visits
            
            # If we explored this action at all, consider it
            if total_visits > 0 and worst_case_value < float('inf'):
                # Pick action with best worst-case outcome
                if worst_case_value > best_worst_case:
                    best_worst_case = worst_case_value
                    best_action = my_action
        
        # Fallback: pick most-visited action
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
    
    def _simulate(self, node: MCTSNode) -> float:
        """Run one MCTS simulation."""
        # Selection
        current = node
        while not current.state.terminal and current.is_fully_expanded():
            current = current.best_child()
        
        # Expansion
        if not current.state.terminal:
            untried = current.get_untried_action()
            if untried:
                current = current.expand(untried)
        
        # Rollout
        result = self._rollout(current.state)
        
        # Backpropagation
        while current is not None:
            current.visits += 1
            if result == 1:
                current.wins += 1
            elif result == 0.5:
                current.draws += 1
            current = current.parent
        
        return result
    
    def _rollout(self, state: BattleState) -> float:
        """Rollout with random play for both players (unbiased)."""
        current = state.clone()
        
        while not current.terminal:
            legal_p1 = legal_actions_for_player(current, 1)
            legal_p2 = legal_actions_for_player(current, 2)
            a1 = random.choice(legal_p1)
            a2 = random.choice(legal_p2)
            current = step(current, a1, a2)
        
        if current.winner == self.player_id:
            return 1.0
        elif current.winner is None:
            return 0.5
        else:
            return 0.0

