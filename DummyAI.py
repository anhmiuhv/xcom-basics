import board
import Controller
from random import randint
import helper

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

    def improvedRandomExecution(self,board,soldiers,side):
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
        
        if self.srcTile != None:
#             testList = self.dangerBoard(board, soldiers, side, self.srcTile.unit)
#             if testList[self.srcTile.coords[0]][self.srcTile.coords[1]] > helper.findMinTile(testList)[1]:
#                 self.ID = randint(1,2)
#                 if (self.ID == 2) and (self.srcTile.unit.actionPoints < 2):
#                     self.ID = 1
#             else: 
#                 self.ID = 3
#                 if self.srcTile.unit.weapon.ammo == 0:
#                     self.ID = 4
            self.ID = randint(1,4)

            while ((self.ID == 2) and (self.srcTile.unit != None) and (self.srcTile.unit.actionPoints == 1)):
    #         while not((self.srcTile != None) and (self.ID in self.controller.possibleAction(self.srcTile))):
                self.ID = randint(3,4)
            
            
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
            
        check = 1
        
        if self.srcTile != None:    
                
            if self.ID ==1 or self.ID ==2:
                testList = []
                if (self.srcTile.unit.weapon.name == 'Assault Rifle') or (self.srcTile.unit.weapon.name == 'Sniper Rifle'):
                    coords = []
                    testList = self.dangerBoard(board, soldiers, side, self.srcTile.unit)
                    possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
                    for tile in possibleDesTile:
                        coords.append(tile.coords)
                    mincoord = helper.findMinTile(testList,coords)
                    self.desTile = board.tiles[mincoord[0][0]][mincoord[0][1]]
                else:
                    coords = []
                    testList = self.dangerBoard(board, soldiers, side, self.srcTile.unit)
                    possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
                    for tile in possibleDesTile:
                        coords.append(tile.coords)
                    testList1 = self.dangerBoard(board, soldiers, side, self.srcTile.unit)
                    testList2 = self.shootMap(board, soldiers, side, self.srcTile.unit)
                    mincoord1 = helper.findMinTile(testList1,coords)
                    mincoord2 = helper.findMinTile(testList2,coords)
#                     if mincoord1[1] < mincoord2[1]:
#                         mincoord = mincoord1
#                         print("safe over aggressive")
#                     else: 
#                         mincoord = mincoord2
#                         print("aggressive over safe")
                    mincoord = mincoord1
                    self.desTile = board.tiles[mincoord[0][0]][mincoord[0][1]]
                #mincoord = helper.findMinTile(testList)
                #possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
#                 for i in range (0,len(possibleDesTile)):
#                     if board.tiles[mincoord[0]][mincoord[1]] == possibleDesTile[i]:
                #self.desTile = board.tiles[mincoord[0][0]][mincoord[0][1]]
                
                
            possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
            
            action = False
            
            for tile in possibleDesTile:
                if (tile.coords == self.desTile.coords):
                        action = True
            
#             if action == False:
#                 if side == 1:
# # #                 if self.srcTile.unit.weapon.name == 'Shotgun':
#                     if self.ID == 1 or self.ID == 2:
#                         self.desTile = helper.tryToGetToTile(possibleDesTile,self.desTile)
    
        else:
            self.desTile = None
#                 if check == 1:
#                     self.ID = 2
#             
#             if self.ID == 2: 
#                 testList = self.dangerBoard(board, soldiers, side, soldiers[side][0])
#                 mincoord = helper.findMinTile(testList)
#                 possibleDesTile = self.controller.possibleTiles(board,self.srcTile,self.ID)
#                 for i in range (0,len(possibleDesTile)):
#                     if board.tiles[mincoord[0]][mincoord[1]] == possibleDesTile[i]:
#                         self.desTile = board.tiles[mincoord[0]][mincoord[1]]
#                         check = 1
            
    def dangerBoard(self, board, soldiers, side, thesoldier):
        utilityB =[]
        otherside = []
        thisside = []
        #find position of units from the other side
        for i in range(0,board.width):
            utilityB.append([])
            for j in range(0,board.height):
                utilityB[i].append(0)
                if not board.tiles[i][j].passable:
                    utilityB[i][j] = 1000000
                    continue
                if (board.tiles[i][j].unit != None): 
                    if (board.tiles[i][j].unit.side != side):
                        otherside.append(board.tiles[i][j])
                    else:
                        thisside.append(board.tiles[i][j])
                    if board.tiles[i][j].unit != thesoldier:
                        utilityB[i][j] = 1000000

        for g in otherside:
            for i in range(0,board.width):
                for j in range(0,board.height):
                    utilityB[i][j] += self.controller.dangerScore(board, board.tiles[i][j], g, thesoldier)
                    
        return utilityB
    
    def shootMap(self, board, soldiers, side, thesoldier):
        utilityB =[]
        otherside = []
        thisside = []
        
        #find position of units from the other side
        for i in range(0,board.width):
            utilityB.append([])
            for j in range(0,board.height):
                utilityB[i].append(0)
                if not board.tiles[i][j].passable:
                    utilityB[i][j] = 1000000
                    continue
                if (board.tiles[i][j].unit != None): 
                    if (board.tiles[i][j].unit.side != side):
                        otherside.append(board.tiles[i][j])
                    else:
                        thisside.append(board.tiles[i][j])
                    if board.tiles[i][j].unit != thesoldier:
                        utilityB[i][j] = 1000000
                    else:
                        thesoldiertile = board.tiles[i][j]

        for g in otherside:
            for i in range(0,board.width):
                for j in range(0,board.height):
                    utilityB[i][j] -= self.controller.damageScore(board, board.tiles[i][j], thesoldier, g)
                    
        return utilityB
                
        