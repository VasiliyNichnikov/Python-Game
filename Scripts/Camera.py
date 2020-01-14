import pygame


class Camera:
    def __init__(self, player):
        self.player = player
        self.stopCamera = False
        self.pos = 0

    def StartPos(self, obj, player, posX, posPlayerX):
        obj.rect.x -= posX
        player.rect.x = posPlayerX

    def apply(self, obj):
        # Блокировка движения игрока
        keys = pygame.key.get_pressed()
        #if self.player.rect.x == 1280 // 2 - self.player.rect.w and not self.stopCamera:
        self.player.isLock = True
        #else:
            #self.player.isLock = False
        # Передвижение камеры
        if keys[pygame.K_d]:  # and self.pos >= -83600:
            self.stopCamera = False
            obj.rect.x -= 10
            self.pos -= 10
        elif keys[pygame.K_a]:  # and self.pos <= -2000:
            self.stopCamera = False
            self.pos += 10
            obj.rect.x += 10
        else:
            self.stopCamera = True
