import pygame

class Setup:
    @staticmethod
    def create():
        pygame.init()
        return pygame.display.set_mode((800, 600))

    @staticmethod
    def destroy():
        pygame.quit()    
