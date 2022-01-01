import pygame
from constants import Constants
from colors import Colors
from man import Man
from screen import Screen


class GameLoop:
    def __init__(self, display):
        self.display = display
        self.score = 0
        self.player_lives = Constants.PLAYER_STARTING_LIVES
        self.coin_velocity = Constants.COIN_START_VELOCITY
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.font = pygame.font.Font('assets/BlackgroundsRegular.ttf', 32)
        pygame.mixer.music.load('assets/draft-monk-ambience.mp3')
        pygame.mixer.music.play(-1)

        self.man = Man(100,100)

    def run_loop_state(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False                         
            self.clock.tick(self.FPS)

        self.draw_objects()

        return True

    def draw_objects(self):
        self.draw_header()

        pygame.display.update()

    def draw_header(self):
        score_text = self.font.render('Score: 0', False, Colors.GREEN, Colors.BLACK)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (20, 20)

        lives_text = self.font.render('Lives: 5', False, Colors.GREEN, Colors.BLACK)
        lives_text_rect = score_text.get_rect()
        lives_text_rect.topright = (Screen.WIDTH - 10, 20)   

        header_text = self.font.render('catch the bitcoins', False, Colors.YELLOW, Colors.BLACK)
        header_text_rect = header_text.get_rect()
        header_text_rect.topleft = (Screen.WIDTH // 2 - header_text_rect.width//2, 20)        

        self.display.fill(Colors.BLACK)
        self.display.blit(score_text, score_text_rect)
        self.display.blit(lives_text, lives_text_rect)
        self.display.blit(header_text, header_text_rect)
        self.display.blit(self.man.image, self.man.rect)
        pygame.draw.line(self.display, Colors.GREEN, (0, 60), (Screen.WIDTH, 60), width=2)

    def run_game_loop(self):
        run_loop = True
        while run_loop:
            run_loop = self.run_loop_state()
