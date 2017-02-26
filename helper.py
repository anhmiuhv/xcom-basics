import pygame
import random, os.path
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