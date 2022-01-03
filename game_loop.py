import pygame
from random import randint
from pygame import constants
from pygame.constants import K_UP
from pygame.display import update
from bitcoin import Bitcoin
from constants import Constants
from colors import Colors
from hand import Hand
from screen import Screen


class GameLoop:
    def __init__(self, display):
        self.setup_game(display)

    def setup_game(self, display):
        self.run_loop = True
        self.stopped = False
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

        self.hand = Hand(10,100)
        self.make_new_coin()        

    def make_new_coin(self):
        self.coin = Bitcoin(Screen.WIDTH - 32, randint(60, Screen.HEIGHT - 32))

    def loop_state_transition(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False       
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p and self.stopped:
                self.setup_game(self.display)
                return True 

        if self.stopped:   
            self.draw_end()            
            self.clock.tick(self.FPS)
            return True

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP] and self.hand.rect.y > 60:
            self.hand.rect.y -= self.player_velocity
        elif pressed[pygame.K_DOWN] and self.hand.rect.y < Screen.HEIGHT - self.hand.rect.width:
            self.hand.rect.y += self.player_velocity

        self.process_coin()

        self.check_hand_coin_collision()

        if self.lost():   
            self.loss_sound.play(0)         
            pygame.mixer.music.stop()
            self.stopped = True

        self.draw_objects()

        self.clock.tick(self.FPS)

        return True

    def check_hand_coin_collision(self):
        if self.hand.rect.colliderect(self.coin.rect):
            self.score += 1
            self.make_new_coin()
            self.pickup_sound.play()
            self.coin_velocity += Constants.COIN_ACCELERATION

    def process_coin(self):
        if self.coin.rect.x - self.coin_velocity < 0:     
            self.lives -= 1       
            self.make_new_coin()
            self.miss_sound.play()        
        else:
            self.coin.rect.x -= self.coin_velocity

    def draw_end(self):
        end = self.endgame_font.render('Game over!', False, Colors.GREEN, Colors.DARKGREEN)
        press_play = self.endgame_font.render('Press "P" to play again', False, Colors.GREEN, Colors.DARKGREEN)
        end_rect = end.get_rect()
        press_play_rect = press_play.get_rect()
        end_rect.center = (Screen.WIDTH // 2, Screen.HEIGHT // 2)        
        press_play_rect.center = (Screen.WIDTH // 2, Screen.HEIGHT // 2 + 60)        
        self.display.blit(end, end_rect)
        self.display.blit(press_play, press_play_rect)
        pygame.display.update()        

    def lost(self):
        return self.lives < 1

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

        header_text = self.font.render('Catch the bitcoin', False, Colors.YELLOW, Colors.BLACK)
        header_text_rect = header_text.get_rect()
        header_text_rect.topleft = (Screen.WIDTH // 2 - header_text_rect.width//2, 20)        

        self.display.fill(Colors.BLACK)
        self.display.blit(score_text, score_text_rect)
        self.display.blit(lives_text, lives_text_rect)
        self.display.blit(header_text, header_text_rect)
        self.display.blit(self.hand.image, self.hand.rect)
        self.display.blit(self.coin.image, self.coin.rect)
        pygame.draw.line(self.display, Colors.GREEN, (0, 60), (Screen.WIDTH, 60), width=2)

    def run_game_loop(self):
        while self.run_loop:
            self.run_loop = self.loop_state_transition()
