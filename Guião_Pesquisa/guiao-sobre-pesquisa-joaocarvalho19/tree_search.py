
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
    def __init__(self,state,parent,depth,cost,heuristic,a): 
        self.state = state
        self.parent = parent
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic
        self.action=a
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth'): 
        self.problem = problem
        root = SearchNode(problem.initial, None, 0,0,self.problem.domain.heuristic(problem.initial, self.problem.goal),None)
        self.open_nodes = [root]
        self.strategy = strategy
        self.length=0
        self.solution=None
        self.non_terminals=1
        self.terminals=0
        self.node_num=0
        self.avg_ramification=0
        self.plan = []


    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # registar a profuntdidade do nó
    def node_depth(self,node):
        if node.parent == None:
            return 0
        return 1 + self.node_depth(node.parent)
    
    def get_plan(self,node):
        if node.parent == None:
            return []
        plan = [node.plan] + self.get_plan(node.parent)
        return path
    
    def plan():
        return self.get_plan(self.solution)

    def length1(self):
        s = self.length
        return s
    
    # procurar a solucao
    def search(self,limit=None):
        while self.open_nodes != []:
                node = self.open_nodes.pop(0)
                if self.problem.goal_test(node.state):
                    self.terminals = len(self.open_nodes)
                    self.solution = node
                    self.avg_ramification=self.node_num/self.non_terminals
                    return self.get_path(node), node.cost
                lnewnodes = []
                self.non_terminals+=1
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                    newnode = SearchNode(newstate,node,len(self.get_path(node)), node.cost+self.problem.domain.cost(node.state,a), self.problem.domain.heuristic(newstate, self.problem.goal),a)
                    if newstate not in self.get_path(node) and (limit == None or newnode.depth<=limit):
                        self.node_num+=1
                        lnewnodes.append(newnode)
                self.add_to_open(lnewnodes)
                self.length += 1
        
        return None

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key = lambda node: node.cost)
        elif self.strategy == 'greedy':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key = lambda node: node.heuristic)
        elif self.strategy == 'A*':
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key = lambda node: node.heuristic+node.cost)

