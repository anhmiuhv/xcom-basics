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
from DummyAI import DummyAI

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

    
    #pygame.draw.rect(blank, (50,140,200), (0,0,60,60), 2)
    soldiers = []
    soldiers.append([])
    soldiers.append([])

    wep_assault = soldier.Weapon("Assault Rifle", 3, 5, 3, [25,20,18,16,14,12,10,8,6,4,2,0,0,0,0,0,0,0,0,0,-5,-10,-15,-20,-25,-30], 0, 2)
    wep_shotgun = soldier.Weapon("Shotgun", 4, 7, 3, [45,40,32,24,16,8,4,0,0,-4,-8,-16,-32,-40,-70,-80,-90,-100], 20, 3)
    wep_sniper = soldier.Weapon("Sniper Rifle", 4, 6, 3, [-35,-30,-27,-24,-21,-18,-15,-12,-9,-6,-3,0,0,0,0,0,0,0,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10], 10, 3, True)


    # Initialize time for checking click
    x = 0
    y = 0

    for i in range(0,board1.width):
        for j in range(0,board1.height):
            exec(compile(open("soldier.txt", "rb").read(), "soldier.txt", 'exec'))
            exec(compile(open("map.txt", "rb").read(), "map.txt", 'exec'))



    renderer = Renderer.Renderer(board1,screen)
    controller = Controller.Controller()
    count = 0

    srcTile = None
    desTile = None
    ID = None

    currentTile = None
    displayHover = 0
    currentSide = 0
    
    dummyAI = DummyAI('noob1')
    xcomwin = 0
    alienwin = 0
    try:
        while 1:
            event = pygame.event.poll()
            #event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    print("XCOM wins: " + str(xcomwin))
                    print("ALIENS wins: " + str(alienwin))
                    break
#             coord2 = pygame.mouse.get_pos()
#             currentTile = controller.getTile(board1, coord2)
#             if (currentTile.unit !=None):
#                 if displayHover == 3:
#                     displayHover = 1
#             else:
#                 if displayHover == 2:
#                     displayHover = 0
#    
#             if displayHover == 1:
#                 print ("mouse is over 'unit'")
#                 renderer.renderHover(currentTile,myfont)
#                 displayHover = 2
#                 print(currentSide)
#    
#             elif(displayHover == 0):
#                 print("mouse is not on unit anymore")
#                 if count == 0:
#                     renderer.render(board1)
#                 displayHover = 3
#                 print(currentSide)



            if currentSide == 0:
                dummyAI.execution(board1,soldiers,currentSide)
                srcTile = dummyAI.srcTile
                desTile = dummyAI.desTile
                ID = dummyAI.ID
            
            if currentSide == 1:
                dummyAI.execution(board1,soldiers,currentSide)
                srcTile = dummyAI.srcTile
                desTile = dummyAI.desTile
                ID = dummyAI.ID
                
#             if pygame.mouse.get_pressed()[0]:
#                 if ((time.time() - x) > 0.5):
#                     x = time.time()
#  
#                     #print ("You have opened a chest!")
#                     if (count == 0):
#  
#                         coord1 = pygame.mouse.get_pos()
#                         srcTile = controller.getTile(board1, coord1)
#  
#                         if (srcTile.unit != None and srcTile.unit in soldiers[currentSide] and srcTile.unit.actionPoints > 0):
#                             print(str(srcTile.unit.actionPoints))
#                             count = count + 1
#                             print("got it")
#                             renderer.renderPossibleTiles([srcTile])
#                         else:
#                             count = 0
#                             print("You do not click on an unit nooob!")
#  
#                     elif(count == 2):
#                         print("destination receive")
#                         coord2 = pygame.mouse.get_pos()
#                         desTile = controller.getTile(board1, coord2)
#  
#                         count = 0
#                         #board2 = controller.makemove(board1, coord1,coord2)
#  
#                 else:
#                     print("you pressed too fast")
#                     #coord = pygame.mouse.get_pos()
#             if event.type == pygame.KEYDOWN:
#                 if (count == 1)or(count == 2):
#                     if ((time.time() - y) > 0.5):
#                         y = time.time()
#                         if event.key == pygame.K_ESCAPE or event.unicode == '1':
#                             if 1 in controller.possibleAction(srcTile):
#                                 print("move")
#                                 ID = 1
#                                 count = 2
#                                 possibleTiles = controller.possibleTiles(board1, srcTile, ID)
#                                 renderer.renderPossibleTiles(possibleTiles)
#                         if event.key == pygame.K_ESCAPE or event.unicode == '2':
#                             if 2 in controller.possibleAction(srcTile):
#                                 print("dash")
#                                 ID = 2
#                                 count = 2
#                                 possibleTiles = controller.possibleTiles(board1, srcTile, ID)
#                                 renderer.renderPossibleTiles(possibleTiles)
#                         if event.key == pygame.K_ESCAPE or event.unicode == '3':
#                             if 3 in controller.possibleAction(srcTile):
#                                 print("shoot")
#                                 ID = 3
#                                 count = 2
#                                 possibleTiles = controller.possibleTiles(board1, srcTile, ID)
#                                 renderer.renderPossibleTiles(possibleTiles)
#                         if event.key == pygame.K_ESCAPE or event.unicode == '4':
#                             print(controller.possibleAction(srcTile))
#                             if 4 in controller.possibleAction(srcTile):
#                                 print(controller.possibleAction(srcTile))
#                                 print("reload")
#                                 ID = 4
#                                 desTile = board.Tile((100,100))
#                                 print(controller.performAction(board1, srcTile, desTile, ID))
#                                 desTile = None
#                                 srcTile = None
#                                 ID = None
#                                 count = 0
#                                 renderer.render(board1)
# #                             possibleTiles = controller.possibleTiles(board1, srcTile, ID)
# #                         renderer.renderPossibleTiles(possibleTiles)
#                     else:
#                         print("you press too fast")
            if (srcTile == None):
                if currentSide == 1:
                    currentSide = 0
                    print("XCOM's Turn")
                else:
                    currentSide = 1
                    print("Alien's Turn")
                for u in soldiers[currentSide]:
                    u.actionPoints = 2
                
            if (srcTile != None) and (desTile != None) and (ID != None):
                #print("action perform")
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


                if helper.checkWinCondition(board1)==0:
                    print("XCOM wins yay")
                    xcomwin = xcomwin + 1
                    board1 = board.Board(15,20)
                    for i in range(0,board1.width):
                        for j in range(0,board1.height):
                            exec(compile(open("soldier.txt", "rb").read(), "soldier.txt", 'exec'))
                            exec(compile(open("map.txt", "rb").read(), "map.txt", 'exec'))
                
            
                    renderer = Renderer.Renderer(board1,screen)
                    controller = Controller.Controller()
                    count = 0
                
                    srcTile = None
                    desTile = None
                    ID = None
                
                    currentTile = None
                    displayHover = 0
                    currentSide = 0
                elif helper.checkWinCondition(board1)==1:
                    print("XCOM noob, Alien win")
                    alienwin = alienwin+1
                    board1 = board.Board(15,20)
                    for i in range(0,board1.width):
                        for j in range(0,board1.height):
                            exec(compile(open("soldier.txt", "rb").read(), "soldier.txt", 'exec'))
                            exec(compile(open("map.txt", "rb").read(), "map.txt", 'exec'))
                
            
                    renderer = Renderer.Renderer(board1,screen)
                    controller = Controller.Controller()
                    count = 0
                
                    srcTile = None
                    desTile = None
                    ID = None
                
                    currentTile = None
                    displayHover = 0
                    currentSide = 0
                
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
