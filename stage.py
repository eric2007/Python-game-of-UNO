import pygame
import card
import random
pygame.init()
class Stage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__()
    def init(self):
        self.groups[0]().add(card.Card())
    def getRandomCard(self):
        color = random.randint(1, 4)
        # 10 jing
        # 11 change
        # 12 +2
        num = random.randint(0, 12)
        if color == 1:
            copyright()
        else:
            pass
    def cardFun(self, num):
        self
    