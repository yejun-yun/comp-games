"""
MCTS with Explicit Opponent Modeling

Key insight: If opponent plays greedy deterministically, we don't need to explore
all joint actions - just assume they play greedy and build our tree accordingly!
"""

import math
import random
from typing import Dict, Optional, List
from battle import (
    BattleState, ActionType, step, legal_actions_for_player, 
    calculate_damage
)

def greedy_action(state: BattleState, player_id: int) -> ActionType:
    """Choose greedy action (max immediate damage)."""
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


class MCTSNodeOpponentModel:
    def __init__(self, state: BattleState, parent: Optional['MCTSNodeOpponentModel'] = None,
                 my_player: int = 1, opp_player: int = 2):
        self.state = state
        self.parent = parent
        self.my_player = my_player
        self.opp_player = opp_player
        
        # Children indexed by MY action only (opponent assumed greedy)
        self.children: Dict[ActionType, 'MCTSNodeOpponentModel'] = {}
        
        self.visits = 0
        self.wins = 0
        self.draws = 0
    
    def is_fully_expanded(self) -> bool:
        if self.state.terminal:
            return True
        my_legal = legal_actions_for_player(self.state, self.my_player)
        return len(self.children) >= len(my_legal)
    
    def get_untried_action(self) -> Optional[ActionType]:
        my_legal = legal_actions_for_player(self.state, self.my_player)
        untried = [a for a in my_legal if a not in self.children]
        return random.choice(untried) if untried else None
    
    def best_child(self, exploration_weight: float = 1.414) -> 'MCTSNodeOpponentModel':
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
    
    def expand(self, my_action: ActionType) -> 'MCTSNodeOpponentModel':
        """Expand by assuming opponent plays greedy."""
        opp_action = greedy_action(self.state, self.opp_player)
        
        if self.my_player == 1:
            new_state = step(self.state, my_action, opp_action)
        else:
            new_state = step(self.state, opp_action, my_action)
        
        child = MCTSNodeOpponentModel(new_state, parent=self, 
                                      my_player=self.my_player,
                                      opp_player=self.opp_player)
        self.children[my_action] = child
        return child


class OpponentModelMCTSAgent:
    def __init__(self, simulations_per_move: int = 1000, player_id: int = 1):
        self.simulations_per_move = simulations_per_move
        self.player_id = player_id
        self.opp_player = 2 if player_id == 1 else 1
    
    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        """Choose best action assuming opponent plays greedy."""
        root = MCTSNodeOpponentModel(state, my_player=player_id, 
                                      opp_player=self.opp_player)
        
        # Run simulations
        for _ in range(self.simulations_per_move):
            self._simulate(root)
        
        # Pick action with best win rate
        best_action = None
        best_win_rate = -1
        
        for action, child in root.children.items():
            if child.visits > 0:
                win_rate = child.wins / child.visits
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_action = action
        
        # Fallback
        if best_action is None:
            legal = legal_actions_for_player(state, player_id)
            best_action = legal[0] if legal else ActionType.USE_MOVE_1
        
        return best_action
    
    def _simulate(self, node: MCTSNodeOpponentModel) -> float:
        """Run one simulation."""
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
        """Rollout assuming both players play greedy."""
        current = state.clone()
        
        while not current.terminal:
            a1 = greedy_action(current, 1)
            a2 = greedy_action(current, 2)
            current = step(current, a1, a2)
        
        if current.winner == self.player_id:
            return 1.0
        elif current.winner is None:
            return 0.5
        else:
            return 0.0

