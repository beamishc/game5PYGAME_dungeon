from classes.base_classes.gameobject_class import GameObject
from icecream import ic

class PC(GameObject):

    SPEED = 10

    def __init__(self, asset_name, image_path, x, y, width, height):
        super().__init__(asset_name, image_path, x, y, width, height)

    def move(self, direction_up_down, direction_left_right, max_height, max_width, walls, doors):
        if direction_up_down > 0:  # We're moving downwards
            self.y_pos -= self.SPEED
        elif direction_up_down < 0:  # We're moving upwards
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - 16:
            self.y_pos = max_height - 16
        elif self.y_pos <= 0:
            self.y_pos = 0

        if direction_left_right > 0:  # We're moving to the right.
            self.x_pos += self.SPEED
        elif direction_left_right < 0:   # We're moving to the left.
            self.x_pos -= self.SPEED

        if self.x_pos >= max_width - 16:
            self.x_pos = max_width - 16
        elif self.x_pos <= 0:
            self.x_pos = 0

        for wall in walls:
            if self.collidewall(wall):
                # deal with left and right
                if direction_left_right > 0:  # We're moving to the right.
                    self.x_pos = wall[0] - 16
                elif direction_left_right < 0:  # We're moving to the left.
                    self.x_pos = wall[0] + wall[2]
                # deal with up and down
                if direction_up_down < 0:  # We're moving upwards
                    self.y_pos = wall[1] - 16
                elif direction_up_down > 0:  # We're moving downwards
                    self.y_pos = wall[1] + wall[3]

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height or self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width or self.x_pos + self.width < other_body.x_pos:
            return False
        return True

    # TODO: FIX weird collision issue
    def collidewall(self, wall):
        if self.y_pos > wall[1] + wall[3] or self.y_pos + self.height < wall[1]:
            return False
        if self.x_pos > wall[0] + wall[2] or self.x_pos + self.width < wall[0]:
            return False
        return True


    def calculate_health(self, current_health):
        pass
