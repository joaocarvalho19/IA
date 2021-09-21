import time
from strips_test import *
from mapa import *
import asyncio
import getpass
import json
import os
from tree_search import *
import sys

import websockets
from mapa import Map
from consts import Tiles, TILES
import pygame

os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)

"""
def add_pos(pos1, pos2): #juntar o movimento à posição para saber a posição a testar
    new_pos = (pos1[0]+pos2[0], pos1[1]+pos2[1])
    return new_pos
"""

def check_neighbours(coords, map): #the purpose of this function is to check how neighbours of a given position are walls
    neighbours=[(0,1), (0,-1), (1,0), (-1,0)]
    walls=0
   
    for neighbour in neighbours:
        neighbour_pos = (coords[0]+neighbour[0], coords[1]+neighbour[1])
        try:
            tile = map.get_tile(neighbour_pos)
            if(tile == Tiles.WALL): #se tile for Wall, incrementar walls em 1 unidade
                walls+=1
        except IndexError:
            walls+=1   
    return walls

def check_for_goals(mapa):
    map_size = mapa.size
    x_max=map_size[0]
    y_max=map_size[1]
    safe_spots=[0,0,0,0]
    #checking first row of map
    for x in range(x_max):
        tile=mapa.get_tile((x,0))
        if tile==Tiles.GOAL or tile==Tiles.BOX_ON_GOAL or tile==Tiles.MAN_ON_GOAL:
            safe_spots[0]=1
            break

    #checking bottom row of map
    for x in range(x_max):
        tile=mapa.get_tile((x,y_max-1))
        if tile==Tiles.GOAL or tile==Tiles.BOX_ON_GOAL or tile==Tiles.MAN_ON_GOAL:
            safe_spots[1]=1
            break

    #checking first column of map
    for y in range(y_max):
        tile=mapa.get_tile((0,y))
        if tile==Tiles.GOAL or tile==Tiles.BOX_ON_GOAL or tile==Tiles.MAN_ON_GOAL:
            safe_spots[2]=1
            break
    
    #checking last column of map
    for y in range(y_max):
        tile=mapa.get_tile((x_max-1,y))
        if tile==Tiles.GOAL or tile==Tiles.BOX_ON_GOAL or tile==Tiles.MAN_ON_GOAL:
            safe_spots[3]=1
            break
    
    return safe_spots

        
def set_initial_state(mapa):
    map_size = mapa.size #ter dimensões do mapa
    mapa_goal_state = []
    mapa_initial_state = []

    safe_spots=check_for_goals(mapa) #holds rows or columns that would be forbidden floor but are not because they have goals in them
    
    x_max=map_size[0]
    y_max=map_size[1]

    for x in range(x_max): #percorrer x para todos os y's 
        for y in range(y_max):
            tile = mapa.get_tile(((x,y))) #Ver que tipo de tile está nessa posição

            if(tile == Tiles.FLOOR): #se tile for chão, juntar Free(pos) ao initial state
                #Verificar se se pode movimentar a caixa para o tile ou não
                if check_neighbours((x,y), mapa)<2:
                    #mapa_initial_state.append(Free((x,y)))
                    if x == 0:
                        if safe_spots[0]==1:
                            mapa_initial_state.append(Free((x,y)))
                    elif x==x_max:
                        if safe_spots[1]==1:
                            mapa_initial_state.append(Free((x,y)))
                    elif y==y_max:
                        if safe_spots[2]==1:
                            mapa_initial_state.append(Free((x,y)))
                    elif y==y_max:
                        if safe_spots[3]==1:
                            mapa_initial_state.append(Free((x,y)))
                    else:
                        mapa_initial_state.append(Free((x,y)))
                else: 
                    mapa_initial_state.append(Not_Free_For_Box((x,y)))
                    
                #else:
                #    if check_for_goals((x,y), mapa):
                #        mapa_initial_state.append(Free((x,y)))

            if(tile == Tiles.BOX): #se tile for Box, juntar Box_On(pos) ao initial state
                mapa_initial_state.append(Box_On((x,y)))

            if(tile == (Tiles.MAN)): #se tile for Homem, juntar Keeper_On(pos) ao initial state
                mapa_initial_state.append(Keeper_On_Box_Allowed((x,y)))
            
            if(tile == (Tiles.MAN_ON_GOAL)):
                mapa_initial_state.append(Keeper_On_Box_Allowed((x,y)))
                mapa_initial_state.append(Goal((x,y)))
                mapa_goal_state.append(Box_On_Goal(x,y))

            if(tile == Tiles.BOX_ON_GOAL):# junta free(pos) e box _on_goal(pos) ao init state junta box_on_goal(pos) ao goal state
                mapa_initial_state.append(Goal((x,y)))
                mapa_initial_state.append(Box_On_Goal((x,y)))
                mapa_goal_state.append(Box_On_Goal((x,y)))

            if (tile == Tiles.GOAL):
                mapa_initial_state.append(Goal((x,y))) # junta free(pos) e box _on_goal(pos) ao init state junta box_on_goal(pos) ao goal state
                mapa_initial_state.append(Free((x,y)))
                mapa_goal_state.append(Box_On_Goal((x,y)))   

    """
    free_pos= [p for p in mapa_initial_state if type(p).__name__ == 'Free' or type(p).__name__ == 'Not_Free_For_Box' ]
    print(free_pos)
    sys.exit()
    """

    return mapa_initial_state, mapa_goal_state

# Blocks world predicates


class Box_On(Predicate):
    def __init__(self, coordinates):#, next = (0,0), next_over=(0,0)):     
        #self.args = add_pos(coordinates, add_pos(next, next_over))
        self.args = coordinates#, next, next_over]
        
class Keeper_On_Box_Allowed(Predicate):
    def __init__(self, coordinates):#, next = (0,0)):     
        #self.args = add_pos(coordinates, next)
        #self.args = coordinates
        self.args = coordinates#, next]
        #set_keeper_pos(coordinates)

class Keeper_On_Box_Not_Allowed(Predicate):
    def __init__(self, coordinates):#, next = (0,0)):     
        #self.args = add_pos(coordinates, next)
        #self.args = coordinates
        self.args = coordinates#, next]
        #set_keeper_pos(coordinates)



#Allows both the keeper and the boxes into the tile
class Free(Predicate):
    def __init__(self, coordinates):#, next = (0,0), next_over=(0,0)):     
        #self.args = add_pos(coordinates, add_pos(next, next_over))
        #self.args = coordinates
        self.args = coordinates#, next, next_over]


#Allows only the keeper into the tile
class Not_Free_For_Box(Predicate):
    def __init__(self, coordinates):#, next = (0,0), next_over=(0,0)):     
        #self.args = add_pos(coordinates, add_pos(next, next_over))
        #self.args = coordinates
        self.args = coordinates#, next, next_over]

class Box_On_Goal(Predicate):
    def __init__(self,coordinates):#, next = (0,0), next_over=(0,0)):     
        #self.args = add_pos(coordinates, add_pos(next, next_over))
        #self.args = coordinates
        self.args = coordinates#, next, next_over]

class Goal(Predicate):
    def __init__(self, coordinates):     
        self.args = coordinates

# Blocks world operators

X='X'
Y='Y'
Z='Z'
M='M'

class Move_Keeper_A_A(Operator):
    args = [X, Y] # args[X,Y] Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Allowed(X), Free(Y)] #é preciso que Y esteja livre e X tenha o keeper
    neg  = [Keeper_On_Box_Allowed(X),Free(Y)] #Y deixa de estar livre e X deixa de ter o keeper
    pos  = [Keeper_On_Box_Allowed(Y), Free(X)] #Y passa a ter o keeper, X passa a estar livre

class Move_Keeper_A_NA(Operator):
    args = [X, Y] # args[X,Y] Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Allowed(X), Not_Free_For_Box(Y)] #é preciso que Y esteja livre e X tenha o keeper
    neg  = [Keeper_On_Box_Allowed(X),Not_Free_For_Box(Y)] #Y deixa de estar livre e X deixa de ter o keeper
    pos  = [Keeper_On_Box_Not_Allowed(Y), Free(X)] #Y passa a ter o keeper, X passa a estar livre

class Move_Keeper_NA_A(Operator):
    args = [X, Y] # args[X,Y] Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Not_Allowed(X), Free(Y)] #é preciso que Y esteja livre e X tenha o keeper
    neg  = [Keeper_On_Box_Not_Allowed(X), Free(Y)] #Y deixa de estar livre e X deixa de ter o keeper
    pos  = [Keeper_On_Box_Allowed(Y), Not_Free_For_Box(X)] #Y passa a ter o keeper, X passa a estar livre

class Move_Keeper_NA_NA(Operator):
    args = [X, Y] # args[X,Y] Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Not_Allowed(X), Not_Free_For_Box(Y)] #é preciso que Y esteja livre e X tenha o keeper
    neg  = [Keeper_On_Box_Not_Allowed(X), Not_Free_For_Box(Y)] #Y deixa de estar livre e X deixa de ter o keeper
    pos  = [Keeper_On_Box_Not_Allowed(Y), Not_Free_For_Box(X)] #Y passa a ter o keeper, X passa a estar livre

##################################################################################################################
class Move_Box_From_A(Operator):
    args = [X, Y, Z] #Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Allowed(X), Box_On(Y), Free(Z)] #é preciso que Y tenha uma caixa, que Z esteja livre e que X tenha o Keeper
    neg  = [Keeper_On_Box_Allowed(X), Box_On(Y), Free(Z)] #X deixa de ter o keeper, Y deixa de ter a caixa, Z deixa de estar livre
    pos  = [Keeper_On_Box_Allowed(Y), Box_On(Z), Free(X)] #X passa a estar livre, Y passa a ter o Keeper, Z passa a ter uma caixa

class Move_Box_From_NA(Operator):
    args = [X, Y, Z] #Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Not_Allowed(X), Box_On(Y), Free(Z)] #é preciso que Y tenha uma caixa, que Z esteja livre e que X tenha o Keeper
    neg  = [Keeper_On_Box_Not_Allowed(X), Box_On(Y), Free(Z)] #X deixa de ter o keeper, Y deixa de ter a caixa, Z deixa de estar livre
    pos  = [Keeper_On_Box_Allowed(Y), Box_On(Z), Not_Free_For_Box(X)] #X passa a estar livre, Y passa a ter o Keeper, Z passa a ter uma caixa

############################################################################################################

class Move_Box_To_Goal_From_A(Operator):
    args = [X, Y, Z] #Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Allowed(X), Box_On(Y), Goal(Z), Free(Z)] #é preciso que Y tenha uma caixa, que Z seja Goal e esteja livre e que X tenha o Keeper
    neg  = [Keeper_On_Box_Allowed(X), Box_On(Y), Free(Z)] #X deixa de ter o keeper, Y deixa de ter a caixa
    pos  = [Keeper_On_Box_Allowed(Y), Box_On_Goal(Z), Free(X)] #X passa a estar livre, Y passa a ter o Keeper, Z passa a ter uma caixa

class Move_Box_To_Goal_From_NA(Operator):
    args = [X, Y, Z] #Recebe o bloco onde está o Keeper e o movimento que este está a tentar fazer
    pc   = [Keeper_On_Box_Not_Allowed(X), Box_On(Y), Goal(Z), Free(Z)] #é preciso que Y tenha uma caixa, que Z seja Goal e esteja livre e que X tenha o Keeper
    neg  = [Keeper_On_Box_Not_Allowed(X), Box_On(Y), Free(Z)] #X deixa de ter o keeper, Y deixa de ter a caixa
    pos  = [Keeper_On_Box_Allowed(Y), Box_On_Goal(Z), Not_Free_For_Box(X)] #X passa a estar livre, Y passa a ter o Keeper, Z passa a ter uma caixa

################################################################################################################
class Move_Box_From_Goal_From_A(Operator):
    args = [X, Y, Z]
    pc   = [Keeper_On_Box_Allowed(X), Box_On_Goal(Y), Free(Z)]
    neg  = [Keeper_On_Box_Allowed(X), Box_On_Goal(Y), Free(Z)]
    pos  = [Keeper_On_Box_Allowed(Y), Box_On(Z), Free(X)]


class Move_Box_From_Goal_From_NA(Operator):
    args = [X, Y, Z]
    pc   = [Keeper_On_Box_Not_Allowed(X), Box_On_Goal(Y), Free(Z)]
    neg  = [Keeper_On_Box_Not_Allowed(X), Box_On_Goal(Y), Free(Z)]
    pos  = [Keeper_On_Box_Allowed(Y), Box_On(Z), Not_Free_For_Box(X)]

###############################################################################################################

async def solver(puzzle, solution):
    while True:
        game_properties = await puzzle.get()
        mapa = Map(game_properties["map"])
        print(mapa)
        #print(state)
        keys=""
        states = set_initial_state(mapa)
        
        initial_state = states[0]
        goal_state= states[1]
        domain = STRIPS()     
                                
        inittime = time.time()
        keys=""
        p = SearchProblem(domain, initial_state, goal_state)
        t = SearchTree(p, "greedy")
        #await t.search()
        print()
        while t.open_nodes != []:  
            node = t.open_nodes.pop(0)  
            print(node.action)      
            if t.problem.goal_test(node.state):
                t.solution = node
                print("FOUND!!")
                #t.length = t.solution.depth
                t.terminal += len(t.open_nodes)
                t.avg_ramification = t.avg_branching
                t.terminal=len(t.open_nodes)

                for move in t.plan:
                    stri=str(move.args[0][0]-move.args[1][0])+","+str(move.args[0][1]-move.args[1][1])
                    print(stri)
                    if stri == "1,0":
                        keys += "a"
                    if stri == "-1,0":
                        print("correto")
                        keys += "d"
                    if stri == "0,1":
                        keys += "w"
                    if stri == "0,-1":
                        keys += "s"
                print(keys)     
                break

            t.non_terminal+=1
            lnewnodes = []

            for a in t.problem.domain.actions(node.state):
                test=False
                """print(a)
                print("-------------------------")"""
                newstate = t.problem.domain.result(node.state,a)           
                newnode = SearchNode(newstate, node, node.depth+1, node.cost + t.problem.domain.cost(node.state, a),t.problem.domain.heuristic(newstate, t.problem.goal), a)
                new = sorted(str(newnode))
                for n in t.get_path(newnode):
                    par = sorted(str(self.parent.state))
                    if new == par:
                        test=True
                if not test:
                    lnewnodes.append(newnode)

            t.add_to_open(lnewnodes)
        #Solução! - as boxes estão nos goals


        print(t.solution)
        print('time=',time.time()-inittime)
        print(len(t.open_nodes),' nodes')

        await solution.put(keys)
    

async def agent_loop(puzzle, solution,server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                update = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                if "map" in update:
                    # we got a new level
                    game_properties = update
                    keys = ""
                    await puzzle.put(game_properties)
                
                if not solution.empty():
                    keys = await solution.get()

                # Next lines are only for the Human Agent, the key values are nonetheless the correct ones!
                key = ""
                if len(keys):  # we got a solution!
                    key = keys[0]
                    keys = keys[1:]

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
                
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return

            # Next line is not needed for AI agent
            #pygame.display.flip()


# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())

puzzle = asyncio.Queue(loop=loop)
solution = asyncio.Queue(loop=loop)

net_task = loop.create_task(agent_loop(puzzle, solution, f"{SERVER}:{PORT}", NAME))
solver_task = loop.create_task(solver(puzzle, solution))

loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
loop.close()

