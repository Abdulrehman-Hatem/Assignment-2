from hosts import Host

import copy

class GameState:
    def __init__(self, hosts:list[Host],turn:bool = True,ply_count:int = 0,start_host:Host = None,end_host:Host = None,
                  defender_budget:int = 10, attacker_zeroday:bool = True,exfiltrated:bool = False):
        self.hosts = hosts
        self.turn = turn  # attacker's turn if True, defender's turn if False
        self.start_host = start_host            # H0 always in this assignment
        self.end_host = end_host                # H5 always in this assignment
        self.ply_count = ply_count              # 10 always in this assignment
        self.defender_budget = defender_budget  # 10 always in this assignment
        self.attacker_zerodays= attacker_zeroday
        self.exfiltrated= exfiltrated

        if self.start_host is not None:
            self.start_host.compromised = True  # The initial host is always compromised at the start of the game
        
        

    #this functions returns a set of host ids that are attackable by the attacker in the current state
    def _get_attackable_hosts(self) -> set[str]:
        attackable_hosts = set() #a set is used to avoid duplicates in a simpler way

        for host in self.hosts:
            if host.compromised and not host.isolated:
                for neighbor in host.get_connections_list():
                        attackable_hosts.add(neighbor)
        return attackable_hosts
            
  
    #returns a list of possible moves  where each move is (action,target) 
    def get_possible_actions(self) -> list[tuple[str, str]]: 
        actions=[]

        if self.turn:  # Attacker's turn
            attackable_hosts = self._get_attackable_hosts()

            for host in self.hosts:
                if host.id == self.start_host.id:
                    continue  # Skip the initial host, as it cannot be exploited
                
                elif host.id == self.end_host.id and host.compromised and not host.isolated:
                    actions.append(("exfiltrate",host.id))
                    continue

                elif not host.compromised and not host.isolated:

                    # skip it if there is no path to it from any compromised host
                    if not host.id in attackable_hosts:
                        continue 

                    if not host.patched:
                        actions.append(("exploit",host.id))
                    elif self.attacker_zerodays:
                        actions.append(("zeroday",host.id))


            actions.append(("pass", None))  # Attacker can always choose to pass


        else:  # Defender's turn
            for host in self.hosts:
                if host.id == self.start_host.id:
                    continue  # Skip the initial host, as it cannot be exploited
                
                if not host.compromised and not host.patched and self.defender_budget >= 2:
                    actions.append(("patch", host.id))

                if not host.isolated and self.defender_budget >= 8:
                    actions.append(("isolate", host.id))

                if host.compromised and self.defender_budget >= 5:
                    actions.append(("restore", host.id))

            actions.append(("pass", None))  # Defender can always choose to pass

        return actions



    # actions are : "exploit", "zeroday", "exfiltrate", "patch", "isolate", "restore", "pass"
    # the function returns a new GameState object that is the result of applying the action to the current state
    # which is easier and more efficient than modifying the current state in place and reverting it back later
    def apply_action(self, action:tuple[str, str]) -> GameState: #typegame state might be a problem later 
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

    # returns True if the game has ended, False otherwise
    def is_done(self) -> bool:
        # Check if the game has ended
        if self.ply_count >= 10:
            return True

        if self.exfiltrated:
            return True

        return False

    # returns the utility of the current state from the perspective of the defender
    def get_util(self) -> int:
        #defender util fn , attacker util fn is just the negative of this
        x = 1 if self.exfiltrated else 0
        sum_assets = sum(host.value for host in self.hosts if host.compromised)

        return -(sum_assets)-(10-self.defender_budget)- (100 * x)
    
