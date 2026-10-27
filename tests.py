from GameState import GameState
from algos import minimax, alpha_beta

import time

#this file contains the test cases for the assignment.
#it will test the game state class manually
#it will then test the minimax and alpha-beta pruning algorithms on the game state class


#helper function to print results
def print_results(game_state: GameState, time: float, total_nodes_evaluated: int):
    print("\nFinal State after Algorithm:")
    print(game_state)
    print("="*44+"\n")
    print(f"- Game ended after {game_state.ply_count} plies.")
    print(f" The data was {'exfiltrated' if game_state.exfiltrated else 'not exfiltrated'}.")
    print(f"- Final Utility (Defender perspective): {game_state.get_util()}")
    print(f"- Total Time Taken: {time:.4f} seconds")
    print(f"- Number of nodes evaluated: {total_nodes_evaluated}")
    print("="*44+"\n")
    temp = input("Press Enter to continue...")


def run_task_1_tests(state: GameState):
    print("\n" + "="*44)
    print("TEST CASE 1: Demonstrating Legal Moves")
    print("="*44)
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

    temp = input("Press Enter to continue to Patching demonstration...")

    print("\n" + "="*44)
    print("TEST CASE 2: Demonstrating Patching")
    print("="*44)
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

    temp = input("Press Enter to continue to Winning demonstration...")

    print("\n" + "="*44)
    print("TEST CASE 3: Demonstrating Winning (Exfiltration)")
    print("="*44)
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

    print("="*44)
    print("\nFinal Game State:")
    print(state_3)
    print( "="*44+"\n")
    print(f"- Did game end? (is_done): {state_3.is_done()}")
    print(f"- Was data exfiltrated?: {state_3.exfiltrated}")
    print(f"- Final Utility (Defender perspective): {state_3.get_util()}")
    print("\n" + "="*44)
    temp = input("Press Enter to continue...")

def run_minmax_test(state: GameState, depth: int = None):

    print("\n" + "="*44)

    if depth is None:
        print("--Minimax Algorithm--")
    else:
        print(f"--Depth-Limited Minimax Algorithm (Depth: {depth})--")

    print("="*44)
    
    # Start fresh game
    state_copy = state.copy()

    #start timer and node count
    total_nodes_evaluated = 0
    timer_start = time.time()

    # Run Depth-Limited Minimax till game ends
    i=1
    while not state_copy.is_done():
        score, best_action, node_count = minimax(state_copy, depth)
        print(f"- ply {i}:Action: {best_action}, Nodes Evaluated: {node_count}")
        state_copy = state_copy.apply_action(best_action)
        total_nodes_evaluated += node_count
        i += 1

    timer_end = time.time()
    print_results(state_copy, timer_end - timer_start, total_nodes_evaluated)

def run_alpha_beta_depth_test(state: GameState, depth: int = None):
    print("\n" + "="*44)
    if depth is None:
        print("--Alpha-Beta Pruning Algorithm--")
    else:
        print(f"--Depth-Limited Alpha-Beta Pruning Algorithm (Depth: {depth})--")
    print("="*44)
    
    # Start fresh game
    state_copy = state.copy()

    #start timer and node count
    timer_start = time.time()
    total_nodes_evaluated = 0

    # Run Alpha-Beta Pruning till game ends
    i = 1
    while not state_copy.is_done():
        score, best_action, node_count = alpha_beta(state_copy, depth)   
        print(f"- ply {i}:Action: {best_action}, Nodes Evaluated: {node_count}")
        state_copy = state_copy.apply_action(best_action)
        total_nodes_evaluated += node_count
        i += 1

    timer_end = time.time()

    print_results(state_copy, timer_end - timer_start, total_nodes_evaluated)
