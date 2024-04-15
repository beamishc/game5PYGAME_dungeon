import pygame
import json
import sys
from game_class import Game
from icecream import ic

# RGB color codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# define the clock
clock = pygame.time.Clock()

ic(sys.argv[1])

with open("lvls.json") as f:
    lvls = json.load(f)

with open('save_file.json') as f:
    save_file = json.load(f)[sys.argv[1]]

current_lvl = save_file["CURRENT_LEVEL"]

# initialise game
pygame.init()

for lvl in [x for x in lvls.keys() if int(x) >= current_lvl]:
    ic(lvl)
    game_lvl = Game(lvls[lvl], save_file)
    game_lvl.run_game_loop(1)


# end game
pygame.quit()
quit()
