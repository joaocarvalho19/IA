#João Miguel Santos Carvalho     Nmec: 89059

from tree_search import *
from cidades import *
from strips import *


class MyTree(SearchTree):

    def __init__(self,problem, strategy='breadth'): 
        super().__init__(problem,strategy)
        self.from_init = None
        self.to_goal = None

    def hybrid1_add_to_open(self,lnewnodes):
        for i in range(len(lnewnodes)):
            if i % 2 == 0:
                self.open_nodes[:0] = [lnewnodes[i]]
            else:
                self.open_nodes.extend([lnewnodes[i]])

    def hybrid2_add_to_open(self,lnewnodes):
        new_list = self.open_nodes + lnewnodes
        new_list = sorted(new_list, key=lambda x: x.depth - x.offset)
        self.open_nodes = new_list

    def search2(self):
        offs = {}
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.terminal = len(self.open_nodes)+1
                self.solution = node
                return self.get_path(node)
            self.non_terminal+=1
            node.children = []
            for a in self.problem.domain.actions(node.state):
                newstate = self.problem.domain.result(node.state,a)
                if newstate not in self.get_path(node):
                    newstate_depth = self.node_depth(node)+1
                    if newstate_depth not in offs:
                        offs[newstate_depth] = 0
                    else:
                        offs[newstate_depth] += 1
                    newnode = Node(newstate,node,newstate_depth,offs[newstate_depth])
                    node.children.append(newnode)

            self.add_to_open(node.children)
        return None
    
    # registar a profuntdidade do nó
    def node_depth(self,node):
        if node.parent == None:
            return 0
        return 1 + self.node_depth(node.parent)

    def search_from_middle(self):
        middle_state = MinhasCidades.middle(self.problem.domain,self.problem.initial,self.problem.goal)
        self.from_init = MyTree(SearchProblem(self.problem.domain,self.problem.initial,middle_state))
        from_init_list = self.from_init.search2()

        self.to_goal = MyTree(SearchProblem(self.problem.domain,middle_state,self.problem.goal))
        to_goal_list = self.to_goal.search2()
        to_goal_list.pop(0)
        return from_init_list + to_goal_list

class Node(SearchNode):
    def __init__(self,state,parent,depth,offset): 
        super().__init__(state,parent)
        self.depth=depth
        self.offset=offset


class MinhasCidades(Cidades):
    # state that minimizes heuristic(state1,middle)+heuristic(middle,state2)
    def middle(self,city1,city2):
        heur_d = {}
        for i in self.coordinates:
            if i != city1 and i != city2:
                heur_d[i] = self.heuristic(city1,i) + self.heuristic(i,city2)
        return min(heur_d.keys(), key=(lambda k: heur_d[k]))

class MySTRIPS(STRIPS):
    def result(self, state, action):
        state2 = []
        for c in state:
            if c not in action.neg:
                state2.append(c)
        return state2 + action.pos
        
    def sort(self,state):
        return sorted(state, key=lambda x: str(x))


