import pygame
from random import randint
from pygame import constants
from pygame.constants import K_UP
from pygame.display import update
from bitcoin import Bitcoin
from constants import Constants
from colors import Colors
from man import Man
from screen import Screen


class GameLoop:
    def __init__(self, display):
        self.display = display
        self.score = 0
        self.lives = 5
        self.player_lives = Constants.PLAYER_STARTING_LIVES
        self.player_velocity = Constants.PLAYER_VELOCITY
        self.coin_velocity = Constants.COIN_START_VELOCITY
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.font = pygame.font.Font('assets/BlackgroundsRegular.ttf', 32)
        self.endgame_font = pygame.font.Font('assets/BlackgroundsRegular.ttf', 72)

        self.miss_sound = pygame.mixer.Sound('assets/miss.wav')
        self.pickup_sound = pygame.mixer.Sound('assets/pickup.wav')
        self.loss_sound = pygame.mixer.Sound('assets/loss.wav')
        pygame.mixer.music.load('assets/draft-monk-ambience.mp3')
        pygame.mixer.music.play(-1)

        self.man = Man(30,100)
        self.make_new_coin()

    def make_new_coin(self):
        self.coin = Bitcoin(Screen.WIDTH - 32, randint(60, Screen.HEIGHT - 32))

    def run_loop_state(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False              

        if self.lost():   
            self.clock.tick(self.FPS)
            return True

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] and self.man.rect.y > 60:
            self.man.rect.y -= self.player_velocity
        elif pressed[pygame.K_DOWN] and self.man.rect.y < Screen.HEIGHT - 64:
            self.man.rect.y += self.player_velocity

        if self.coin.rect.x - self.coin_velocity < 0:     
            self.lives -= 1       
            self.make_new_coin()
            self.miss_sound.play()        
        else:
            self.coin.rect.x -= self.coin_velocity

        if self.man.rect.colliderect(self.coin.rect):
            self.score += 1
            self.make_new_coin()
            self.pickup_sound.play()
            self.coin_velocity += Constants.COIN_ACCELERATION


        if self.lost():   
            self.loss_sound.play(0)         
            pygame.mixer.music.stop()

        self.draw_objects()

        self.clock.tick(self.FPS)

        return True

    def lost(self):
        if self.lives > 0: return False        
        end = self.endgame_font.render('Game over', False, Colors.GREEN, Colors.DARKGREEN)
        end_rect = end.get_rect()
        end_rect.center = (Screen.WIDTH // 2, Screen.HEIGHT // 2)        
        self.display.blit(end, end_rect)
        pygame.display.update()
        return True

    def draw_objects(self):
        self.draw()
        pygame.display.update()

    def draw(self):
        score_text = self.font.render(f'Score: {self.score}', False, Colors.GREEN, Colors.BLACK)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (20, 20)

        lives_text = self.font.render(f'Lives: {self.lives}', False, Colors.GREEN, Colors.BLACK)
        lives_text_rect = score_text.get_rect()
        lives_text_rect.topright = (Screen.WIDTH - 10, 20)   

        header_text = self.font.render('Ante, catch the bitcoin', False, Colors.YELLOW, Colors.BLACK)
        header_text_rect = header_text.get_rect()
        header_text_rect.topleft = (Screen.WIDTH // 2 - header_text_rect.width//2, 20)        

        self.display.fill(Colors.BLACK)
        self.display.blit(score_text, score_text_rect)
        self.display.blit(lives_text, lives_text_rect)
        self.display.blit(header_text, header_text_rect)
        self.display.blit(self.man.image, self.man.rect)
        self.display.blit(self.coin.image, self.coin.rect)
        pygame.draw.line(self.display, Colors.GREEN, (0, 60), (Screen.WIDTH, 60), width=2)

    def run_game_loop(self):
        run_loop = True
        while run_loop:
            run_loop = self.run_loop_state()
