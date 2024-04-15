from gameobject_class import GameObject

class PC(GameObject):

    SPEED = 10

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction_up_down, direction_left_right, max_height, max_width):
        if direction_up_down > 0:
            self.y_pos -= self.SPEED
        elif direction_up_down < 0:
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - 40:
            self.y_pos = max_height - 40
        elif self.y_pos <= 40:
            self.y_pos = 40

        if direction_left_right > 0:
            self.x_pos += self.SPEED
        elif direction_left_right < 0:
            self.x_pos -= self.SPEED

        if self.x_pos >= max_width - 40:
            self.x_pos = max_width - 40
        elif self.x_pos <= 40:
            self.x_pos = 40

    def detect_collision(self, other_body):
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False
        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.height < other_body.x_pos:
            return False
        return True
