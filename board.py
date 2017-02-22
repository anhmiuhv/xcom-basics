import math

SQRT2 = math.sqrt(2)

# Priority queue for A* implementation
class PQ:
    def __init__(self):
        self.list = []

        def empty(self):
            return len(self.list) == 0

        def put(self, item, priority):
            heapq.heappush(self.list, (priority, item))

        def get(self):
            return heapq.heappop(self.list)[1]

def createBoard():
    return Board()


# Tile's attributes: whether they are passable, their xy coordinates (as a tuple)
# the cover values of 4 sides, and the unit standing on the tile
# (note: a tile knows its position within the board as well. this is so that
# coding is more convenient and the game is faster than if you manually find the tile)
class Tile:
    def __init__(self, coords, passable = True, coverN = 0, coverE = 0, coverS = 0, coverW = 0, unit = None):
        self.passable = passable
        self.coords = coords
        self.coverN = coverN
        self.coverE = coverE
        self.coverS = coverS
        self.coverW = coverW
        self.unit = unit
        self.neighbors = []



# xy coordinates start from the top left of the window
class Board:
    # tiles is a dict with key being coords and value being actual tiles
    def __init__(self, height, width, tiles = {}):
        self.height = height
        self.width = width
        self.tiles = []
        for x in range(0, width):
            self.tiles.append([])
            for y in range(0, height):
                if (x, y) in tiles:
                    self.tiles[x].append(tiles[(x,y)])
                else:
                    self.tiles[x].append(Tile((x,y)))


    # return the cover value of a "target" tile if it's being shot at by the "start" tile
    # if there are two cover values, always use the higher one
    def coverValue(self, start, target):
        # same x
        if start.coords[0] == target.coords[0]:
            if start.coords[1] > target.coords[1]:
                return target.coverS
            elif start.coords[1] < target.coords[1]:
                return target.coverN

        # different x
        if (start.coords[0] < target.coords[0]):
            if start.coords[1] > target.coords[1]:
                return max(target.coverW, target.coverS)
            elif start.coords[1] < target.coords[1]:
                return max(target.coverW, target.coverN)
            else:
                return target.coverW

        if (start.coords[0] > target.coords[0]):
            if start.coords[1] > target.coords[1]:
                return max(target.coverE, target.coverS)
            elif start.coords[1] < target.coords[1]:
                return max(target.coverE, target.coverN)
            else:
                return target.coverE

    # fill a tile's neighbors list
    # impassable tiles are not counted, as are tiles separated by cover value larger than 50
    def fillNeighbors(self, tile):
        nlist = tile.neighbors
        if not nlist:
            x = tile.coords[0]
            y = tile.coords[1]
            leftEdge = x == 0
            rightEdge = x == self.width - 1
            topEdge = y == 0
            bottomEdge = y == self.height - 1
            if (not leftEdge):
                t = self.tiles[x-1][y]
                if t.passable and tile.coverW <= 50:
                    nlist.append(t)
            if (not leftEdge) and (not topEdge):
                t = self.tiles[x-1][y-1]
                if t.passable and (tile.coverW <= 50 or tile.coverN <= 50) and (t.coverE <= 50 or t.coverS <= 50):
                    nlist.append(t)
            if (not topEdge):
                t = self.tiles[x][y-1]
                if t.passable and tile.coverN <= 50:
                    nlist.append(t)
            if (not topEdge) and (not rightEdge):
                t = self.tiles[x+1][y-1]
                if t.passable and (tile.coverN <= 50 or tile.coverE <= 50) and (t.coverS <= 50 or t.coverW <= 50):
                    nlist.append(t)
            if (not rightEdge):
                t = self.tiles[x+1][y]
                if t.passable and tile.coverE <= 50:
                    nlist.append(t)
            if (not rightEdge) and (not bottomEdge):
                t = self.tiles[x+1][y+1]
                if t.passable and (tile.coverE <= 50 or tile.coverS <= 50) and (t.coverW <= 50 or t.coverN <= 50):
                    nlist.append(t)
            if (not bottomEdge):
                t = self.tiles[x][y+1]
                if t.passable and tile.coverS <= 50:
                    nlist.append(t)
            if (not bottomEdge) and (not leftEdge):
                t = self.tiles[x-1][y+1]
                if t.passable and (tile.coverS <= 50 or tile.coverW <= 50) and (t.coverN <= 50 or t.coverE <= 50):
                    nlist.append(t)

    # returns the straight line distance between two tiles
    def straightDistance(self, tile1, tile2):
        return sqrt(abs(tile1.coords[0] - tile2.coords[1])**2 + abs(tile1.coords[1] - tile2.coords[2])**2)

    # returns all tiles within a movement distance
    # (basically A*, but with a goal distance instead of goal tile)
    def moveDistance(self, tile, distance):
        opqueue = PQ()
        opqueue.put(tile1, 0)
        cameFrom = {}
        cost_so_far = {}
        cameFrom[tile1] = None
        cost_so_far[tile1] = 0

        while not opqueue.empty():
            current = opqueue.get()
            self.fillNeighbors(current)

            for n in current.neighbors:
                if (n.coords[0] == current.coords[0]) or (n.coords[1] == current.coords[1]):
                    cost = 1.0
                else:
                    cost = SQRT2
                new_cost = cost_so_far[current] + cost
                if new_cost > distance:
                    return cameFrom, cost_so_far
                if n not in cost_so_far or new_cost < cost_so_far[n]:
                    cost_so_far[n] = new_cost
                    priority = new_cost
                    opqueue.put(n, priority)
                    cameFrom[n] = current

        return cameFrom, cost_so_far
