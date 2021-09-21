from copy import deepcopy

class move_map:
    def __init__(self):
        self.move_list = {}

    def addMove(self,node,m):
        key = str(node.boxes + [node.keeper])
        for k in self.move_list:
            if k == key:
                self.move_list[k].append(m)

    def setMoveMap(self,node,l):
        key = str(node.boxes + [node.keeper])
        lis = deepcopy(l)
        self.move_list[key] = lis

    def getMoveMap(self):
        return self.move_list

    def returnList(self,node):
        key = str(node.boxes + [node.keeper])
        for k in self.move_list:
            if k == key:
                return self.move_list[k]
            