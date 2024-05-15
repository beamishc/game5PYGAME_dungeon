from classes.base_classes.gameobject_class import GameObject

class NPC(GameObject):

    SPEED = 1

    def __init__(self, asset_name, image_path, x, y, width, height):
        super().__init__(asset_name, image_path, x, y, width, height)
        self.y_walk = 0
        self.y_up = True

    def move(self, max_width):
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED)
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

        if self.y_walk >= 1:
            self.y_up = False

        if self.y_walk <= 0:
            self.y_up = True

        if self.y_up == True:
            self.y_walk += 0.1
            self.y_pos += 0.1

        if self.y_up == False:
            self.y_walk -= 0.1
            self.y_pos -= 0.1
