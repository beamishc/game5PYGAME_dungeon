import pygame
import pytmx
import pyscroll
import os
import json
from gameobject_class import GameObject
from playercharacter_class import PC
from nonplayercharacter_class import NPC
from enemy_class import Enemy
from spriteclass import SpriteSheet

# print(pygame.font.get_fonts())

# dung_asset_path = 'assets/kenney_tiny-dungeon/'
bit_asset_sheet_path = 'assets/kenney_1-bit-pack/Tilesheet/colored-transparent_packed.png'
bit_sprite = SpriteSheet(bit_asset_sheet_path, 49, 22, 16, 16, 1)

# RGB color codes
WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)

# define the clock
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('baskerville', 96, bold=True)

class Game:
    # Typical rate of 60 , equivalent to FPS
    TICK_RATE = 60

    def __init__(self, lvl_dct, save_file):
        self.title = lvl_dct['SCREEN_TITLE']
        self.background = lvl_dct['BACKGROUND']
        self.width = eval(lvl_dct['SCREEN_WIDTH'])
        self.height = eval(lvl_dct['SCREEN_HEIGHT'])
        self.player_image = lvl_dct["ASSET_PATH"] + lvl_dct['PRE_PLAYER']
        self.later_player = lvl_dct["ASSET_PATH"] + lvl_dct['PLAYER']
        self.enemy_image = lvl_dct["ASSET_PATH"] + lvl_dct['ENEMIES']
        self.sword_image = lvl_dct["ASSET_PATH"] + lvl_dct['SWORD']
        self.treasure_image = lvl_dct["ASSET_PATH"] + lvl_dct['TREASURE']
        self.health = save_file["HEALTH"]
        self.damage_taken = False

        # create the game screen
        self.game_screen = pygame.display.set_mode((self.width, self.height))

        # create images that need to be converted onto blit
        self.heart = bit_sprite.image_at(10, 39)
        self.halflife = bit_sprite.image_at(10, 41)
        self.heartless = bit_sprite.image_at(10, 40)

        # set the game screen to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(self.title)

        # tmxdata = pytmx.TiledMap(self.background)
        self.gameMap = pytmx.load_pygame(self.background)

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction_up_down = 0
        direction_left_right = 0
        px_h = 16
        px_w = 16

        player_character = PC(self.player_image, 384, 720, px_h, px_w)

        enemy_0 = Enemy(self.enemy_image, 24, 624, px_h, px_w)
        enemy_0.SPEED *= level_speed

        # 'source_files/project_files/treasure.png'
        treasure = GameObject(self.treasure_image, 384, 48, px_h, px_w)
        sword = GameObject(self.sword_image, 384, 48, px_h, px_w)

        # signage = GameObject(self.sign, 336, 672, px_h, px_w)

        heart1_x = self.width - (px_w*3)
        heart2_x = self.width - (px_w*2)
        heart3_x = self.width - px_w
        heart_y = 0

        heart1 = GameObject(self.heart, heart1_x, heart_y, px_h, px_w, sprite=True)
        heart2 = GameObject(self.heart, heart2_x, heart_y, px_h, px_w, sprite=True)
        heart3 = GameObject(self.heart, heart3_x, heart_y, px_h, px_w, sprite=True)

        # Main loop of game - runs until is_game_over == True
        while not is_game_over:

            # checks all events that occur
            for event in pygame.event.get():

                # quit event closes game
                if event.type == pygame.QUIT:
                    is_game_over = True

                # detect when key pressed
                elif event.type == pygame.KEYDOWN:

                    # move forward if key up pressed
                    if event.key ==pygame.K_UP:
                        direction_up_down = 1

                    # move back if key up pressed
                    elif event.key == pygame.K_DOWN:
                        direction_up_down = -1

                    elif event.key == pygame.K_LEFT:
                        direction_left_right = -1

                    elif event.key == pygame.K_RIGHT:
                        direction_left_right = 1

                # detect when key lifted
                elif event.type == pygame.KEYUP:

                    # stop moving when key lifted
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        direction_up_down = 0

                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        direction_left_right = 0

                # print(event)

            # Clear screen
            self.game_screen.fill(WHITE_COLOR)
            for layer in self.gameMap.visible_layers:
                for x, y, gid, in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if(tile != None):
                        self.game_screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

            if level_speed == 1:
                sword.draw(self.game_screen)
            else:
                treasure.draw(self.game_screen)

            # signage.draw(self.game_screen)

            heart1.draw(self.game_screen)
            heart2.draw(self.game_screen)
            heart3.draw(self.game_screen)

            # Update player position
            player_character.move(direction_up_down, direction_left_right, self.height, self.width)

            # Display player at new position
            player_character.draw(self.game_screen)

            enemy_0.move(self.width)
            enemy_0.draw(self.game_screen)

            collision = sum([player_character.detect_collision(enemy_0)])

            if collision > 0 and self.damage_taken == False:
                self.game_screen.fill((255,0,0))
                self.health -= 1

            if self.health == 5:
                self.damage_taken = True
                heart3 = GameObject(self.halflife, heart3_x, heart_y, px_h, px_w, sprite=True)

            if self.health == 4:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w, sprite=True)

            if self.health == 3:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w, sprite=True)
                heart2 = GameObject(self.halflife, heart2_x, heart_y, px_h, px_w, sprite=True)

            if self.health == 2:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w, sprite=True)
                heart2 = GameObject(self.heartless, heart2_x, heart_y, px_h, px_w, sprite=True)

            if self.health == 1:
                self.damage_taken = True
                heart3 = GameObject(self.heartless, heart3_x, heart_y, px_h, px_w, sprite=True)
                heart2 = GameObject(self.heartless, heart2_x, heart_y, px_h, px_w, sprite=True)
                heart1 = GameObject(self.halflife, heart1_x, heart_y, px_h, px_w, sprite=True)

            if collision == 0:
                self.damage_taken = False

            if self.health == 0:
                self.damage_taken = True
                is_game_over = True
                did_win = False
                text = font.render('YOU LOSE!', True, BLACK_COLOR)
                self.game_screen.blit(text, (200, 350))
                pygame.display.update()
                clock.tick(1)
                break

            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render('YOU WIN!', True, BLACK_COLOR)
                self.game_screen.blit(text, (200, 350))
                pygame.display.update()
                clock.tick(1)
                break

            # updates all game graphics
            pygame.display.update()
            # tick the clock to update everything in the game
            clock.tick(self.TICK_RATE)

        if did_win:
            self.player_image = self.later_player
            self.run_game_loop(level_speed + 0.5)
        else:
            return
