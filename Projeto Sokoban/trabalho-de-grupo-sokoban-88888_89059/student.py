import asyncio
import getpass
import json
import os
import move_map
import deadlock_list
import sys
import math

import websockets
from mapa import Map
from copy import deepcopy
from consts import Tiles, TILES
import hash_table
import time

# Next 4 lines are not needed for AI agents, please remove them from your code!
import pygame

pygame.init()
program_icon = pygame.image.load("data/icon2.png")
pygame.display.set_icon(program_icon)



# Verificar se o movimento é possível
def nei_filter(node,move, deadlocks):
    (x,y) = node.keeper
    (dx,dy) = move

    #Nova localização do keeper
    (new_x,new_y) = (x+dx,y+dy)

    # Não pode ser Wall
    if node.get_tile([new_x,new_y]) == Tiles.WALL:
        return False

    # Só pode mexer uma box se atrás estiver espaço vazio ou um goal
    if (node.get_tile([new_x,new_y]) == Tiles.BOX or node.get_tile([new_x,new_y]) == Tiles.BOX_ON_GOAL):
        back_x = new_x + dx
        back_y = new_y + dy

        if (node.get_tile([back_x,back_y]) == Tiles.BOX or node.get_tile([back_x,back_y]) == Tiles.WALL or node.get_tile([back_x,back_y]) == Tiles.BOX_ON_GOAL or (back_x,back_y) in deadlocks.getDeads()):
                return False
                
    
    return True


# Buscar as possiveis coordenadas vizinhas do keeper
def get_neighbours(node,moves,deadlocks):
    return [(dx,dy) for (dx,dy) in moves if nei_filter(node,(dx,dy), deadlocks)]

# retorna a lista dos possiveis novos nodes
def new_states(node, move_map, deadlocks):  
    return [new_node(nei,node,move_map) for nei in get_neighbours(node ,[(0,1),(0,-1),(1,0),(-1,0)] ,deadlocks)]

def new_node(move,node,move_map):
        (x,y) = node.keeper
        (dx,dy) = move
        new_node = deepcopy(node)
        l = move_map.returnList(node)

        # Nova localização do keeper
        (new_x,new_y) = (x+dx,y+dy)
        goal = False
        push = False

        if new_node.get_tile([new_x,new_y]) == Tiles.BOX:
            push = True

        elif new_node.get_tile([new_x,new_y]) == Tiles.BOX_ON_GOAL:
            push = True
            goal = True
        
        if new_node.get_tile([new_x,new_y]) == Tiles.GOAL:
            goal = True

        # Empurrar uma box
        if push:
            back_x = new_x + dx
            back_y = new_y + dy

            if new_node.get_tile([back_x,back_y]) == Tiles.FLOOR:
                new_node.clear_tile([back_x,back_y])
                new_node.set_tile([back_x,back_y], Tiles.BOX)
            elif new_node.get_tile([back_x,back_y]) == Tiles.GOAL:
                new_node.clear_tile([back_x,back_y])
                new_node.set_tile([back_x,back_y], Tiles.BOX_ON_GOAL)

        new_node.clear_tile([x,y])
        new_node.clear_tile([new_x,new_y])

        if goal:
            new_node.set_tile((new_x,new_y), Tiles.MAN_ON_GOAL)
        else:
            new_node.set_tile((new_x,new_y), Tiles.MAN)

        move_map.setMoveMap(new_node,l)
        move_map.addMove(new_node,move)

        return new_node
	

def calDistance(a, b):
    #Euclidean distance
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))
    

def calcHeuristic(node):
        """
        A naive heuristic. Returns the sum of the shortest distance between the
        player with an unplaced box and the distances between each box and their
        nearest goals
        """
        unplaced_boxes = node.filter_tiles([Tiles.BOX])
        unfilled_goals = node.empty_goals

        if not unplaced_boxes:
            return 0
        if not unfilled_goals:
            return 0

        player_dist = min([calDistance(node.keeper, box) for box in unplaced_boxes])
        box_distances = sum([min([calDistance(box, goal) for goal in unfilled_goals]) for box in unplaced_boxes])

        return player_dist + box_distances



async def solver(puzzle, solution):
    while True:
        game_properties = await puzzle.get()
        mapa = Map(game_properties["map"])
        print("NEW LEVEL!")
        print(mapa)
        open_nodes = [(mapa,calcHeuristic(mapa))]
        hash_t = hash_table.hash_table()
        hash_t.hashCheck(mapa)
        move_m = move_map.move_map()
        move_m.setMoveMap(mapa,[])

        deadlocks = deadlock_list.deadlock_list()
        deadlocks.find_deadlocks(mapa)
        print("THIS MAP HAS:",len(deadlocks.getDeads()),"DEADLOCKS")
        nodes = 0
        keys=""
        
        while True:
            await asyncio.sleep(0)  # this should be 0 in your code and this is REQUIRED
            nodes += 1
            node = open_nodes.pop(0)
            currentNode = node[0]
            if currentNode.completed:
                print("FOUND!!!!!")
                #Solução! - as boxes estão nos goals
                for m in move_m.returnList(currentNode):
                    if m == (1,0):
                        keys += "d"
                    if m == (-1,0):
                        keys += "a"
                    if m == (0,1):
                        keys += "s"
                    if m == (0,-1):
                        keys += "w"

                break

            if nodes % 1000 == 0:
                print ("...")

            lnewnodes = []
            for newnode in new_states(currentNode, move_m, deadlocks):  
                if not hash_t.hashCheck(newnode):
                    lnewnodes.append((newnode, calcHeuristic(newnode)))

            open_nodes.extend(lnewnodes)            
            open_nodes.sort(key = lambda node: node[1])  #Priorizar heuristica

        await solution.put(keys)

        
async def agent_loop(puzzle, solution, server_address="localhost:8000", agent_name="student"):
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

                #-------------------------------------------------------------------------
                key=""
                if len(keys):  # we got a solution!
                    key = keys[0]
                    keys = keys[1:]

                #--------------------------------------------------------------------------
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
