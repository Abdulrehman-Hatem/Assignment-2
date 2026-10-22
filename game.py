from hosts.py import *

class GameState:
    def __init__(self, hosts:list,turn:bool = True,ply_count:int = 0, defender_budget:int = 10, attacker_zeroday:bool = True):
        self.hosts = hosts
        self.turn = turn  # attacker's turn if True, defender's turn if False
        self.ply_count = ply_count
        self.defender_budget = defender_budget
        self.attacker_zeroday = attacker_zeroday