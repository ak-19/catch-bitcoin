from typing import Set
from setup import Setup
from game_loop import GameLoop

GameLoop(Setup.create()).run_game_loop()

Setup.destroy()