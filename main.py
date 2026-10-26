from  hosts import Host
from GameState import GameState
from algos import minimax


def create_assignment_game_state_list() -> GameState:
    # 1. Create all hosts with empty connection lists first
    hosts = [
        Host(id="H0", value=0, connections=["H1", "H2"]),    # index 0
        Host(id="H1", value=10, connections=["H0", "H3", "H4"]),   # index 1
        Host(id="H2", value=15, connections=["H0", "H4"]),   # index 2
        Host(id="H3", value=30, connections=["H1", "H5", "H6"]),   # index 3
        Host(id="H4", value=10, connections=["H1", "H2", "H6"]),   # index 4
        Host(id="H5", value=100, connections=["H3", "H7"]),  # index 5
        Host(id="H6", value=60, connections=["H3", "H4", "H7"]),   # index 6
        Host(id="H7", value=25, connections=["H5", "H6", "H8"]),   # index 7
        Host(id="H8", value=20, connections=["H7", "H9"]),   # index 8
        Host(id="H9", value=40, connections=["H8"])    # index 9
    ]

    # 2. Initialize and return the GameState
    game_state = GameState(hosts=hosts, start_host='H0', end_host='H5')
    return game_state


def run_task_1_tests():
    print("\n" + "="*60)
    print("TEST CASE 1: Demonstrating Legal Moves")
    print("="*60)
    # Start fresh game
    state_1 = create_assignment_game_state_list()
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
    state_2 = create_assignment_game_state_list()
    
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
    state_3 = create_assignment_game_state_list()
    
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


  

def  main():


    #run_task_1_tests()

    game_state = create_assignment_game_state_list()

    #minmax test
    while not game_state.is_done():
        print("\n" + "="*60)
        print(f"Current Game State (Turn: {'Attacker' if game_state.turn else 'Defender'}):")
        print(game_state)
        
       
        score, best_action = minimax(game_state, depth=3)  
        print(f"- Best action determined by Minimax: {best_action} with score: {score}")
        
        # Apply the best action to the game state
        game_state = game_state.apply_action(best_action)

    

main()