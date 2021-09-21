from consts import Tiles, TILES

class deadlock_list:
    def __init__(self):
        self.deadList = []
    
    def getDeads(self):
        return self.deadList

    def find_deadlocks(self, node):
        # Encontrar deadlocks nos "cantos" do mapa
        def corner_deadlock(self,x,y,delta_y,delta_x):
            if node.get_tile([x,y+delta_y]) == Tiles.WALL and node.get_tile([x+delta_x,y]) == Tiles.WALL:
                self.deadList.append((x,y))
                return True
            else:
                return False

        for x in range(node.size[0]):
                for y in range(node.size[1]):
                    if x == 0 or x == (node.size[0]-1) or y == 0 or (y == node.size[1]-1):
                        continue
                    if node.get_tile([x,y]) == Tiles.FLOOR or node.get_tile([x,y]) == Tiles.MAN:
                        corner_deadlock(self,x,y,-1,-1) or corner_deadlock(self,x,y,-1,1) or corner_deadlock(self,x,y,1,-1) or corner_deadlock(self,x,y,1,1)
        

        # Ligar os deadlocks se estiverem numa linha reta ao lado de uma wall(se não estiverem goals pelo caminho)
        def connect_deadlocks_horizontal(self,dx,dy):
            up = True
            down = True
            found = False
            x = dx

            while x > 1:
                x -= 1
                try:
                    if (x,dy) in self.deadList:
                        found = True
                        break
                except IndexError:
                    break
            n=0
            if found:
                sx = x
                while x != dx:
                    x += 1
                    try:
                        if node.get_tile([x,dy+1]) != Tiles.WALL and down:
                            down = False
                    except IndexError:
                        down = False
                    try:
                        if node.get_tile([x,dy-1]) != Tiles.WALL and up:
                            up = False
                    except IndexError:
                        up = False
                    try:
                        if (x,dy) not in self.deadList:
                            if node.get_tile([x,dy]) != Tiles.FLOOR and node.get_tile([x,dy]) != Tiles.MAN:
                                up = down = False
                    except IndexError:
                        down = up = False
                    n+=1
                if up or down:
                    x = sx
                    
                    while x != dx:
                        val = node.get_tile([x,dy])
                        if (val == Tiles.FLOOR or val == Tiles.MAN) and ((x,dy) not in self.deadList):
                            self.deadList.append((x,dy))
                        x += 1
        
        def connect_deadlocks_vertical(self,dx,dy):
            up = True
            down = True
            found = False
            y = dy

            while y > 1:
                y -= 1
                try:
                    if (dx,y) in self.deadList:
                        found = True
                        break
                except IndexError:
                    break
            n=0
            if found:
                sy = y
                while y != dy:
                    y += 1
                    try:
                        if node.get_tile([dx+1,y]) != Tiles.WALL and down:
                            down = False
                    except IndexError:
                        down = False
                    try:
                        if node.get_tile([dx-1,y]) != Tiles.WALL and up:
                            up = False
                    except IndexError:
                        up = False
                    try:
                        if (dx,y) not in self.deadList:
                            if node.get_tile([dx,y]) != Tiles.FLOOR and node.get_tile([dx,y]) != Tiles.MAN:
                                up = down = False
                    except IndexError:
                        down = up = False
                    n+=1
                if up or down:
                    y = sy
                    while y != dy:
                        val = node.get_tile([dx,y])
                        if (val == Tiles.FLOOR or val == Tiles.MAN) and ((dx,y) not in self.deadList):
                            self.deadList.append((dx,y))
                        y += 1


        for dead in self.deadList:
            (dx,dy) = dead
            connect_deadlocks_horizontal(self,dx, dy)
            connect_deadlocks_vertical(self,dx, dy)