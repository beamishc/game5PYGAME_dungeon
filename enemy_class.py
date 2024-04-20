from gameobject_class import GameObject
from icecream import ic

ic.disable()

class Enemy(GameObject):

    SPEED = 5

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)
        self.y_float = 0
        self.y_up = True

    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

        ic("-----START-----")
        ic(self.y_float)

        if self.y_float >= 5:
            self.y_up = False

        if self.y_float <= 0:
            self.y_up = True

        ic(self.y_up)

        if self.y_up == True:
            self.y_float += 0.1
            self.y_pos += 0.1

        if self.y_up == False:
            self.y_float -= 0.1
            self.y_pos -= 0.1

        ic(self.y_float)

        ic(self.y_pos)
        ic("------END------")
