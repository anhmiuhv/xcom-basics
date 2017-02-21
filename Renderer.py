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

class Renderer():
    def __init__(self,board,screen):
        
        self.board = board
        self.screen = screen
        

        #Create The Backgound
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((255, 255, 255))
        #test character
        self.papixel = helper.load_image('papixel.png').convert()
        transColor = self.papixel.get_at((0,0))
        self.papixel.set_colorkey(transColor)
        
        #add character to background
        self.background.blit(self.papixel,(500,500))



        #Display The Background
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def render(self):
        dummy = pygame.Surface(self.screen.get_size())
        dummy = dummy.convert()
        dummy.fill((255,255,255))
        papixel = pygame.Surface((60,60))
        papixel = papixel.convert()
        papixel.fill((255, 0, 0))
        papixel2 = pygame.Surface((60,60))
        papixel2 = papixel.convert()
        papixel2.fill((0, 255, 0))
        for j in range(0,self.board.height):
            for i in range(0,self.board.width):
                if (self.board.tiles[i][j].unit != None):
                    dummy.blit(self.board.tiles[i][j].unit.image, (i*60,j*60))
                else: 
                    dummy.blit(papixel, (i*60,j*60))
        #Display The Background
        
        self.screen.blit(dummy, (0, 0))
        self.background = dummy
        print("test")
        pygame.display.flip()
    