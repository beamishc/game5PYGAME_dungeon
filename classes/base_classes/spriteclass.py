import pygame

class SpriteSheet:

    def __init__(self, filename, horizontal, vertical, tile_h, tile_w, space):
        """Load the sheet"""
        self.horizontal = horizontal
        self.vertical = vertical
        self.tile_h = tile_h
        self.tile_w = tile_w
        self.space = space

        try:
            self.sheet = pygame.image.load(filename)
        except pygame.error as e:
            print(f"unable to locate spritesheet at given location: {filename}")
            raise SystemExit(e)

    def image_at(self, y_deep_tiles, x_deep_tiles, colorkey=None):
        """Load a specific image from a specific rectangle in a spritesheet"""
        x_deep_px = x_deep_tiles * self.tile_w
        y_deep_px = y_deep_tiles * self.tile_h
        rectangle = (x_deep_px, y_deep_px, x_deep_px + self.tile_w, self.tile_h)
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey=None):
        """Load a bunch of images and return them as a list"""
        return [self.image_at(rect,colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey=None):
        """Load a whole strip of images and return them as a list"""
        tups = [(rect[0] + rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        return self.images_at(tups,colorkey)
