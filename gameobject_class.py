import pygame

class GameObject:
    def __init__(self, image_path, x, y, width, height, sprite=False):
        if sprite == False:
            object_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(object_image, (width, height))
        else:
            self.image = image_path
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))
