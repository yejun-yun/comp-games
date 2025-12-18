import math
import random
import sys
import os
from typing import Dict, Tuple, Optional, List, Set
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from battle_v2 import BattleState, ActionType, step, legal_actions_for_player, calculate_damage


class RAVENode:
    def __init__(self, state: BattleState, parent: Optional['RAVENode'] = None,
                 my_player: int = 1):
        self.state = state
        self.parent = parent
        self.my_player = my_player
        self.children: Dict[Tuple[ActionType, ActionType], 'RAVENode'] = {}
        self.visits = 0
        self.wins = 0
        self.amaf_stats: Dict[Tuple[int, ActionType], List[int]] = defaultdict(lambda: [0, 0])

    def is_fully_expanded(self) -> bool:
        if self.state.terminal:
            return True
        legal_p1 = legal_actions_for_player(self.state, 1)
        legal_p2 = legal_actions_for_player(self.state, 2)
        return len(self.children) >= len(legal_p1) * len(legal_p2)

    def get_untried_action(self) -> Optional[Tuple[ActionType, ActionType]]:
        legal_p1 = legal_actions_for_player(self.state, 1)
        legal_p2 = legal_actions_for_player(self.state, 2)
        all_joint = [(a1, a2) for a1 in legal_p1 for a2 in legal_p2]
        untried = [ja for ja in all_joint if ja not in self.children]
        return random.choice(untried) if untried else None

    def expand(self, joint_action: Tuple[ActionType, ActionType]) -> 'RAVENode':
        new_state = step(self.state, joint_action[0], joint_action[1])
        child = RAVENode(new_state, parent=self, my_player=self.my_player)
        self.children[joint_action] = child
        return child


class MCTSRAVEAgent:
    def __init__(self, simulations_per_move: int = 1000, player_id: int = 1,
                 rave_k: float = 500, exploration_weight: float = 1.414):
        self.simulations_per_move = simulations_per_move
        self.player_id = player_id
        self.rave_k = rave_k
        self.exploration_weight = exploration_weight

    def choose_action(self, state: BattleState, player_id: int) -> ActionType:
        root = RAVENode(state, my_player=player_id)

        for _ in range(self.simulations_per_move):
            self._simulate(root)

        legal_actions = legal_actions_for_player(state, player_id)
        opp_player = 2 if player_id == 1 else 1
        legal_opp = legal_actions_for_player(state, opp_player)

        best_action = None
        best_worst_case = -float('inf')

        for my_action in legal_actions:
            worst_case_value = float('inf')
            total_visits = 0

            for opp_action in legal_opp:
                if player_id == 1:
                    joint = (my_action, opp_action)
                else:
                    joint = (opp_action, my_action)

                if joint in root.children:
                    child = root.children[joint]
                    if child.visits > 0:
                        if player_id == 1:
                            win_rate = child.wins / child.visits
                        else:
                            win_rate = (child.visits - child.wins) / child.visits

                        worst_case_value = min(worst_case_value, win_rate)
                        total_visits += child.visits

            if total_visits > 0 and worst_case_value < float('inf'):
                if worst_case_value > best_worst_case:
                    best_worst_case = worst_case_value
                    best_action = my_action

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

    def _get_rave_beta(self, node_visits: int) -> float:
        return math.sqrt(self.rave_k / (3 * node_visits + self.rave_k))

    def _best_child_rave(self, node: RAVENode) -> 'RAVENode':
        best_score = -float('inf')
        best_child = None

        for joint_action, child in node.children.items():
            if child.visits == 0:
                return child

            uct_value = child.wins / child.visits
            exploration = self.exploration_weight * math.sqrt(math.log(node.visits) / child.visits)

            a1, a2 = joint_action
            my_action = a1 if node.my_player == 1 else a2
            amaf = node.amaf_stats[(node.my_player, my_action)]

            if amaf[0] > 0:
                if node.my_player == 1:
                    amaf_value = amaf[1] / amaf[0]
                else:
                    amaf_value = (amaf[0] - amaf[1]) / amaf[0]

                beta = self._get_rave_beta(child.visits)
                combined_value = (1 - beta) * uct_value + beta * amaf_value
                score = combined_value + exploration
            else:
                score = uct_value + exploration

            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def _simulate(self, node: RAVENode) -> float:
        actions_played: List[Tuple[int, ActionType]] = []
        path: List[Tuple[RAVENode, Optional[Tuple[ActionType, ActionType]]]] = []

        current = node
        while not current.state.terminal and current.is_fully_expanded():
            best_child = self._best_child_rave(current)
            joint_action = None
            for ja, child in current.children.items():
                if child is best_child:
                    joint_action = ja
                    break

            if joint_action:
                actions_played.append((1, joint_action[0]))
                actions_played.append((2, joint_action[1]))
                path.append((current, joint_action))

            current = best_child

        if not current.state.terminal:
            untried = current.get_untried_action()
            if untried:
                path.append((current, untried))
                actions_played.append((1, untried[0]))
                actions_played.append((2, untried[1]))
                current = current.expand(untried)

        result, rollout_actions = self._rollout_with_actions(current.state)
        actions_played.extend(rollout_actions)

        backprop_node = current
        while backprop_node is not None:
            backprop_node.visits += 1
            if result == 1:
                backprop_node.wins += 1
            elif result == 0.5:
                backprop_node.wins += 0.5
            backprop_node = backprop_node.parent

        for i, (path_node, _) in enumerate(path):
            actions_after = actions_played[2*(i+1):]
            seen_actions: Set[Tuple[int, ActionType]] = set()
            for player_id, action in actions_after:
                if (player_id, action) not in seen_actions:
                    seen_actions.add((player_id, action))
                    path_node.amaf_stats[(player_id, action)][0] += 1
                    if result == 1:
                        path_node.amaf_stats[(player_id, action)][1] += 1
                    elif result == 0.5:
                        path_node.amaf_stats[(player_id, action)][1] += 0.5

        return result

    def _rollout_with_actions(self, state: BattleState) -> Tuple[float, List[Tuple[int, ActionType]]]:
        current = state.clone()
        actions_played = []

        while not current.terminal:
            legal_p1 = legal_actions_for_player(current, 1)
            legal_p2 = legal_actions_for_player(current, 2)
            a1 = random.choice(legal_p1)
            a2 = random.choice(legal_p2)

            actions_played.append((1, a1))
            actions_played.append((2, a2))

            current = step(current, a1, a2)

        if current.winner == 1:
            return 1.0, actions_played
        elif current.winner == 2:
            return 0.0, actions_played
        else:
            return 0.5, actions_played


class MCTSRAVEGreedyAgent(MCTSRAVEAgent):
    def _greedy_action(self, state: BattleState, player_id: int) -> ActionType:
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

            expected = base_dmg * (move.accuracy / 100)
            if move.recoil_percent > 0:
                expected -= base_dmg * (move.recoil_percent / 100) * 0.5

            if expected > max_expected:
                max_expected = expected
                best_action = action

        return best_action if best_action else legal[0]

    def _rollout_with_actions(self, state: BattleState) -> Tuple[float, List[Tuple[int, ActionType]]]:
        current = state.clone()
        actions_played = []

        while not current.terminal:
            a1 = self._greedy_action(current, 1)
            a2 = self._greedy_action(current, 2)

            actions_played.append((1, a1))
            actions_played.append((2, a2))

            current = step(current, a1, a2)

        if current.winner == 1:
            return 1.0, actions_played
        elif current.winner == 2:
            return 0.0, actions_played
        else:
            return 0.5, actions_played
