from typing import Set
from setup import Setup
from game_loop import run_game_loop

run_game_loop(Setup.create())

Setup.destroy()