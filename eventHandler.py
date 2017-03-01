import pygame
import board
def hoverDisplay(displayHover, currentTile, currentSide, myfont, renderer, count, board1):
    if (currentTile.unit !=None):
        if displayHover == 3:
            displayHover = 1
    else:
        if displayHover == 2:
            displayHover = 0

    if displayHover == 1:
        print ("mouse is over 'unit'")
        renderer.renderHover(currentTile,myfont)
        displayHover = 2
        print(currentSide)

    elif(displayHover == 0):
        print("mouse is not on unit anymore")
        if count == 0:
            renderer.render(board1)
            displayHover = 3
            print(currentSide)

    return displayHover

def mouseButtonHandler(count, controller, board1, soldiers, currentSide, renderer, srcTile, desTile):
    if (count == 0):

        coord1 = pygame.mouse.get_pos()
        srcTile = controller.getTile(board1, coord1)

        if (srcTile.unit != None and srcTile.unit in soldiers[currentSide] and srcTile.unit.actionPoints > 0):
            print(str(srcTile.unit.actionPoints))
            count = count + 1
            print("got it")
            renderer.renderPossibleTiles([srcTile])
        else:
            count = 0
            print("You do not click on an unit nooob!")

    elif(count == 2):
        print("destination receive")
        coord2 = pygame.mouse.get_pos()
        desTile = controller.getTile(board1, coord2)

        count = 0

    return count, srcTile, desTile

def buttonActionHander(event, controller, srcTile ,renderer, board1, desTile):
    possibleTiles = []
    count = 1
    ID = None
    if event.key == pygame.K_ESCAPE or event.unicode == '1':
        if 1 in controller.possibleAction(srcTile):
            print("move")
            ID = 1
            count = 2
            possibleTiles = controller.possibleTiles(board1, srcTile, ID)
            renderer.renderPossibleTiles(possibleTiles)
    if event.key == pygame.K_ESCAPE or event.unicode == '2':
        if 2 in controller.possibleAction(srcTile):
            print("dash")
            ID = 2
            count = 2
            possibleTiles = controller.possibleTiles(board1, srcTile, ID)
            renderer.renderPossibleTiles(possibleTiles)
    if event.key == pygame.K_ESCAPE or event.unicode == '3':
        if 3 in controller.possibleAction(srcTile):
            print("shoot")
            ID = 3
            count = 2
            possibleTiles = controller.possibleTiles(board1, srcTile, ID)
            renderer.renderPossibleTiles(possibleTiles)
    if event.key == pygame.K_ESCAPE or event.unicode == '4':
        if 4 in controller.possibleAction(srcTile):
            print("reload")
            ID = 4
            desTile = board.Tile((100,100))
            print(controller.performAction(board1, srcTile, desTile, ID))
            desTile = None
            srcTile = None
            ID = None
            count = 0
            renderer.render(board1)
    #    possibleTiles = controller.possibleTiles(board1, srcTile, ID)
    #renderer.renderPossibleTiles(possibleTiles)
    return count, ID, srcTile, desTile


