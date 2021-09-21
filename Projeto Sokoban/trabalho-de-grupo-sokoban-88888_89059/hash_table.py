class hash_table:
    def __init__(self):
        self.table = []

    def hashCheck(self, node):
        state = str(node.boxes + [node.keeper])
        if state in self.table:
            return True
        else:
            self.table.append(state)
            return False

    def print_table(self):
        return self.table