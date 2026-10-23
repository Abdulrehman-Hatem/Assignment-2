

class Host:

    def __init__(self, id:str, value:int, connections:list, compromised:bool=False, patched:bool=False, isolated:bool=False):
        self.id = id
        self.value = value
        self.connections = connections
        self.compromised = compromised
        self.patched = patched
        self.isolated = isolated

    def get_connections_list(self) -> list[str]:
        return [conn.id for conn in self.connections]

    