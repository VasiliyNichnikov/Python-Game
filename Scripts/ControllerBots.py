import pygame
import os


class BotMoveHorizon(pygame.sprite.Sprite):
    def __init__(self, posX, posY, directory, group, parent):
        super().__init__(group)
        self.posX = posX
        self.posY = posY
        self.speed = 1

        self.bodyBot = pygame.image.load(directory)
        self.bodyBot = pygame.transform.scale(self.bodyBot, (80, 80))
        self.rect = self.bodyBot.get_rect()
        self.rect = self.rect.move(self.posX, self.posY)
        self.image = self.bodyBot
        self.parent = parent

    # Загрузка изображений
    def load_images(self, directory, nameFolder):
        files = os.listdir(directory + "/" + nameFolder)
        listRes = []
        for image in files:
            loadedImage = pygame.image.load(directory + "/" + nameFolder + "/" + image)
            loadedImage = pygame.transform.scale(loadedImage, (60, 60))
            self.rect = loadedImage.get_rect()
            listRes.append(loadedImage)
            return listRes

    def update(self, group):
        self.image = self.bodyBot
        self.Move()

    def Move(self):
        allBlocks = self.parent.spritesTitles
        blocksZone = pygame.sprite.spritecollide(self, allBlocks, False)
        for blockOne in blocksZone:
            for blockTwo in allBlocks:
                if blockTwo == blockOne and self.rect.y >= blockTwo.rect.y:
                    self.speed = -self.speed
        self.rect.x += self.speed

    def CheckPlayer(self, blockPlayer, player):
        blocksZone = pygame.sprite.spritecollide(self, blockPlayer, False)
        for blockOne in blocksZone:
            for blockTwo in blockPlayer:
                if blockTwo == blockOne:
                    player.isDead = True
                    player.isBlockGravity = False


class Sow(pygame.sprite.Sprite):
    def __init__(self, posX, posY, directory, group, parent):
        super().__init__(group)
        self.posX = posX
        self.posY = posY
        self.speed = 1
        self.angle = 0
        self.bodySow = pygame.image.load(directory)
        self.bodySow = pygame.transform.scale(self.bodySow, (200, 200))
        self.rect = self.bodySow.get_rect()
        self.rect = self.rect.move(self.posX, self.posY)
        self.image = self.bodySow
        self.parent = parent

    def Update(self, screen, move=True):
        surf, r = self.RotationCenter(self.image, self.rect, self.angle)
        self.angle += 1
        if self.angle >= 360:
            self.angle = 0
        screen.blit(surf, r)
        if move:
            self.Move()

    def RotationCenter(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

    def Move(self):
        if self.rect.y > 400 or self.rect.y < 255:
            self.speed = -self.speed
        self.rect.y += self.speed

    def CheckPlayer(self, blockPlayer, player):
        blocksZone = pygame.sprite.spritecollide(self, blockPlayer, False)
        for blockOne in blocksZone:
            for blockTwo in blockPlayer:
                if blockTwo == blockOne:
                    player.isDead = True
                    player.isBlockGravity = False

