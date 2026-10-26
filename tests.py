from GameState import GameState
from algos import minimax, alpha_beta
from hosts import Host
import time

#this file contains the test cases for the assignment.
#it will test the game state class manually
#it will then test the minimax and alpha-beta pruning algorithms on the game state class


#helper function to print results
def print_results(game_state: GameState, start_time: float, end_time: float):
    print("\nFinal State after Algorithm:")
    print(game_state)
    print(f"- Did game end? (is_done): {game_state.is_done()}")
    print(f"- Was data exfiltrated?: {game_state.exfiltrated}")
    print(f"- Final Utility (Defender perspective): {game_state.get_util()}")
    print(f"- Total Time Taken: {end_time - start_time:.4f} seconds")


def run_task_1_tests(state: GameState):
    print("\n" + "="*60)
    print("TEST CASE 1: Demonstrating Legal Moves")
    print("="*60)
    # Start fresh game
    state_1 = state.copy()
    print("Initial State (Attacker's Turn):")
    print(state_1)
    
    attacker_moves = state_1.get_possible_actions()
    print(f"- Attacker's initial legal moves: \n{attacker_moves}\n")
    
    # Attacker passes to show Defender's moves
    state_1 = state_1.apply_action(("pass", None))
    defender_moves = state_1.get_possible_actions()
    print(f"- Defender's initial legal moves (Budget: {state_1.defender_budget}): \n{defender_moves}\n")


    print("\n" + "="*60)
    print("TEST CASE 2: Demonstrating Patching")
    print("="*60)
    state_2 = state.copy()
    
    # Attacker passes
    state_2 = state_2.apply_action(("pass", None))
    
    # Defender patches H1
    print("- Defender plays: ('patch', 'H1')")
    state_2 = state_2.apply_action(("patch", "H1"))
    
    print("\nState after Patching (Notice H1 is Patched and Budget is 8):")
    print(state_2)
    
    # Check Attacker's moves now
    new_attacker_moves = state_2.get_possible_actions()
    print(f"- Attacker's moves after H1 is patched (Notice 'zeroday' instead of 'exploit' for H1): \n{new_attacker_moves}\n")


    print("\n" + "="*60)
    print("TEST CASE 3: Demonstrating Winning (Exfiltration)")
    print("="*60)
    state_3 = state.copy()
    
    # Sequence of moves leading to Exfiltration at H5
    move_sequence = [
        ("exploit", "H1"),   # Attacker Ply 1
        ("pass", None),      # Defender Ply 2
        ("exploit", "H3"),   # Attacker Ply 3
        ("pass", None),      # Defender Ply 4
        ("exploit", "H5"),   # Attacker Ply 5
        ("pass", None),      # Defender Ply 6
        ("exfiltrate", "H5") # Attacker Ply 7 (Ends game)
    ]
    
    for move in move_sequence:
        print(f"Applying move: {move}")
        state_3 = state_3.apply_action(move)

    print("="*60)
    print("\nFinal Game State:")
    print(state_3)
    print( "="*60+"\n")
    print(f"- Did game end? (is_done): {state_3.is_done()}")
    print(f"- Was data exfiltrated?: {state_3.exfiltrated}")
    print(f"- Final Utility (Defender perspective): {state_3.get_util()}")
    print("\n" + "="*60)

def run_minmax_test(state: GameState, depth: int = None):
    print("\n" + "="*60)
    if depth is None:
        print("TEST CASE 4: Demonstrating Minimax Algorithm")
    else:
        print(f"TEST CASE 5: Demonstrating Depth-Limited Minimax Algorithm (Depth: {depth})")
    print("="*60)
    
    # Start fresh game
    state_copy = state.copy()
    print("Initial State (Attacker's Turn):")
    print(state_copy)

    timer_start = time.time()

    # Run Depth-Limited Minimax till game ends
    while not state_copy.is_done():
        score, best_action, node_count = minimax(state_copy, depth)
        print(f"- Depth-Limited Minimax Result: Best Action: {best_action}, Score: {score}, Nodes Evaluated: {node_count}")
        state_copy = state_copy.apply_action(best_action)

    timer_end = time.time()

    print_results(state_copy, timer_start, timer_end)


def run_alpha_beta_depth_test(state: GameState, depth: int = None):
    print("\n" + "="*60)
    if depth is None:
        print("TEST CASE 6: Demonstrating Alpha-Beta Pruning Algorithm")
    else:
        print(f"TEST CASE 7: Demonstrating Depth-Limited Alpha-Beta Pruning Algorithm (Depth: {depth})")
    print("="*60)
    
    # Start fresh game
    state_copy = state.copy()
    print("Initial State (Attacker's Turn):")
    print(state_copy)

    timer_start = time.time()

    # Run Depth-Limited Alpha-Beta Pruning till game ends
    while not state_copy.is_done():
        score, best_action, node_count = alpha_beta(state_copy, depth)
        print(f"- Depth-Limited Alpha-Beta Result: Best Action: {best_action}, Score: {score}, Nodes Evaluated: {node_count}")
        state_copy = state_copy.apply_action(best_action)

    timer_end = time.time()

    print_results(state_copy, timer_start, timer_end)
