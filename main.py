#!/usr/bin/env python

import random, os.path
import copy
import board
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


    tiles = []
    papixel = pygame.Surface((60,60))
    papixel.fill((255, 0, 0))
    wep_assault = soldier.Weapon("Assault Rifle", 3, 5, 3, [25,20,18,16,14,12,10,8,6,4,2,0])
    for i in range(0,6):
        for j in range(0,6):
            unit = soldier.Soldier("Julian", copy.copy(wep_assault), (5,5))
            unit.set_image(papixel)
            tile = board.Tile(coords=(i,j),unit = unit)
            tiles.append(tile)

    board1 = board.Board(10,15,tiles=tiles)

    renderer = Renderer.Renderer(board1)
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
                renderer.render()
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()
