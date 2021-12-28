import pygame

def run_loop_state():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True

def run_game_loop(display):
    run_loop = True
    while run_loop:
        run_loop = run_loop_state()
