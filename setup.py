import pygame

from screen import Screen

class Setup:
    @staticmethod
    def create():
        pygame.init()
        return pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))

    @staticmethod
    def destroy():
        pygame.quit()    
