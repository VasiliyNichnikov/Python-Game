import pygame
import os


class WorkWithImage:
    def Load_image(self, name, colorkey=None, way="../data"):
        fullname = os.path.join(way, name)  # ../data
        image = pygame.image.load(fullname).convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def AddSprite(self, group, nameFile, dimensions=(100, 100), colorkey=None, way="../data", position=(0, 0)):
        sprite = pygame.sprite.Sprite()
        sprite.image = self.Load_image(nameFile, colorkey, way)
        sprite.image = pygame.transform.scale(sprite.image, dimensions)
        sprite.rect = sprite.image.get_rect()
        group.add(sprite)
        sprite.rect.x, sprite.rect.y = position
