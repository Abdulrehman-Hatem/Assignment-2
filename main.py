from  hosts import Host
from GameState import GameState
from algos import minimax
from tests import run_minmax_test, run_alpha_beta_depth_test,run_task_1_tests


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

  
def get_task():
    print("="*60)
    print("Enter the number corresponding to the task you want to run:")
    print("0--Exit")
    print("1--Demonstrate Legal Moves, Patching, and Winning")
    print("2--Run Minimax Algorithm (full depth -- SLOW)")
    print("3--Run Minimax Algorithm with Depth Limit")
    print("4--Run Alpha-Beta Pruning Algorithm")
    print("5--Run Alpha-Beta Pruning Algorithm with Depth Limit")
    x = input("Enter your choice: ")
    print("="*60)
    return x



def  main():

    game_state = create_assignment_game_state_list()


    while True:
        x=get_task()
  
        if not x.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        
        x = int(x)
        match x:
            case 0:
                return 
            
            case 1:
                run_task_1_tests(game_state.copy())

            case 2:
                run_minmax_test(game_state.copy())

            case 3:
                y= input("Enter depth limit for Minimax: ")
                y = int(y) if y.isdigit() else 3
                run_minmax_test(game_state.copy(), y)

            case 4:
                run_alpha_beta_depth_test(game_state.copy())

            case 5:
                y= input("Enter depth limit for Alpha-Beta Pruning: ")
                y = int(y) if y.isdigit() else 3
                run_alpha_beta_depth_test(game_state.copy(), y)

            case _:
                print("Invalid choice. Please try again.")


    
    
if __name__ == "__main__":
    main()