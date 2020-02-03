import pygame
font = pygame.font.Font('font.ttf', 20)
class Card(pygame.sprite.Sprite):
    def __init__(self, color, num):
        pygame.sprite.Sprite().__init__()
        surf = font.render(num, color = (color))
        surf.fill((255, 255, 255))
        self.image = surf
        self.rect = self.image.get_rect()
        self.rect.topleft = (1900, 620)
    def move(self, x, y):
        self.rect.topleft = (x, y)
    def remove(self):
        self.remove()