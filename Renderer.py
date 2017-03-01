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

unitImage = {}

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

        pa = helper.load_image('papixel.png').convert()
        transColor = pa.get_at((0,0))
        pa.set_colorkey(transColor)
        pa = pygame.transform.scale(pa, (helper.getResolution(), helper.getResolution()))
        #picture = pygame.transform.scale(picture, (1280, 720))
        ns = helper.load_image('ns.png').convert()
        transColor = ns.get_at((0,0))
        ns.set_colorkey(transColor)
        ns = pygame.transform.scale(ns, (helper.getResolution(), helper.getResolution()))
        unitImage["pa"] = pa
        unitImage["ns"] = ns

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
                if (self.board.tiles[i][j].coverN != 0):
                    pygame.draw.line(blank, (128,self.board.tiles[i][j].coverN / 50 * 255, 0), (0,0), (res,0), 4)

                if (self.board.tiles[i][j].coverS != 0):
                    pygame.draw.line(blank, (128,self.board.tiles[i][j].coverS / 50 * 255, 0), (0,res+2), (res,res+2), 4)

                if (self.board.tiles[i][j].coverW != 0):
                    pygame.draw.line(blank, (128,self.board.tiles[i][j].coverW / 50 * 255, 0), (0,0), (0,res+2), 4)

                if (self.board.tiles[i][j].coverE != 0):
                    pygame.draw.line(blank, (128,self.board.tiles[i][j].coverE / 50 * 255, 0), (res+2,0), (res+2,res), 4)


        #self.coverN = coverN
        #self.coverE = coverE
        #self.coverS = coverS
        #self.coverW = coverW

                if (self.board.tiles[i][j].unit != None):
                    blank.blit(unitImage[self.board.tiles[i][j].unit.image], (2,2))
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

    def renderHover(self, tile, myfont):

        dummy = pygame.Surface(self.screen.get_size())
        dummy = dummy.convert()
        dummy.fill((255,255,255))
        dummy.set_alpha(75)
        res = helper.getResolution()

        hover = pygame.Surface(((res+4)*3,(res+4)*3))
        hover = hover.convert()
        hover.fill((140, 255, 255))
        #hover.set_alpha(75)

        unit = tile.unit
#         self.health = health
#         self.mobility = mobility
#         self.aim = aim
#         self.side = side
#         self.actionPoints = 2
        nametext = myfont.render('Name: ' + unit.name, True, (0,0,0))
        hover.blit(nametext,(0,0))
        weapontext = myfont.render('Weapon: ' + unit.weapon.name, True, (0,0,0))
        hover.blit(weapontext,(0,helper.getTextSize()))
        ammotext = myfont.render('Ammo: ' + str(unit.weapon.ammo), True, (0,0,0))
        hover.blit(ammotext,(0,2*helper.getTextSize()))
        coordstext = myfont.render('Coords: ( ' + str(unit.coords[0]) + ', ' + str(unit.coords[1]) + ')', True, (0,0,0))
        hover.blit(coordstext,(0,3*helper.getTextSize()))
        healthtext = myfont.render('Health: ' + str(unit.health), True, (0,0,0))
        hover.blit(healthtext,(0,4*helper.getTextSize()))
        mobilitytext = myfont.render('Mobility: ' + str(unit.mobility), True, (0,0,0))
        hover.blit(mobilitytext,(0,5*helper.getTextSize()))
        aimtext = myfont.render('Aim: ' + str(unit.aim), True, (0,0,0))
        hover.blit(aimtext,(0,6*helper.getTextSize()))
        sidetext = myfont.render('Side: ' + str(unit.side), True, (0,0,0))
        hover.blit(sidetext,(0,7*helper.getTextSize()))
        actionPointstext = myfont.render('Action Point: ' + str(unit.actionPoints), True, (0,0,0))
        hover.blit(actionPointstext,(0,8*helper.getTextSize()))
        xpos = 0
        ypos = 0
        if (tile.coords[0] < self.board.width/2):
            xpos = res
        else:
            xpos = - 3*res
        if (tile.coords[1] < self.board.height/2):
            ypos = res
        else:
            ypos = - 3*res

        self.background.blit(hover, (tile.coords[0]*(res+4)+xpos,tile.coords[1]*(res+4)+ypos))
        #self.background.blit(dummy, (0,0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()


