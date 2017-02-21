#Tile contains 2 attributes: whether they are passable, and the unit standing on the tile
class Tile:
    def __init__(self, passable = True, unit = None):
        self.passable = passable
        self.unit = unit

class Board:
    def __init__(self, height, width, covers, tiles = []):
        self.height = height
        self.width = width
        self.covers = covers
        self.tiles = tiles


