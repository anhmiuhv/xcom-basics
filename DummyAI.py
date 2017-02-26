import board
import Controller
from random import randint

class DummyAI:
    def __init__(self,name):
        self.name = name
        self.controller = Controller.Controller()
    def execution(self,board,soldiers,side):
        possibleSrcTile = []
        randomSrcNum = 0
        randomDesNum = 0
        for i in range(0,board.width):
            for j in range(0,board.height):
                if (board.tiles[i][j].unit != None): 
                    if (board.tiles[i][j].unit.side == side) and board.tiles[i][j].unit in soldiers[side] and (board.tiles[i][j].unit.actionPoints > 0):
                        possibleSrcTile.append(board.tiles[i][j])
        
        if (len(possibleSrcTile) > 1):
            randomSrcNum = randint(0,len(possibleSrcTile)-1)
            self.srcTile = possibleSrcTile[randomSrcNum]
        elif(len(possibleSrcTile) == 1):
            self.srcTile = possibleSrcTile[0]
        else:
            self.srcTile = None
        
        
        
        self.ID = randint(1,4)
        
        if self.srcTile != None:
            possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
            if (len(possibleDesTile)) > 1:
                randomDesNum = randint(0,len(possibleDesTile)-1)
                self.desTile = possibleDesTile[randomDesNum]
            elif(len(possibleDesTile) == 1):
                randomDesNum = 0
                self.desTile = possibleDesTile[randomDesNum]
            else:
                self.desTile = None
                
            self.desTile = possibleDesTile[randomDesNum]
        else:
            self.desTile = None
        
        