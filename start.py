import pygame
import sys
from pygame.locals import *
import stage
bgcolor = (0, 128, 0)
pygame.init()
display = pygame.display.set_mode((1920, 1280))
pygame.display.set_caption('UNO Cards V0.1')
display.fill(bgcolor)
group = pygame.sprite.Group()
group.add(stage.Stage())
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE: 
                pygame.quit()
                sys.exit()
    pygame.display.update()
