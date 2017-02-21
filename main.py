#!/usr/bin/env python

import random, os.path
import board
import helper
from Node import Node
#import basic pygame modules
import pygame
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
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('XCom - the Unknown Noob')
    pygame.mouse.set_visible(1)

    title = pygame.Surface((60,60))
    title.fill((50,0,0))
    #Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    #test character
    papixel = helper.load_image('papixel.png').convert()
    transColor = papixel.get_at((0,0))
    papixel.set_colorkey(transColor)
    
    node = Node(papixel,500,500)

    #add character to background
    background.blit(node.image,(node.x,node.y))

    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            if pygame.mouse.get_pressed()[0] and node.image.get_rect().move(node.x,node.y).collidepoint(pygame.mouse.get_pos()):
                print ("You have opened a chest!")
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == '__main__':
    main()