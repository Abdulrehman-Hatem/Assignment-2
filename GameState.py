from hosts import Host
from hosts import *
import copy

class GameState:
    def __init__(self, hosts:list,turn:bool = True,ply_count:int = 0, defender_budget:int = 10, attacker_zeroday:bool = True,exfiltrated:bool = False):
        self.hosts = hosts
        self.turn = turn  # attacker's turn if True, defender's turn if False
        self.ply_count = ply_count
        self.defender_budget = defender_budget
        self.attacker_zerodays= attacker_zeroday
        self.exfiltrated= exfiltrated

    def _get_attackable_hosts(self) -> set[str]:
        attackable_hosts = set()
        for host in self.hosts:

            if host.compromised and not host.isolated:
                for neighbor in host.get_connections_list():
                        attackable_hosts.add(neighbor)
        return attackable_hosts
            
  

    def get_possible_actions(self) -> list[tuple[str, str]]: #returns a list of possible moves  where each move is (action,target)
        actions=[]

        if self.turn:  # Attacker's turn
            attackable_hosts = self._get_attackable_hosts()
            for host in self.hosts:
                if host.id == "H0":
                    continue  # Skip the initial host, as it cannot be exploited
                
                elif host.id == "H5" and host.compromised and not host.isolated:
                    actions.append(("exfiltrate",host.id))
                    continue

                elif not host.compromised and not host.isolated:
                    # check if there is a valid path to the host 
                    if not host.id in attackable_hosts:
                        continue  # Skip this host if there is no valid path to it

                    if not host.patched:
                        actions.append(("exploit",host.id))
                    elif self.attacker_zerodays:
                        actions.append(("zeroday",host.id))


            actions.append(("pass", None))  # Attacker can always choose to pass


        else:  # Defender's turn
            for host in self.hosts:
                if host.id == "H0":
                    continue  # Skip the initial host, as it cannot be exploited
                
                if not host.compromised and not host.patched and self.defender_budget >= 2:
                    actions.append(("patch", host.id))

                if not host.isolated and self.defender_budget >= 8:
                    actions.append(("isolate", host.id))

                if host.compromised and self.defender_budget >= 5:
                    actions.append(("restore", host.id))

            actions.append(("pass", None))  # Defender can always choose to pass

        return actions

    def end_game(self):
        return

    # actions are : "exploit", "zeroday", "exfiltrate", "patch", "isolate", "restore", "pass"
    def apply_action(self, action:tuple[str, str]) -> GameState:
        new_state= copy.deepcopy(self)
        action_type ,target_id  = action

        target = next((host for host in new_state.hosts if host.id == target_id), None)


        ## happens always
        new_state.ply_count += 1
        new_state.turn = not new_state.turn  # Switch turns

        if action_type == "pass":
            return new_state
        
        ## attacker actions
        if action_type == "exploit":
            target.compromised = True
        elif action_type == "zeroday":
            target.compromised = True
            new_state.attacker_zerodays = False
        elif action_type == "exfiltrate":
            new_state.exfiltrated = True

        ## defender actions
        elif action_type == "patch":
            target.patched = True
            new_state.defender_budget -= 2
        elif action_type == "isolate":
            target.isolated = True
            new_state.defender_budget -= 8
        elif action_type == "restore":
            target.compromised = False
            target.patched = True
            new_state.defender_budget -= 5

        return new_state

    def is_terminal(self) -> bool:
        # Check if the game has ended
        if self.ply_count >= 10:
            return True
        host_h5 = next((host for host in self.hosts if host.id == "H5"), None)

        if self.exfiltrated:
            return True

        return False

    def get_util(self) -> int:
        #defender util fn , attacker util fn is just the negative of this
        x = 1 if self.exfiltrated else 0
        sum_assets = sum(host.value for host in self.hosts if host.compromised)

        return -(sum_assets)-(10-self.defender_budget)- (100 * x)
    
