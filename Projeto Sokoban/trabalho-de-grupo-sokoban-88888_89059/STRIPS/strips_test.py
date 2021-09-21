#
#  Module: strips
# 
#  This module provides classes for representing STRIPS-based
#  planning domains:
#     Predicate - used to represent conditions in states and operators
#     Operator  - used to represent STRIPS operators
#     STRIPS - a "SearchDomain" for planning with STRIPS operators
#
#  (c) Luis Seabra Lopes
#  Inteligência Artificial & Introducao a Inteligencia Artificial, 2019
#

import sys
from tree_search import *
from functools import reduce
from itertools import product
import math

comp_menor = lambda x,y: True if x<y else False

def sort(list, sorted_list):
    pos=0
    menor_pos=0
    menor = list[0]
    if len(list)>2:
        for value in list[1:]: #skips the first element cause its already stored 
            pos+=1
            if  not comp_menor(menor, value):
                menor_pos=pos
                menor = value
        sorted_list.append(menor)  
        list.pop(menor_pos)
        return(sort(list, sorted_list))
    elif len(list)==2:
        if comp_menor(list[0], list[1]):
            sorted_list.append(list[0])
            sorted_list.append(list[1])
        else:
            sorted_list.append(list[1])
            sorted_list.append(list[0])
        return sorted_list
    else:
        return list

def menor(lista):
    sorted_list=[]
    return sort(lista, sorted_list)[0]

def second_menor(lista):
    sorted_list=[]
    return sort(lista, sorted_list)[1]


def distance(p1, p2):
    return math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )

# Predicates used to describe states, preconditions and effects
class Predicate:
    def __str__(self):
        argsstr = args2string(self.args)
        return type(self).__name__ + "(" + argsstr + ")"
    def __repr__(self):
        return str(self)
    def __eq__(self,predicate):   # allows for comparisons with "==", etc.
        return str(self)==str(predicate)

    def __hash__(self):
       return hash(str(self))

    def substitute(self,assign): # Substitute the arguments in a predicate by constants according to a given assignment (i.e. a dictionary)
        la = self.args     
        return type(self)(assign[la[0]])


# STRIPS operators
# -- operators for a specific domain will be subclasses
# -- concrete actions will be instances of specific operators
class Operator:

    def __init__(self,args,pc,neg,pos):
        self.args = args
        self.pc  = pc
        self.neg = neg
        self.pos = pos
    def __str__(self):
        return type(self).__name__ + '(' + args2string(self.args) + ')'
    def __repr__(self):
        argsstr = args2string(self.args)
        return type(self).__name__ + "(" + argsstr + ")"

    # Produce a concrete action by instanciating a specific 
    # operator (i.e. the "Operator" subclass where the method was 
    # called) for the arguments given in "args"
    # ( returns None if the action is not applicable in the given "state" )
    @classmethod
    def instanciate(cls,args):
        if len(args)!=len(cls.args):
            return None
        assign = dict(zip(cls.args, args))
        pc  = [ p.substitute(assign) for p in cls.pc ]
        neg = [ p.substitute(assign) for p in cls.neg ]
        pos = [ p.substitute(assign) for p in cls.pos ]
        return cls(args,pc,neg,pos)


# Search domains based on STRIPS actions
class STRIPS(SearchDomain):

    # constructor
    def __init__(self):
        pass

    # list of applicable actions in a given "state"
    def actions(self, state):
        keeper_pos = get_keeper_pos(state)[0]
        constants = state_constants(state)
        operators = Operator.__subclasses__()
        actions = []
        for op in operators:

            #A linha seguinte remove de lassign todos os predicados onde se verifiquem as seguintes condições
            #X não foi mapeado para uma posição que é a do keeper
            #Y foi mapeado para uma posição que não é contígua a X
            #Z foi mapeado para uma posição que não é contígua a Y e a 2 blocos de X
            lassign = [ assign for assign in assignments(op.args,constants, keeper_pos) if assign['X']==keeper_pos and distance(assign['Y'], keeper_pos)==1 and ('Z' not in list(assign.keys()) or (distance(assign['Z'], keeper_pos) == 2 and distance(assign['Z'], assign['Y'])==1 ))]
            
            for assign in lassign:
                argvalues = [assign[a] for a in op.args]
                action = op.instanciate(argvalues)
                if all(c in state for c in action.pc):
                    #print(action)
                    actions.append(action)  
        return actions

    # Result of a given "action" in a given "state"
    # ( returns None, if the action is not applicable in the state)
    def result(self, state, action):
        #efeitos negativos
        newstate = [p for p in state if p not in action.neg] #Apaga do estado anterior (ou não adiciona ao novo estado, depende de como quisermos ver) as propriedades que deixam de ser verdade ao executar a ação
        #efeitos positivos
        newstate.extend(action.pos)#Adiciona aos estado atual as propriedades que passam a ser verdade ao executar a ação
        return set(newstate)
        

    def cost(self, state, action):
        if type(action).__name__ == 'Move_Keeper':
            return 2
        return 1

    def heuristic(self, state, goal):
        #return -1*len([p for p in goal if p in state]) 
        #return len([p for p in goal if p in state])
        #return 0
        distances=[]
        box_distances = []
        keeper_distances = []
        boxes_pos= [p.args for p in state if type(p).__name__ == 'Box_On' or type(p).__name__ == 'Box_On_Goal'] #todas as caixas
        box_not_on_goal_pos = [p.args for p in state if type(p).__name__ == 'Box_On' ] #todas as caixas not on goal

        box_on_goal_pos = [p.args for p in state if type(p).__name__ == 'Box_On_Goal'] #caixas no goal

        goals_pos=[pos.args for pos in goal] #todos os goals
        free_goals_pos=[pos for pos in goals_pos if pos not in boxes_pos] #goals que não têm caixas
        keeper_distance_to_every_box=[]
        shortest_distance_to_box=10000
        #Calcula menor distância do keeper a uma caixa
        for pos in boxes_pos:
            shortest_distance_to_box=min([shortest_distance_to_box, distance(get_keeper_pos(state)[0], pos)])
        #calcula a distância mínima de cada caixa a um goal livre
        for pos in box_not_on_goal_pos:  
            box_distances_to_every_goal = []
            for goal in free_goals_pos:
                box_distances_to_every_goal.append(distance(pos, goal))
            try:
                box_distances.append(menor(box_distances_to_every_goal))
            except IndexError:
                pass
            
        distances.append(shortest_distance_to_box)
        distances[0:0]=box_distances[:]
        soma = sum(distances)
        #print(soma)
        return soma
        

    # Checks if a given "goal" is satisfied in a given "state"
    def satisfies(self, state, goal):
        return all(p in state for p in goal)

# Auxiliary functions

def get_keeper_pos(state):
    return [pred.args for pred in state if type(pred).__name__ == 'Keeper_On_Box_Allowed' or type(pred).__name__ == 'Keeper_On_Box_Not_Allowed' ]
def state_constants(state):
    return [pred.args for pred in state]

def assignments(lvars,lconsts, keeper_pos):
    lcombs = product(lconsts,repeat=len(lvars))
    
    makeassign = lambda comb : dict(zip(lvars,comb))
    return list(map(makeassign,lcombs))

def args2string(args):
    if args == []:
        return ""
    return str(args)