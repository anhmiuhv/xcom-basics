import board
import math
import copy

class Controller:
    def __init__(self):
        self.nothing = "nothing"
    
    def makemove(self, board,mouse1, mouse2):
        coord1 = []
        coord1.append(int(math.floor(mouse1[0]/60)))
        coord1.append(int(math.floor(mouse1[1]/60)))
        
        
        coord1.append(int(math.floor(mouse2[0])/60))
        coord1.append(int(math.floor(mouse2[1])/60))
        
        if (board.tiles[coord1[0]][coord1[1]].unit != None)&(board.tiles[coord1[2]][coord1[3]].unit != None):
            
            dummyUnit = copy.copy(board.tiles[coord1[0]][coord1[1]].unit)
            board.tiles[coord1[0]][coord1[1]].unit = copy.copy(board.tiles[coord1[2]][coord1[3]].unit)
            board.tiles[coord1[2]][coord1[3]].unit = dummyUnit
        
        return board