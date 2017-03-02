#!/usr/bin/env python

import random, os.path
import board
import copy
import helper
import eventHandler
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

import argparse

#parsing option from users
parser = argparse.ArgumentParser(description=' in aliens we trust')
parser.add_argument('mode',choices=['pvp','pve', 'eve'], help='The type of mode to run:')
parser.add_argument('levelOfAI',choices=['noob','godlevel'], help='The type of mode to run:')
args = parser.parse_args()
mode = 0

if args.mode == "pvp":
    mode = 1

if args.mode == "pve":
    mode = 2

if args.mode == "eve":
    mode = 3

if args.levelOfAI == "noob":
    level = 0
if args.levelOfAI == "godlevel":
    level = 1
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

    #tiles = {}
    # papixel = pygame.Surface((60,60))
    # #papixel = papixel.convert()
    # papixel.fill((0, 0, 255))

    f = open("map.txt")
    tiles = {}
    for line in f.readlines():
        cols = line.split()
        passable = (cols[2] == "True")
        tiles[(int(cols[0]),int(cols[1]))] = board.Tile((int(cols[0]), int(cols[1])), passable, int(cols[3]), int(cols[4]), int(cols[5]), int(cols[6]))

    #print(tiles)
    board1 = board.Board(15,20, tiles)

    wep_assault = soldier.Weapon("Assault Rifle", 3, 5, 3, [25,20,18,16,14,12,10,8,6,4,2,0,0,0,0,0,0,0,0,0,-5,-10,-15,-20,-25,-30], 0, 2)
    wep_shotgun = soldier.Weapon("Shotgun", 4, 7, 3, [45,40,32,24,16,8,4,0,0,-4,-8,-16,-32,-40,-70,-80,-90,-100], 20, 3)
    wep_sniper = soldier.Weapon("Sniper Rifle", 4, 6, 3, [-35,-30,-27,-24,-21,-18,-15,-12,-9,-6,-3,0,0,0,0,0,0,0,0,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10], 10, 3, True)

    soldiers = []
    soldiers.append([])
    soldiers.append([])

    for i in range(0,board1.width):
        for j in range(0,board1.height):
            exec(compile(open("soldier.txt", "rb").read(), "soldier.txt", 'exec'))
            #exec(compile(open("map.txt", "rb").read(), "map.txt", 'exec'))

    screen = pygame.display.set_mode(((helper.getResolution()+4)*board1.width, (helper.getResolution()+4)*board1.height))


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



    # Initialize time for checking click
    x = 0
    y = 0
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

    def resetBoard():
        nonlocal board1, renderer, controller, count, srcTile, desTile, ID, currentTile \
        ,displayHover, currentSide, wep_sniper, wep_assault, wep_shotgun, soldiers
        f = open("map.txt")
        tiles = {}
        for line in f.readlines():
            cols = line.split()
            passable = (cols[2] == "True")
            tiles[(int(cols[0]),int(cols[1]))] = board.Tile((int(cols[0]), int(cols[1])), passable, int(cols[3]), int(cols[4]), int(cols[5]), int(cols[6]))

        #print(tiles)
        board1 = board.Board(15,20, tiles)
        for i in range(0,board1.width):
            for j in range(0,board1.height):
                exec(compile(open("soldier.txt", "rb").read(), "soldier.txt", 'exec'))
#                 exec(compile(open("map.txt", "rb").read(), "map.txt", 'exec'))

        print ("HI!")

        renderer = Renderer.Renderer(board1,screen)
        controller = Controller.Controller()
        count = 0

        srcTile = None
        desTile = None
        ID = None

        currentTile = None
        displayHover = 0
        currentSide = 0
        
        
        
    testList = dummyAI.dangerBoard(board1, soldiers, currentSide, soldiers[currentSide][0])
    for i in range(0,board1.width):
        for j in range(0,board1.height):
            print("%8.2f " % testList[i][j], end = "")
        
  
    print("NS")  
    print(testList[19][13])
    print(testList[17][12])
    
    try:
        while 1:
            if mode == 1:
                event = pygame.event.wait()

            else:
                event = pygame.event.poll()

            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    print("XCOM wins: " + str(xcomwin))
                    print("ALIENS wins: " + str(alienwin))
                    break
            if mode == 1 or mode ==2:
                coord2 = pygame.mouse.get_pos()
                currentTile = controller.getTile(board1, coord2)
                displayHover = eventHandler.hoverDisplay(displayHover, currentTile, currentSide, myfont, renderer, count, board1)

            if mode == 3 and level == 1:
                if level == 1:
                    if currentSide == 0:
                        dummyAI.improvedRandomExecution(board1,soldiers,currentSide)
                        srcTile = dummyAI.srcTile
                        desTile = dummyAI.desTile
                        ID = dummyAI.ID
                else:
                    if currentSide == 0:
                        dummyAI.execution(board1,soldiers,currentSide)
                        srcTile = dummyAI.srcTile
                        desTile = dummyAI.desTile
                        ID = dummyAI.ID
            if (mode == 2 or mode == 3):
                if level == 1:
                    if currentSide == 1:
                        dummyAI.improvedRandomExecution(board1,soldiers,currentSide)
                        srcTile = dummyAI.srcTile
                        desTile = dummyAI.desTile
                        ID = dummyAI.ID
                else:
                    if currentSide == 1:
                        dummyAI.execution(board1,soldiers,currentSide)
                        srcTile = dummyAI.srcTile
                        desTile = dummyAI.desTile
                        ID = dummyAI.ID
            if mode == 1 or mode == 2:
                if pygame.mouse.get_pressed()[0]:
                    if ((time.time() - x) > 0.5):
                        x = time.time()

                        #print ("You have opened a chest!")
                        count, srcTile, desTile = eventHandler.mouseButtonHandler(count, controller, board1, soldiers, currentSide, renderer, srcTile, desTile)
                            #board2 = controller.makemove(board1, coord1,coord2)

                    else:
                        print("you pressed too fast")
                        #coord = pygame.mouse.get_pos()
                if event.type == pygame.KEYDOWN:
                    if (count == 1)or(count == 2):
                        if ((time.time() - y) > 0.5):
                            y = time.time()
                            count, ID, srcTile, desTile = eventHandler.buttonActionHander(event, controller, srcTile, renderer, board1, desTile)
    #                             possibleTiles = controller.possibleTiles(board1, srcTile, ID)
    #                         renderer.renderPossibleTiles(possibleTiles)
                        else:
                            print("you press too fast")
            if mode == 3:
                if (srcTile == None):
                    if currentSide == 1:
                        currentSide = 0
                        print("XCOM's Turn")
                    else:
                        currentSide = 1
                        print("Alien's Turn")
                    for u in soldiers[currentSide]:
                        u.actionPoints = 2

            if mode == 2:
                if (srcTile == None):
                    if currentSide == 1:
                        currentSide = 0
                        print("XCOM's Turn")
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
                resetBoard()
            elif helper.checkWinCondition(board1)==1:
                print("XCOM noob, Alien win")
                alienwin = alienwin+1
                resetBoard()

            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
