import pygame
import json
import sys

from classes.game_class import Game
from functions.check_files import check_files
from icecream import ic

# RGB color codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# define the clock
clock = pygame.time.Clock()

# load all levels dictionaries
with open("teeny_tiny_game/json/lvls.json") as f:
    lvls = json.load(f)

# load all save file dictionaries
with open('teeny_tiny_game/json/save_file.json') as f:
    save_dct = json.load(f)

# check a player name is provided
if len(sys.argv) > 1:
    ic(sys.argv[1])
    save_name = sys.argv[1]

else:
    query = input("New Game?\n")

    # choose an existing player name
    if query == "n":
        save_name = check_files(list(save_dct.keys()))

    # or create a player name
    else:
        new_name = input("Name your player!\n")
        save_dct[new_name.upper()] = {"NAME": new_name.title(),
                                    "CURRENT_LEVEL": 0,
                                    "CURRENT_WEAPON": "",
                                    "CURRENT_HEALTH": 6,
                                    "HIGHEST_LEVEL": 0,
                                    "MAX_HEALTH": 6,
                                    "TIMES_DIED": 0
                                    }
        save_name = new_name.upper()

# access save file and current level for chosen player name
save_file = save_dct[save_name]
current_lvl = save_file["CURRENT_LEVEL"]

# initialise game
pygame.init()

# start game from current level and beyond
for lvl in [x for x in lvls.keys() if int(x) >= current_lvl]:
    # set up game level
    game_lvl = Game(lvl, lvls[lvl], save_file)
    # run game and return success or failure
    did_win = game_lvl.run_game_loop()
    # update save file
    save_dct[save_name] = game_lvl.save_file
    # stop game if player died
    if did_win == False:
        break

ic(save_dct)

# dump save file back to json
with open('teeny_tiny_game/json/save_file.json', 'w') as f:
    json.dump(save_dct, f)


# end game
pygame.quit()
quit()
