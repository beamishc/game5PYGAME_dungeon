import pygame
import pytmx
# import pyscroll
from classes.base_classes.gameobject_class import GameObject
from classes.playercharacter_class import PC
from classes.nonplayercharacter_class import NPC
from classes.enemy_class import Enemy
from classes.base_classes.spriteclass import SpriteSheet
from icecream import ic

# print(pygame.font.get_fonts())

bit_asset_sheet_path = 'teeny_tiny_game/assets/kenney_1-bit-pack/Tilesheet/colored-transparent_packed.png'
bit_sprite = SpriteSheet(bit_asset_sheet_path, 49, 22, 16, 16, 1)
door_asset_sheet_path = 'teeny_tiny_game/assets/lvls/0.Prologue/Walls, Floor & Doors.png'
bit_sprite = SpriteSheet(bit_asset_sheet_path, 8, 5, 16, 16, 0)


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

    def __init__(self, current_lvl, lvl_dct, save_file):
        '''Initalises the level using the dict for that level and the player's save file'''
        # current level
        self.current_lvl = current_lvl

        # basic info
        self.lvl_dct = lvl_dct
        self.asset_path = lvl_dct["ASSET_PATH"]
        self.title = lvl_dct['SCREEN_TITLE']
        self.width = eval(lvl_dct['SCREEN_WIDTH'])
        self.height = eval(lvl_dct['SCREEN_HEIGHT'])

        # lvl specific content
        self.player = lvl_dct["PLAYER"]
        self.location = lvl_dct["MAIN_LOCATION"]
        self.enemies = lvl_dct['ENEMIES']
        self.goal = lvl_dct['GOAL']
        self.npcs = lvl_dct['NPCS']
        self.doors = lvl_dct['DOORS']
        self.rooms = lvl_dct['ROOMS']

        #save file content
        self.save_file = save_file
        self.health = save_file["CURRENT_HEALTH"]

        # settings
        self.damage_taken = False

        # create the game screen
        self.game_screen = pygame.display.set_mode((self.width, self.height))

        # create images that need to be converted onto blit
        self.heart = bit_sprite.image_at(10, 39)
        self.halflife = bit_sprite.image_at(10, 41)
        self.heartless = bit_sprite.image_at(10, 40)
        self.door_image = bit_sprite.image_at(3, 5)

        # set the game screen to white
        self.game_screen.fill(WHITE_COLOR)
        pygame.display.set_caption(self.title)

    def set_scene(self):
        '''Uses classes to create player_character, enemeies, goal, hearts, doors, and rooms'''

        px_h = 16
        px_w = 16

        player_character = PC(self.save_file["NAME"]
                            , self.asset_path + self.player["IMAGE"]
                            , self.player["x_pos"]
                            , self.player["y_pos"]
                            , px_h, px_w)

        enemies = []
        for enemy in self.enemies:
            enemies.append(Enemy(enemy
                            , self.asset_path + self.enemies[enemy]["IMAGE"]
                            , self.enemies[enemy]["x_pos"]
                            , self.enemies[enemy]["y_pos"]
                            , px_h, px_w))

        # define goal
        goal = GameObject(self.goal["NAME"]
                        , self.asset_path + self.goal["IMAGE"]
                        , self.goal["x_pos"]
                        , self.goal["y_pos"]
                        , px_h, px_w)

        # create hearts
        hearts = []
        for i in range(1, (self.save_file["MAX_HEALTH"]//2)+1):
            ic(i)
            hearts.append(GameObject("heart", self.heart, self.width - px_w*i, 0, px_h, px_w, sprite=True))
        ic(hearts)

        doors = []

        for door in self.doors:
            doors.append(GameObject(door
                        , self.door_image
                        , self.doors[door]["x_pos"]
                        , self.doors[door]["y_pos"]
                        , px_h, px_w, sprite=True))

        rooms = {}

        for room in self.rooms:
            rooms[self.rooms[room]["DOOR"]] = room

        return px_h, px_w, player_character, enemies, goal, hearts, doors, rooms

    def check_input(self, event, is_game_over, direction_up_down, direction_left_right):
        '''Checks the input from the keys and changes the direction or quits the game'''
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

        return is_game_over, direction_up_down, direction_left_right

    # TODO: FIX inexplicable heart problem
    def check_health(self, hearts, px_w, px_h):
        '''Checks the health of the player compared to their maxiumum possible health.
        Depending on the health the hearts in the hearts list should be adjusted to display as half full or empty.
        Currently hardcoded, badly needs to be improved'''

        if self.health != self.save_file["MAX_HEALTH"]:
            self.damage_taken = True
            diff = self.save_file["MAX_HEALTH"] - self.health
            if diff == 1:
                hearts[-1] = GameObject("heart", self.halflife, self.width - px_w, 0, px_h, px_w, sprite=True)
            if diff == 2:
                hearts[-1] = GameObject("heart", self.heartless, self.width - px_w, 0, px_h, px_w, sprite=True)
            if diff == 3:
                hearts[-1] = GameObject("heart", self.heartless, self.width - px_w, 0, px_h, px_w, sprite=True)
                hearts[-2] = GameObject("heart", self.halflife, self.width - px_w*2, 0, px_h, px_w, sprite=True)
            if diff == 4:
                hearts[-1] = GameObject("heart", self.heartless, self.width - px_w, 0, px_h, px_w, sprite=True)
                hearts[-2] = GameObject("heart", self.heartless, self.width - px_w*2, 0, px_h, px_w, sprite=True)
            if diff == 5:
                hearts[-1] = GameObject("heart", self.heartless, self.width - px_w, 0, px_h, px_w, sprite=True)
                hearts[-2] = GameObject("heart", self.heartless, self.width - px_w*2, 0, px_h, px_w, sprite=True)
                hearts[-3] = GameObject("heart", self.halflife, self.width - px_w*3, 0, px_h, px_w, sprite=True)
        return hearts

    def draw_map_and_basics(self, goal, hearts):
        '''Draws the map and the basic game objects on the screen'''
        for layer in self.gameMap.visible_layers:
                for x, y, gid, in layer:
                    tile = self.gameMap.get_tile_image_by_gid(gid)
                    if(tile != None):
                        self.game_screen.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

        # draw stuff
        goal.draw(self.game_screen)

        for heart in hearts:
            heart.draw(self.game_screen)

    def enemy_actions(self, enemy, player_character, px_w, px_h, hearts):
        '''Moves the enemy and checks for collisions with the player character. If a collision is detected the player loses health.'''
        enemy.move(self.width)
        enemy.draw(self.game_screen)
        collision = sum([player_character.detect_collision(enemy)])

        if collision > 0 and self.damage_taken == False:
            self.game_screen.fill((255,0,0))
            self.health -= 1

            hearts = self.check_health(hearts, px_w, px_h)

        if collision == 0:
            self.damage_taken = False

        return hearts

    def door_check(self, doors, rooms,  player_character):
        '''Checks if the player has collided with a door and changes the location to the room that the door leads to'''
        for door in doors:
            if player_character.detect_collision(door):
                self.location = rooms[door.asset_name]
                player_character.x_pos = self.rooms[self.location]["x_pos"]
                player_character.y_pos = self.rooms[self.location]["y_pos"]
        return player_character

    def finalize(self, did_win):
        '''Updates the save file with the current level, highest level, and health of the player.
        If the player has lost the game the health is reset to max health and the times died is increased by 1.'''
        # update current level and highest levels in save_file
        self.save_file["CURRENT_LEVEL"] = int(self.current_lvl)
        if self.save_file["HIGHEST_LEVEL"] < int(self.current_lvl):
            self.save_file["HIGHEST_LEVEL"] = int(self.current_lvl)

        if did_win:
            # update current health in save_file
            self.save_file["CURRENT_HEALTH"] = self.health
        else:
            # return current health in save file to max health
            self.save_file["CURRENT_HEALTH"] = self.save_file["MAX_HEALTH"]
            # add 1 to times died in save file
            self.save_file["TIMES_DIED"] += 1

    def run_game_loop(self):
        '''Runs the main game loop for each level'''
        is_game_over = False
        did_win = False
        direction_up_down = 0
        direction_left_right = 0

        px_h, px_w, player_character, enemies, goal, hearts, doors, rooms = self.set_scene()

        # Main loop of game - runs until is_game_over == True
        while not is_game_over:

            self.gameMap = pytmx.load_pygame(self.rooms[self.location]['BACKGROUND'])

            # define walls
            walls = [pygame.Rect(obj.x, obj.y, obj.width, obj.height) for obj in self.gameMap.objects if obj.type == "wall"]

            # checks all events that occur
            for event in pygame.event.get():
                is_game_over, direction_up_down, direction_left_right = self.check_input(event, is_game_over, direction_up_down, direction_left_right)

            # Clear screen
            self.game_screen.fill(WHITE_COLOR)

            # display map
            self.draw_map_and_basics(goal, hearts)

            ## PLAYER MOVEMENT
            # Update player position
            player_character.move(direction_up_down, direction_left_right, self.height, self.width, walls, doors)
            # Display player at new position
            player_character.draw(self.game_screen)

            ## ENEMY MOVEMENT
            for enemy in enemies:
                hearts = self.enemy_actions(enemy, player_character, px_w, px_h, hearts)

                if self.health == 0:
                    self.damage_taken = True
                    is_game_over = True
                    did_win = False
                    text = font.render('YOU LOSE!', True, BLACK_COLOR)
                    self.game_screen.blit(text, (200, 350))
                    pygame.display.update()
                    clock.tick(1)
                    break

            player_character = self.door_check(doors, rooms, player_character)

            if player_character.detect_collision(goal):
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

        ic(self.location)

        self.finalize(did_win)

        return did_win
