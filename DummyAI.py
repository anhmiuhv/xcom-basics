import board
import Controller
from random import randint
from math import inf

class DummyAI:
    def __init__(self,name):
        self.name = name
        self.controller = Controller.Controller()
        
    def randexecution(self,board,soldiers,side):
        possibleSrcTile = []
        randomSrcNum = 0
        randomDesNum = 0
        for i in range(0,board.width):
            for j in range(0,board.height):
                if (board.tiles[i][j].unit != None): 
                    if (board.tiles[i][j].unit.side == side) and (board.tiles[i][j].unit.actionPoints > 0):
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
            while ((self.ID == 2) and (self.srcTile.unit != None) and (self.srcTile.unit.actionPoints == 1)):
    #         while not((self.srcTile != None) and (self.ID in self.controller.possibleAction(self.srcTile))):
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
    
    def utilityBoard(self, board, soldiers, side, thesoldier):
        utilityB =[]
        otherside = []
        thisside = []
        #find position of units from the other side
        for i in range(0,board.width):
            utilityB.append([])
            for j in range(0,board.height):
                utilityB[i].append(0)
                if (board.tiles[i][j].unit != None): 
                    if (board.tiles[i][j].unit.side != side):
                        otherside.append(board.tiles[i][j])
                    else:
                        thisside.append(board.tiles[i][j])
                    if board.tiles[i][j].unit != thesoldier:
                        utilityB[i].append(1000000)

        for g in otherside:
            for i in range(0,board.width):
                for j in range(0,board.height):
                    utilityB[i][j] += self.controller.dangerScore(board, board.tiles[i][j], g, thesoldier)
                    
        return utilityB
                
                
                
        
        
        