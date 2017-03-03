import pygame
import random, os.path
import math
main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs

def getResolution():
    return 40

def getTextSize():
    return 12

def checkWinCondition(board):
    sideList = []
    sideList.append(99999)
    whowin = 99999
    for j in range(0,board.height):
            for i in range(0,board.width):
                if (board.tiles[i][j].unit != None):
                    check = 1
                    for k in range(0,len(sideList)):
                        if sideList[k] == board.tiles[i][j].unit.side:
                            check = 0
                    if check:
                        sideList.append(board.tiles[i][j].unit.side)
    if (len(sideList)==2):
        whowin = sideList[1]
    else:
        whowin = 4
    return whowin


def findMinTile(utiList,coords):
    min = utiList[0][0]
    minTile = (0,0)
    for i in range(0,len(coords)):
        
        if utiList[coords[i][0]][coords[i][1]] <= min:
            min = utiList[coords[i][0]][coords[i][1]]
            minTile = (coords[i][0],coords[i][1])
    
    return (minTile, min)

def tryToGetToTile(listTile, tile):
    bestTile = listTile[0]
    bestScore = math.fabs(tile.coords[0]-listTile[0].coords[0]) + math.fabs(tile.coords[1]-listTile[0].coords[1])
    for dummytile in listTile:
        newscore = tile.coords[0]-dummytile.coords[0] + tile.coords[1]-dummytile.coords[1]
        if (newscore < bestScore):
            bestTile = dummytile
            
    print(tile.coords)
    print(bestTile.coords)
    return bestTile