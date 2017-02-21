# Tile's attributes: whether they are passable, their xy coordinates (as a tuple)
# the cover values of 4 sides, and the unit standing on the tile
class Tile:
    def __init__(self, coords, passable = True, coverN = 0, coverE = 0, coverS = 0, coverW = 0, unit = None):
        self.passable = passable
        self.coords = coords
        self.coverN = coverN
        self.coverE = coverE
        self.coverS = coverS
        self.coverW = coverW
        self.unit = unit

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










