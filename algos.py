from GameState import *

## This file contains the implementation of the Three required algorithms for the assignment.
## Minimax,depth-limited minimax, and alpha-beta pruning.



def minimax(state: GameState, depth: int = None) -> tuple[int, tuple[str, str], int]:
    node_count= 1

    if state.is_done() or (depth is not None and depth <= 0):
        return (state.get_util(), None, node_count)  # Return the evaluation score 
    
    best_action = None
    best_action_score = float('inf') if state.turn else float('-inf')
    

    for action in state.get_possible_actions():
        new_state = state.apply_action(action)
        score, _ ,child_count= minimax(new_state, depth - 1 if depth is not None else None)
        node_count += child_count

        if state.turn:  # Attacker's turn (minimizing defender)
            if score < best_action_score:
                best_action_score = score
                best_action = action

        else:  # Defender's turn (maximizing defender)
            if score > best_action_score:
                best_action_score = score
                best_action = action
    return (best_action_score, best_action,node_count)

def alpha_beta(state: GameState,depth: int = None, alpha: float = float('-inf'), beta: float = float('inf')) -> tuple[int, tuple[str, str],int]:
    node_count= 1
    

    if state.is_done() or (depth is not None and depth <= 0):
        return (state.get_util(), None, node_count)  # Return the evaluation score 
    
    best_action = None
    best_action_score = float('inf') if state.turn else float('-inf')


    for action in state.get_possible_actions():
        new_state = state.apply_action(action)
        score, _,child_count = alpha_beta(new_state, depth - 1 if depth is not None else None, alpha, beta)
        node_count += child_count

        if state.turn:  # Attacker's turn (minimizing defender)
            if score < best_action_score:
                best_action_score = score
                best_action = action
            beta = min(beta, best_action_score)
            if beta <= alpha:
                break  # Alpha-beta pruning

        else:  # Defender's turn (maximizing defender)
            if score > best_action_score:
                best_action_score = score
                best_action = action
            alpha = max(alpha, best_action_score)
            if beta <= alpha:
                break  # Alpha-beta pruning

    return (best_action_score, best_action,node_count)