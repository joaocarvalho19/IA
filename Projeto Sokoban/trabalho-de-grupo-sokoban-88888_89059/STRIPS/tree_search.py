
# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod
import sys
import asyncio
# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc

class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal

    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, depth, cost, heuristic,action): 
        self.state = state
        self.parent = parent
        self.depth=depth
        self.cost=cost
        self.action=action
        self.heuristic = heuristic

    def in_parent(self, newstate):
        if self.parent == None:
            return False
        new = sorted(str(newstate))
        par = sorted(str(self.parent.state))
        if new==par:
            print("equals")
            return True
        return self.parent.in_parent(newstate)

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0, 0, 0, None)
        self.open_nodes = [root]
        self.strategy = strategy 
        self.solution = None 
        self.terminal=1
        self.non_terminal=0
        self.avg_ramification = None
       

    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    def get_plan(self, node):
        if node.parent == None:
            return []
        plan = self.get_plan(node.parent)
        plan+=[node.action]
        
        return plan

    @property
    def plan(self):
        return self.get_plan(self.solution)

    @property
    def length(self):
        return self.solution.depth

    @property
    def avg_branching(self):
        return round((self.terminal+self.non_terminal-1)/self.non_terminal, 2)

    @property
    def cost(self):
        return self.solution.cost

    # procurar a solucao
    async def search(self,limit=None):

        self.limit=limit
        while self.open_nodes != []:  
            await asyncio.sleep(0.0)
            node = self.open_nodes.pop(0)        
            if self.problem.goal_test(node.state):
                self.solution = node
                print("FOUND!!")
                #self.length = self.solution.depth
                self.terminal += len(self.open_nodes)
                self.avg_ramification = self.avg_branching
                self.terminal=len(self.open_nodes)     
                return [self.get_path(node), self.solution.cost]

            self.non_terminal+=1
            lnewnodes = []
            for a in self.problem.domain.actions(node.state):
                """print(a)
                print("-------------------------")"""
                newstate = self.problem.domain.result(node.state,a)           
                newnode = SearchNode(newstate, node, node.depth+1, node.cost + self.problem.domain.cost(node.state, a),self.problem.domain.heuristic(newstate, self.problem.goal), a)
                if not node.in_parent(newstate) and (limit == None or newnode.depth<=self.limit):
                    lnewnodes.append(newnode)
            """print("LNEW:",len(lnewnodes))
            for l in lnewnodes:
                print("----------",l)"""
            #print("###########################")
            self.add_to_open(lnewnodes)

        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key= lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key= lambda node: node.heuristic)
        elif self.strategy == 'A*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key= lambda node: node.heuristic + node.cost)


