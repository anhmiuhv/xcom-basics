#!/usr/bin/env python

import random, os.path
import board
import copy
import helper
from Node import Node
import Renderer
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
    screen = pygame.display.set_mode((60*board1.width+20, 60*board1.height+20))

    #tiles = {}
    # papixel = pygame.Surface((60,60))
    # #papixel = papixel.convert()
    # papixel.fill((0, 0, 255))

    papixel = helper.load_image('papixel.png').convert()
    transColor = papixel.get_at((0,0))
    papixel.set_colorkey(transColor)
    wall = helper.load_image('wall.png').convert()
    transColor = wall.get_at((0,0))
    wall.set_colorkey(transColor)
    ns = helper.load_image('ns.png').convert()
    transColor = ns.get_at((0,0))
    ns.set_colorkey(transColor)
   
    blank = pygame.Surface((60,60))
    blank = papixel.convert()
    blank.fill((255, 255, 255))
    wep_assault = soldier.Weapon("Assault Rifle", 3, 5, 3, [25,20,18,16,14,12,10,8,6,4,2,0])
    for i in range(0,board1.width):
        for j in range(0,board1.height):
            unit = soldier.Soldier("Julian", copy.copy(wep_assault), (i,j))
            if (i==5)&(j==7):
                unit.set_image(papixel)
            elif (i==1)&(j==2):
                unit.set_image(ns)
            elif (i == 4):
                unit.set_image(wall)
            elif (i == 7):
                unit.set_image(wall)
            elif (j == 4):
                unit.set_image(wall)
            else:
                unit.set_image(blank)
            board1.tiles[i][j].unit = unit

    renderer = Renderer.Renderer(board1,screen)
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
                renderer.render(board1)
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()