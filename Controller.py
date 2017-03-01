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

    # id = 0: do nothing (turn-ending)
    # id = 1: move (1 action)
    # id = 2: dash (2 actions)
    # id = 3: shoot (1 action, turn-ending)
    # id = 4: reload (1 action)
    def possibleAction(self, srcTile):
        l = []
        # can't act if dead or no moves left
        if srcTile.unit.health <= 0 or srcTile.unit.actionPoints <= 0:
            return l
        l.append(0)
        l.append(1)
        if srcTile.unit.actionPoints == 2:
            l.append(2)
        if (srcTile.unit.weapon.ammo > 0) and (not srcTile.unit.weapon.heavy or srcTile.unit.actionPoints == 2):
            l.append(3)
        if srcTile.unit.weapon.ammo < srcTile.unit.weapon.magSize:
            l.append(4)
            #print("test")
        return l

    # possible target tiles for action
    def possibleTiles(self, board, srcTile, ID):
        l = []
        if ID == 1:
            cameFrom, cost_so_far = board.moveDistance(srcTile, srcTile.unit.mobility)
            for t in cost_so_far:
                if t.unit == None:
                    l.append(t)
        if ID == 2:
            cameFrom, cost_so_far = board.moveDistance(srcTile, srcTile.unit.mobility * 2)
            for t in cost_so_far:
                if t.unit == None:
                    l.append(t)
        if ID == 3:
            for i in range(0, board.width):
                for t in board.tiles[i]:
                    if t.unit != None and t.unit.side != srcTile.unit.side:
                        l.append(t)
        if ID == 4 or ID == 0:
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
        if ID == 4 or ID == 0:
            action = True
        if action:
            if ID == 1 or ID == 2:
                srcTile.unit.actionPoints -= ID
                desTile.unit = srcTile.unit
                srcTile.unit = None
                if ID == 1:
                    print("Move Successful")
                else:
                    print("Dash Successful")
            if ID == 3:
                srcTile.unit.actionPoints = 0
                hitChance = srcTile.unit.aim - desTile.unit.defense
                critChance = srcTile.unit.weapon.critChance
                dodgeChance = desTile.unit.dodge
                cover = board.coverValue(srcTile, desTile)
                if (cover <= 0): # flanking gets a 40% bonus to crit chance
                    critChance += 40
                else: # if not flanking then aiming chance reduced by cover
                    hitChance -= cover
                # range modifiers; weapons do better at close range and worse faraway
                dis = int(board.straightDistance(srcTile, desTile))
                if dis >= len(srcTile.unit.weapon.rangeMod):
                    dis = len(srcTile.unit.weapon.rangeMod) - 1
                hitChance += srcTile.unit.weapon.rangeMod[dis]
                # RNGESUS COMETH
                # Long War 2 calculation for maximum RNGesus
                # 0 = miss, 1 = graze (50% damage), 2 = hit, 3 = crit
                damageType = 0
                num = random.randint(0, 100)
                critnum = random.randint(0, 100)
                dodgenum = random.randint(0, 100)
                if num <= hitChance - 10:
                    damageType = 2
                elif num <= hitChance + 10:
                    damageType = 1
                else:
                    damageType = 0
                if damageType > 0:
                    if critnum <= critChance:
                        damageType += 1
                    if dodgenum <= dodgeChance:
                        damageType -= 1
                    if damageType <= 0:
                        damageType = 1
                    elif damageType > 3:
                        damageType = 3
                    damage = random.randint(srcTile.unit.weapon.minDamage, srcTile.unit.weapon.maxDamage)
                    if (damageType == 3):
                        damage += srcTile.unit.weapon.critDamage
                        msg = "Crit: "
                    elif (damageType == 1):
                        damage /= 2
                        msg = "Grazed: "
                    else:
                        msg = "Hit: "
                    desTile.unit.health -= damage
                    if (desTile.unit.health <= 0):
                        desTile.unit = None
                    srcTile.unit.weapon.ammo -= 1
                    msg = msg + str(hitChance) + "% Hit " + str(critChance) + "% Crit " + str(dodgeChance) + "% Dodge, " + str(damage) + " damage dealt."
                    if desTile.unit == None:
                        msg = msg + "  ... and your target die"
                else:
                    msg = "Missed: " + str(hitChance) + "% chance."
            if ID == 4:
                srcTile.unit.actionPoints -= 1
                srcTile.unit.weapon.ammo = srcTile.unit.weapon.magSize
                msg = "Weapon reloaded."
            if ID == 0:
                srcTile.unit.actionPoints = 0
                msg = "Done nothing."

        else:
            msg = "You click on the wrong tile you noob!"
        return msg


    def dangerScore(self, board, tile, srcTile, defunit):
        hitChance = srcTile.unit.aim - defunit.defense
        critChance = srcTile.unit.weapon.critChance
        dodgeChance = defunit.dodge
        cover = board.coverValue(srcTile, tile)
        if (cover <= 0): # flanking gets a 40% bonus to crit chance
            critChance += 40
        else: # if not flanking then aiming chance reduced by cover
            hitChance -= cover
        # range modifiers; weapons do better at close range and worse faraway
        dis = int(board.straightDistance(srcTile, tile))
        if dis >= len(srcTile.unit.weapon.rangeMod):
            dis = len(srcTile.unit.weapon.rangeMod) - 1
        hitChance += srcTile.unit.weapon.rangeMod[dis]
        # RNGESUS COMETH
        # Long War 2 calculation for maximum RNGesus
        # 0 = miss, 1 = graze (50% damage), 2 = hit, 3 = crit
       
        damage = (srcTile.unit.weapon.minDamage + srcTile.unit.weapon.maxDamage) / 2 * hitChance / 100
            
        damage += srcTile.unit.weapon.critDamage * critChance / 100
        damage -= damage * dodgeChance / 100
        return damage
        
                