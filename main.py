import pygame, sys
from pygame.locals import *
from constants import *
print("hello world")

pygame.init()
DISPLAYSURF = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("hello world")

DISPLAYSURF.fill((120,80,80))
pygame.draw.rect(DISPLAYSURF,(0,0,255), (0,0,WIDTH, SKY_HEIGHT))

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            print("end of game")
            sys.exit()
    pygame.display.update()

