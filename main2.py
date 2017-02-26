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
import time
from pygame import display

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
    pygame.font.init() # you have to call this at the start, 
                        # if you want to use this module.
    myfont = pygame.font.SysFont("Comic Sans MS", helper.getTextSize())
    pygame.display.set_caption('XCom - the Unknown Noob')
    pygame.mouse.set_visible(1)
    board1 = board.Board(15,20)
    screen = pygame.display.set_mode(((helper.getResolution()+4)*board1.width, (helper.getResolution()+4)*board1.height))

    #tiles = {}
    # papixel = pygame.Surface((60,60))
    # #papixel = papixel.convert()
    # papixel.fill((0, 0, 255))

    papixel = helper.load_image('papixel.png').convert()
    transColor = papixel.get_at((0,0))
    papixel.set_colorkey(transColor)
    papixel = pygame.transform.scale(papixel, (helper.getResolution(), helper.getResolution()))
#picture = pygame.transform.scale(picture, (1280, 720))
    ns = helper.load_image('ns.png').convert()
    transColor = ns.get_at((0,0))
    ns.set_colorkey(transColor)
    ns = pygame.transform.scale(ns, (helper.getResolution(), helper.getResolution()))

    blank = pygame.Surface((helper.getResolution(),helper.getResolution()))
    blank = papixel.convert()
    blank.fill((255, 255, 255))
    #pygame.draw.rect(blank, (50,140,200), (0,0,60,60), 2)
    soldiers = []
    soldiers.append([])
    soldiers.append([])

    wep_assault = soldier.Weapon("Assault Rifle", 3, 5, 3, [25,20,18,16,14,12,10,8,6,4,2,0,-2,-4,-6,-8,-10,-12,-14,-16,-18,-20,-25])


    # Initialize time for checking click
    x = 0
    y = 0
    
    for i in range(0,board1.width):
        for j in range(0,board1.height):

            
            if (i==5)&(j==7):
                unit1 = soldier.Soldier("Julian", copy.copy(wep_assault), (i,j))
                unit1.set_image(papixel)
                board1.tiles[i][j].unit = unit1
                soldiers[0].append(unit1)
                testtile = board1.tiles[i][j]
            elif (i==1)&(j==2):
                unit2 = soldier.Soldier("Lalala", copy.copy(wep_assault), (i,j), side = 1)
                unit2.set_image(ns)
                board1.tiles[i][j].unit = unit2
                soldiers[1].append(unit2)
            elif (i ==10)&(j==10):
                unit1 = soldier.Soldier("Julian2", copy.copy(wep_assault), (i,j))
                unit1.set_image(papixel)
                board1.tiles[i][j].unit = unit1
                soldiers[0].append(unit1)


            if (i==3)&(j==6):
                board1.tiles[i][j].coverN = 1
            if (i==3)&(j==6):
                board1.tiles[i][j].coverW = 1
            if (i==2)&(j==6):
                board1.tiles[i][j].coverS = 1
            if (i==11)&(j==7):
                board1.tiles[i][j].coverE = 1


            if (j == 9) and ((i!=5) and (i!=6) and (i!=12)):
                board1.tiles[i][j].passable = False
            
            
    renderer = Renderer.Renderer(board1,screen)
    controller = Controller.Controller()
    count = 0

    srcTile = None
    desTile = None
    ID = None
    
    currentTile = None
    displayHover = 0
    currentSide = 0
    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            coord2 = pygame.mouse.get_pos()
            currentTile = controller.getTile(board1, coord2)
            if (currentTile.unit !=None):
                if displayHover == 3:
                    displayHover = 1
            else: 
                if displayHover == 2:
                    displayHover = 0
            
            if displayHover == 1:
                print ("mouse is over 'unit'")
                renderer.renderHover(currentTile,myfont)
                displayHover = 2
                
            elif(displayHover == 0):
                print("mouse is not on unit anymore")
                if count == 0:
                    renderer.render(board1)
                displayHover = 3
                
          
                            
            
            if pygame.mouse.get_pressed()[0]:
                if ((time.time() - x) > 0.5):
                    x = time.time()
                    
                    #print ("You have opened a chest!")
                    if (count == 0):

                        coord1 = pygame.mouse.get_pos()
                        srcTile = controller.getTile(board1, coord1)

                        if (srcTile.unit != None and srcTile.unit in soldiers[currentSide] and srcTile.unit.actionPoints > 0):
                            print(str(srcTile.unit.actionPoints))
                            count = count + 1
                            print("got it")
                            renderer.renderPossibleTiles([srcTile])
                        else:
                            count = 0
                            print("You do not click on an unit nooob!")

                    elif(count == 2):
                        print("destination receive")
                        coord2 = pygame.mouse.get_pos()
                        desTile = controller.getTile(board1, coord2)

                        count = 0
                        #board2 = controller.makemove(board1, coord1,coord2)

                else:
                    print("you pressed too fast")
                    #coord = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if (count == 1)or(count == 2):
                    if ((time.time() - y) > 0.5):
                        y = time.time()
                        if event.key == pygame.K_ESCAPE or event.unicode == '1':
                            print("move")
                            ID = 1
                            count = 2
                            possibleTiles = controller.possibleTiles(board1, srcTile, ID)
                            renderer.renderPossibleTiles(possibleTiles)
                        if event.key == pygame.K_ESCAPE or event.unicode == '2':
                            print("dash")
                            ID = 2
                            count = 2
                            possibleTiles = controller.possibleTiles(board1, srcTile, ID)
                            renderer.renderPossibleTiles(possibleTiles)
                        if event.key == pygame.K_ESCAPE or event.unicode == '3':
                            print("shoot")
                            ID = 3
                            count = 2
                            possibleTiles = controller.possibleTiles(board1, srcTile, ID)
                            renderer.renderPossibleTiles(possibleTiles)
                        if event.key == pygame.K_ESCAPE or event.unicode == '4':
                            print("reload")
                            ID = 4
                            desTile = board.Tile((100,100))
                            print(controller.performAction(board1, srcTile, desTile, ID))
                            desTile = None
                            srcTile = None
                            ID = None
                            count = 0
                            renderer.render(board1)
#                         possibleTiles = controller.possibleTiles(board1, srcTile, ID)
#                         renderer.renderPossibleTiles(possibleTiles)
                    else:
                        print("you press too fast")

            if (srcTile != None) and (desTile != None) and (ID != None):
                print("action perform")
                print(controller.performAction(board1, srcTile, desTile, ID))
                srcTile = None
                desTile = None
                ID = None
                renderer.render(board1)
                switch = True
                for u in soldiers[currentSide]:
                    if u.actionPoints > 0 and u.health > 0:
                        switch = False
                if switch:
                    if currentSide == 0:
                        currentSide = 1
                        print("Alien Activity")
                    else:
                        currentSide = 0
                        print("XCOM's Turn")
                    for u in soldiers[currentSide]:
                        u.actionPoints = 2



            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
