import board
import Controller
from random import randint

class DummyAI:
    def __init__(self,name):
        self.name = name
        self.controller = Controller.Controller()
    def execution(self,board,side):
        possibleSrcTile = []
        for i in range(0,board.width):
            for j in range(0,board.height):
                if (board.tiles[i][j].unit != None) and (board.tiles[i][j].unit.side == side):
                    possibleSrcTile.append(board.tiles[i][j])
        if len(possibleSrcTile) > 1:
            randomSrcNum = randint(0,len(possibleSrcTile)-1)
        else: 
            randomSrcNum = 0
            
        self.srcTile = possibleSrcTile[randomSrcNum]
        
        self.ID = randint(1,4)
        
        possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
        if (len(possibleDesTile)) > 1:
            randomDesNum = randint(0,len(possibleDesTile)-1)
        else:
            randomDesNum = 0
        self.desTile = possibleDesTile[randomDesNum]
        
        
        