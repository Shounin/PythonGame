__author__ = 'Soffía & Styrmir'
import pygame, sys, os, random
from pygame.locals import *


#Colors
BLACK = (0, 0, 0)
BETTERBLUE = (12,  64, 142)
WHITE = (255, 255, 255)
RED = (255,   0,   0)

#Setup
BACKGROUND_COLOR = BLACK
BG_PIC = pygame.image.load(os.path.join('img', 'duckling.jpg'))
BG_PIC = pygame.transform.scale(BG_PIC, (500, 600))
SURFACE = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Hvar er Hjalti?')

#FPS Cap
FPS = 30
fpsClock = pygame.time.Clock()

#An object for each card on the screen
class Box:
    visible = True
    symbol_visible = False
    color = BETTERBLUE
    size = 98
    locationX = 0
    locationY = 0
    picture = 0
    pictureLocation = ''

    def __init__(self, location, picture):
        self.locationX = location[0]
        self.locationY = location[1]
        self.pictureLocation = picture
        self.picture = pygame.image.load(picture)
        self.picture = pygame.transform.scale(self.picture, (self.size, self.size))

    def draw(self):
        pygame.draw.rect(SURFACE, self.color, (self.locationX, self.locationY, self.size, self.size), 0)

    def display_symbol(self):
        SURFACE.blit(self.picture, (self.locationX, self.locationY))


#Find out whether coordinates of mouse click are contained within specific box
def inBox(mouseCoord, boxCoord):
    return ((mouseCoord[0] - boxCoord[0]) >= 0 and (mouseCoord[0] - boxCoord[0]) < 100) and \
           ((mouseCoord[1] - boxCoord[1]) >= 0 and (mouseCoord[1] - boxCoord[1]) < 100)


#Compare two symbols, can't have the same location
def isSamePic(first_box, second_box):
    return first_box.pictureLocation == second_box.pictureLocation and \
           ((first_box.locationX is not second_box.locationX) or \
           (first_box.locationY is not second_box.locationY))


def main():
    counter = 0

    #Initialize list of symbols
    symbolsList = []
    for dirName, subDir, fileList in os.walk(os.path.join('img', 'alph')):
        for file in fileList:
            symbolsList.append(os.path.join(dirName, file))
            symbolsList.append(os.path.join(dirName, file))
    random.shuffle(symbolsList)

    #Initialize Boxes
    boxes = []
    first_box = 0
    first_move = True
    very_first_move = True

    for i in range(0, 800, 100):
        for j in range(0, 600, 100):
            boxes.append(Box((i, j), symbolsList.pop()))

    pygame.init()

    #Sounds
    bubble = pygame.mixer.Sound(os.path.join('audio', 'Bubble.wav'))
    applause = pygame.mixer.Sound(os.path.join('audio', 'Quack.wav'))
    tick = pygame.mixer.Sound(os.path.join('audio', 'Tick.wav'))

    #initialize winning text
    fontObj = pygame.font.SysFont('arial', 68, True)
    textSurfaceObj = fontObj.render('Þú fannst Hjalta!', True, RED, BLACK)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (400, 300)

    textSurfaceObj2 = fontObj.render('Hvar er Hjalti?', True, RED, BLACK)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (400, 300)

    #Main game loop
    while True:
        SURFACE.fill(BLACK)
        SURFACE.blit(BG_PIC, (150, 0))

        #Display all symbols on game start
        if very_first_move:
            for x in boxes:
                x.display_symbol()
            pygame.display.update()
            pygame.time.wait(2000)
            for x in boxes:
                x.draw()
            SURFACE.blit(textSurfaceObj2, textRectObj2)
            pygame.display.update()
            pygame.time.wait(2000)
            SURFACE.fill(BLACK)
            SURFACE.blit(BG_PIC, (150, 0))
            for x in boxes:
                x.draw()
            pygame.display.update()
            very_first_move = False

        #Draw boxes
        for x in boxes:
            if x.symbol_visible:
                x.display_symbol()
            elif x.visible:
                x.draw()

        #Main event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                mx, my = pygame.mouse.get_pos()
                for box in boxes:
                    #Find Box containing coordinates of mouse click
                    if inBox((mx, my), (box.locationX, box.locationY)):
                        if box.visible and not box.symbol_visible:
                            tick.play()
                            #If selecting the first card
                            if first_move:
                                box.symbol_visible = True
                                box.display_symbol()
                                first_box = box
                                first_move = False
                            #If selecting the second card
                            else:
                                first_move = True
                                box.symbol_visible = True
                                box.display_symbol()
                                pygame.display.update()
                                pygame.time.wait(500)
                                #If cards contain the same symbol
                                if isSamePic(first_box, box):
                                    counter += 1  #To figure out when the player has won
                                    if counter is not 24:
                                        bubble.play()  #BLUB
                                    first_box.symbol_visible = False
                                    first_box.visible = False
                                    box.symbol_visible = False
                                    box.visible = False
                                    boxes = [x for x in boxes if x.pictureLocation is not box.pictureLocation]
                                else:
                                    first_box.symbol_visible = False
                                    box.symbol_visible = False
        #Win state
        if counter == 24:
            SURFACE.fill(BLACK)
            SURFACE.blit(BG_PIC, (150, 0))
            pygame.display.update()
            SURFACE.blit(textSurfaceObj, textRectObj)
            applause.play()
            pygame.display.update()
            pygame.time.wait(5000)
            pygame.quit()
            sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == '__main__':
    main()
