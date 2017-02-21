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
	def __init__(self,board):
		
	    self.board = board
	    self.screen = pygame.display.set_mode((60*board.width+20, 60*board.height+20))
	    

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
		for dummyTile in self.board.tiles:
			
			self.background.blit(dummyTile.unit.image, (dummyTile.coords[0]*60,dummyTile.coords[1]*60))
		#Display The Background
	    
		self.screen.blit(self.background, (0, 0))
		pygame.display.flip()
    