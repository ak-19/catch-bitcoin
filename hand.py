import pygame

class Hand:
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/hand.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
