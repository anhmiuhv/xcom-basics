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
        self.render(self.board)

    def render(self, board):
        dummy = pygame.Surface(self.screen.get_size())
        dummy = dummy.convert()
        dummy.fill((255,255,255))
        papixel = pygame.Surface((helper.getResolution(),helper.getResolution()))
        papixel = papixel.convert()
        papixel.fill((255, 255, 255))
        
        wall = helper.load_image('wall.png').convert()
        transColor = wall.get_at((0,0))
        wall.set_colorkey(transColor)
        #blank = pygame.Surface((60,60))
        #blank = papixel.convert()
        #blank.fill((255, 255, 255))
        #pygame.draw.rect(blank, (50,140,200), (0,0,60,60), 2)
        self.board = board
        for j in range(0,self.board.height):
            for i in range(0,self.board.width):
                blank = pygame.Surface((helper.getResolution()+4,helper.getResolution()+4))
                blank = blank.convert()
                blank.fill((255, 255, 150))
                #pygame.draw.rect(blank, (50,140,200), (0,0,60,60), 2)
                res = helper.getResolution()
                if (self.board.tiles[i][j].coverN == 1):
                    pygame.draw.line(blank, (50,140,200), (0,0), (res,0), 4)
                    
                if (self.board.tiles[i][j].coverS == 1):
                    pygame.draw.line(blank, (50,140,200), (0,res+2), (res,res+2), 4)
                    
                if (self.board.tiles[i][j].coverW == 1):
                    pygame.draw.line(blank, (50,140,200), (0,0), (0,res+2), 4)
                    
                if (self.board.tiles[i][j].coverE == 1):
                    pygame.draw.line(blank, (50,140,200), (res+2,0), (res+2,res), 4)
                    
                    
        #self.coverN = coverN
        #self.coverE = coverE
        #self.coverS = coverS
        #self.coverW = coverW
                
                if (self.board.tiles[i][j].unit != None):
                    blank.blit(self.board.tiles[i][j].unit.image, (2,2))
                    #test = 1
                elif(self.board.tiles[i][j].passable == False):
                    blank.blit(wall, (2,2))
                else:    
                    blank.blit(papixel, (2,2))
                    
                dummy.blit(blank, (i*(res+4),j*(res+4)))

        
        #Display The Background
        
        self.screen.blit(dummy, (0, 0))
        self.background = dummy
        
        pygame.display.flip()
    
    def renderPossibleTiles(self,possibleTiles):
        self.render(self.board)
        #print("possibleTile")
        dummy = pygame.Surface(self.screen.get_size())
        dummy = dummy.convert()
        dummy.fill((255,255,255))
        dummy.set_alpha(75)
        res = helper.getResolution()
        for tile in possibleTiles: 
            cover = pygame.Surface((res,res))
            cover = cover.convert()
            cover.fill((0, 140, 255))
            cover.set_alpha(75)
            dummy.blit(cover, (tile.coords[0]*(res+4),tile.coords[1]*(res+4)))
            
        self.background.blit(dummy, (0,0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
            