#!/usr/bin/env python

import random, os.path
import board
import copy
import helper
from Node import Node
import Renderer
import Controller
#import basic pygame modules
import pygame
import soldier
from pygame.locals import *

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

main_dir = os.path.split(os.path.abspath(__file__))[0]


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    #Initialize Everything
    pygame.init()
    pygame.display.set_caption('XCom - the Unknown Noob')
    pygame.mouse.set_visible(1)
    board1 = board.Board(10,15)
    screen = pygame.display.set_mode((64*board1.width+20+64*2, 64*board1.height+20))

    #tiles = {}
    # papixel = pygame.Surface((60,60))
    # #papixel = papixel.convert()
    # papixel.fill((0, 0, 255))

    papixel = helper.load_image('papixel.png').convert()
    transColor = papixel.get_at((0,0))
    papixel.set_colorkey(transColor)
    
    ns = helper.load_image('ns.png').convert()
    transColor = ns.get_at((0,0))
    ns.set_colorkey(transColor)
   
    blank = pygame.Surface((60,60))
    blank = papixel.convert()
    blank.fill((255, 255, 255))
    #pygame.draw.rect(blank, (50,140,200), (0,0,60,60), 2)
    
    wep_assault = soldier.Weapon("Assault Rifle", 3, 5, 3, [25,20,18,16,14,12,10,8,6,4,2,0])
    for i in range(0,board1.width):
        for j in range(0,board1.height):
            unit = soldier.Soldier("Julian", copy.copy(wep_assault), (i,j))
            if (i==5)&(j==7):
                unit.set_image(papixel)
                board1.tiles[i][j].unit = unit
            elif (i==1)&(j==2):
                unit.set_image(ns)
                board1.tiles[i][j].unit = unit
            
            
            
            if (i==3)&(j==6):
                board1.tiles[i][j].coverN = 1
            if (i==3)&(j==6):
                board1.tiles[i][j].coverW = 1
            if (i==2)&(j==6):
                board1.tiles[i][j].coverS = 1
            if (i==11)&(j==7):
                board1.tiles[i][j].coverE = 1  
            
            
            if (j == 4):
                board1.tiles[i][j].passable = False
    renderer = Renderer.Renderer(board1,screen)
    controller = Controller.Controller()
    count = 0
    
    srcTile = None
    desTile = None
    ID = None
    
    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            if pygame.mouse.get_pressed()[0]:
                print ("You have opened a chest!")
                if (count == 0):
                    print(count)
                    coord1 = pygame.mouse.get_pos()
                    srcTile = controller.getTile(board1, coord1)
                    if (srcTile.unit != None):
                        count = count + 1
                    
                    
                else:
                    print(count)
                    coord2 = pygame.mouse.get_pos()
                    desTile = controller.getTile(board1, coord2)
                    #board2 = controller.makemove(board1, coord1,coord2)
                    
                    count = 0
                coord = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if (count == 1):
                    if event.key == pygame.K_ESCAPE or event.unicode == '1':
                        print("move")
                        ID = 1
                    if event.key == pygame.K_ESCAPE or event.unicode == '2':
                        print("dash")
                        ID = 2
                    if event.key == pygame.K_ESCAPE or event.unicode == '3':
                        print("shoot")
                        ID = 3
                    if event.key == pygame.K_ESCAPE or event.unicode == '4':
                        print("reload")
                        ID = 4
            if (srcTile != None)&(desTile != None)&(ID != None):
                print(controller.performAction(board1, srcTile, desTile, ID))
                srcTile = None
                desTile = None
                ID = None
                renderer.render(board1)
                
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()