import board
import math
import copy
import random
import helper

class Controller:
    def __init__(self):
        self.nothing = "nothing"

    # probably obsolete after more stuff gets added
    def makemove(self, board,mouse1, mouse2):
        coord1 = []
        coord1.append(int(math.floor(mouse1[0]/(helper.getResolution()+4))))
        coord1.append(int(math.floor(mouse1[1]/(helper.getResolution()+4))))


        coord1.append(int(math.floor(mouse2[0])/(helper.getResolution()+4)))
        coord1.append(int(math.floor(mouse2[1])/(helper.getResolution()+4)))

        #if (board.tiles[coord1[0]][coord1[1]].unit != None)&(board.tiles[coord1[2]][coord1[3]].unit != None):

        dummyUnit = copy.copy(board.tiles[coord1[0]][coord1[1]].unit)
        board.tiles[coord1[0]][coord1[1]].unit = copy.copy(board.tiles[coord1[2]][coord1[3]].unit)
        board.tiles[coord1[2]][coord1[3]].unit = dummyUnit

        return board

    def getTile(self, board, mouse):
        coord1 = []
        coord1.append(int(math.floor(mouse[0]/(helper.getResolution()+4))))
        coord1.append(int(math.floor(mouse[1]/(helper.getResolution()+4))))
        return board.tiles[coord1[0]][coord1[1]]

    # id = 1: move (1 action)
    # id = 2: dash (2 actions)
    # id = 3: shoot (1 action, turn-ending)
    # id = 4: reload (1 action)
    def possibleAction(self, srcTile):
        l = []
        # can't act if dead or no moves left
        if srcTile.unit.health <= 0 or srcTile.unit.actionPoints <= 0:
            return l
        l.append(1)
        if srcTile.unit.actionPoints == 2:
            l.append(2)
        if srcTile.unit.weapon.ammo > 0:
            l.append(3)
        if srcTile.unit.weapon.ammo < srcTile.unit.weapon.magSize:
            l.append(4)
        return l

    # possible target tiles for action
    def possibleTiles(self, board, srcTile, ID):
        l = []
        if ID == 1:
            cameFrom, cost_so_far = board.moveDistance(srcTile, srcTile.unit.mobility)
            for t in cost_so_far:
                l.append(t)
        if ID == 2:
            cameFrom, cost_so_far = board.moveDistance(srcTile, srcTile.unit.mobility * 2)
            for t in cost_so_far:
                l.append(t)
        if ID == 3:
            for i in range(0, board.width):
                for t in board.tiles[i]:
                    if t.unit != None and t.unit.side != srcTile.unit.side:
                        l.append(t)
        if ID == 4:
            l.append(srcTile)
        return l

    # this presumes that possibleTiles and possibleActions are valid, and makes no checking attempt
    # updates board, returns a message indicating outcome
    def performAction(self, board, srcTile, desTile, ID):
        msg = ""
        possibleTiles = self.possibleTiles(board, srcTile, ID)
        action = False
        for tile in possibleTiles:
            if (tile.coords == desTile.coords):
                action = True
                
        if action:
            if ID == 1 or ID == 2:
                srcTile.unit.actionPoints -= ID
                desTile.unit = srcTile.unit
                srcTile.unit = None
            if ID == 3:
                srcTile.unit.actionPoints = 0
                hitChance = srcTile.unit.aim
                cover = board.coverValue(srcTile, desTile)
                if (cover <= 0): # flanking gets a 40% bonus
                    hitChance += 40
                else: # if not flanking then aiming chance reduced by cover
                    hitChance -= cover
                # range modifiers; weapons do better at close range and worse faraway
                hitChance += srcTile.unit.weapon.rangeMod[int(board.straightDistance(srcTile, desTile))]
                # RNGESUS COMETH
                if random.randint(0, 100) <= hitChance:
                    damage = random.randint(srcTile.unit.weapon.minDamage, srcTile.unit.weapon.maxDamage)
                    desTile.unit.health -= damage
                    srcTile.unit.weapon.ammo -= 1
                    msg = "Hit: " + str(hitChance) + "% chance, " + str(damage) + " damage dealt."
                else:
                    msg = "Missed: " + str(hitChance) + "% chance."
            if ID == 4:
                srcTile.unit.actionPoints -= 1
                srcTile.unit.weapon.ammo = srcTile.unit.weapon.magSize
                msg = "Weapon reloaded."
                
        else: 
            msg = "You click on the wrong tile you noob!"
        return msg

