from  hosts import Host
from GameState import GameState


def create_assignment_game_state_list() -> GameState:
    # 1. Create all hosts with empty connection lists first
    hosts = [
        Host(id="H0", value=0, connections=[]),    # index 0
        Host(id="H1", value=10, connections=[]),   # index 1
        Host(id="H2", value=15, connections=[]),   # index 2
        Host(id="H3", value=30, connections=[]),   # index 3
        Host(id="H4", value=10, connections=[]),   # index 4
        Host(id="H5", value=100, connections=[]),  # index 5
        Host(id="H6", value=60, connections=[]),   # index 6
        Host(id="H7", value=25, connections=[]),   # index 7
        Host(id="H8", value=20, connections=[]),   # index 8
        Host(id="H9", value=40, connections=[])    # index 9
    ]

    # 2. Connect hosts using the object references based on the assignment table
    hosts[0].connections = [hosts[1], hosts[2]]          # H0 -> H1, H2
    hosts[1].connections = [hosts[0], hosts[3], hosts[4]]# H1 -> H0, H3, H4
    hosts[2].connections = [hosts[0], hosts[4]]          # H2 -> H0, H4
    hosts[3].connections = [hosts[1], hosts[5], hosts[6]]# H3 -> H1, H5, H6
    hosts[4].connections = [hosts[1], hosts[2], hosts[6]]# H4 -> H1, H2, H6
    hosts[5].connections = [hosts[3], hosts[7]]          # H5 -> H3, H7
    hosts[6].connections = [hosts[3], hosts[4], hosts[7]]# H6 -> H3, H4, H7
    hosts[7].connections = [hosts[5], hosts[6], hosts[8]]# H7 -> H5, H6, H8
    hosts[8].connections = [hosts[7], hosts[9]]          # H8 -> H7, H9
    hosts[9].connections = [hosts[8]]                    # H9 -> H8

    # 3. Initialize and return the GameState
    game_state = GameState(hosts=hosts, start_host=hosts[0], end_host=hosts[5])
    return game_state

def  main():

    game_state = create_assignment_game_state_list()


main()