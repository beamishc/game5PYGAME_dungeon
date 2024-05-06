import pygame
import json
import sys
from classes.game_class import Game
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
    save_dct = json.load(f)

save_file = save_dct[sys.argv[1]]

current_lvl = save_file["CURRENT_LEVEL"]

# initialise game
pygame.init()

for lvl in [x for x in lvls.keys() if int(x) >= current_lvl]:
    ic.enable()
    ic(lvl)
    game_lvl = Game(lvl, lvls[lvl], save_file)
    did_win = game_lvl.run_game_loop()
    save_dct[sys.argv[1]] = game_lvl.save_file
    if did_win == False:
        break

ic(save_dct)

with open('save_file.json', 'w') as f:
    json.dump(save_dct, f)


# end game
pygame.quit()
quit()
