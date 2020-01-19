from Scripts.LoadImages import WorkWithImage
from Scripts.ControllerBots import BotMoveHorizon
from Scripts.ControllerBots import Sow
import pygame


class CreateScene:
    def __init__(self, parent, sizeTitle, player, directory):
        self.classLoadImage = WorkWithImage()
        self.parent = parent
        self.spritesTitles = pygame.sprite.Group()
        self.spritesBots = pygame.sprite.Group()
        self.spritesThings = pygame.sprite.Group()
        self.sizeTitle = sizeTitle
        self.player = player
        self.directory = directory
        self.listAllSpritesGrassX = []
        self.listAllSpritesGrassY = []
        self.listAllBots = []
        self.listAllThings = []
        # Дверь для выхода из игры
        self.doorEndLevel = None
        self.LoadScene()

    # Загрузка уровня с помощью текстового документа
    def LoadScene(self):
        numX, numY = 0, 0
        numberDoorLevel = 1  # Уровень двери
        with open(self.directory) as file:
            fileRead = file.readlines()
            for line in fileRead:
                for block in range(len(line)):
                    if line[block] == '-':  # Трава со всех сторон
                        self.classLoadImage.AddSprite(self.spritesTitles, "GrassMid.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.listAllSpritesGrassY.append(self.spritesTitles.sprites()[-1])
                    elif line[block] == '#':  # Просто земля
                        self.classLoadImage.AddSprite(self.spritesTitles, "Dirt.png", (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels", position=(numX, numY))
                    elif line[block] == '@':  # Вода с землей
                        self.classLoadImage.AddSprite(self.spritesTitles, "Dirt.png", (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels", position=(numX, numY))
                        self.classLoadImage.AddSprite(self.spritesTitles, "Water_01.png",
                                                      (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels", position=(numX, numY), colorkey=-1)
                    elif line[block] == '?':  # Вода
                        self.classLoadImage.AddSprite(self.spritesTitles, "Water_01.png",
                                                      (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels", position=(numX, numY), colorkey=-1)
                    elif line[block] == '&':  # Просто трава
                        self.classLoadImage.AddSprite(self.spritesTitles, "Grass.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        #self.parent.CreateGrassInBlock()
                        self.listAllSpritesGrassY.append(self.spritesTitles.sprites()[-1])
                    elif line[block] == '.':  # Земля с права
                        self.classLoadImage.AddSprite(self.spritesTitles, "DirtRight.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.listAllSpritesGrassX.append(self.spritesTitles.sprites()[-1])
                    elif line[block] == ',':  # Земля с лева
                        self.classLoadImage.AddSprite(self.spritesTitles, "DirtLeft.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                    elif line[block] == '/':  # Трава с права
                        self.classLoadImage.AddSprite(self.spritesTitles, "GrassRight.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.listAllSpritesGrassX.append(self.spritesTitles.sprites()[-1])
                        self.listAllSpritesGrassY.append(self.spritesTitles.sprites()[-1])
                    elif line[block] == '!':  # Трава с лева
                        self.classLoadImage.AddSprite(self.spritesTitles, "GrassLeft.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.listAllSpritesGrassX.append(self.spritesTitles.sprites()[-1])
                        self.listAllSpritesGrassY.append(self.spritesTitles.sprites()[-1])
                    elif line[block] == '^':  # Дверь с уровнями (Доделать)
                        self.classLoadImage.AddSprite(self.spritesTitles, "Door.png", (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels",
                                                      position=(numX, numY), colorkey=-1)
                        self.parent.dictInfoDoor["Door" + str(numberDoorLevel)] = {"level": numberDoorLevel,
                                                                                   "sprite": self.spritesTitles.sprites()[-1]}
                        if int(self.player.dictInfoPlayer['Level']) < numberDoorLevel:  # Уровень подходит
                            self.classLoadImage.AddSprite(self.spritesTitles, "Fence.png",
                                                          (300, 300),
                                                          way="../data/Levels",
                                                          position=(numX - 110, numY - 215), colorkey=-1)
                            self.classLoadImage.AddSprite(self.spritesTitles, "CloseLevel.png",
                                                          (self.sizeTitle, self.sizeTitle),
                                                          way="../data/Levels",
                                                          position=(numX, numY - 64), colorkey=-1)
                        else:
                            self.classLoadImage.AddSprite(self.spritesTitles, "OpenLevel.png",
                                                          (self.sizeTitle, self.sizeTitle),
                                                          way="../data/Levels",
                                                          position=(numX, numY - 64), colorkey=-1)

                        self.parent.dictAllTexts["level" + str(numberDoorLevel)] = {"name": "Уровень " +
                                                                                            str(numberDoorLevel),
                                                                                    "position":
                                                                                        (numX + 6, numY, 10, 10),
                                                                                    "text": None
                                                                                    }
                        numberDoorLevel += 1
                    elif line[block] == '$':  # Создание бота, который двигается по горизонтале
                        botMoveHor = BotMoveHorizon(numX, numY, "../data/Levels/Mac 512.png", self.spritesBots, self)
                        self.listAllBots.append(botMoveHor)
                    elif line[block] == '*':
                        sow = Sow(numX, numY, "../data/Levels/Saw.png", self.spritesThings, self)
                        self.listAllThings.append(sow)
                    elif line[block] == '|':  # Дерево
                        self.classLoadImage.AddSprite(self.spritesTitles, "Tree_01.png", (300, 300),
                                                      way="../data/Levels",
                                                      position=(numX - 150, numY - 213), colorkey=-1)
                    elif line[block] == '>':  # Создание двери выхода
                        self.classLoadImage.AddSprite(self.spritesTitles, "Door.png", (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels",
                                                      position=(numX, numY), colorkey=-1)
                        self.doorEndLevel = self.spritesTitles.sprites()[-1]
                        self.classLoadImage.AddSprite(self.spritesTitles, "TraversedLevel.png",
                                                      (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels",
                                                      position=(numX, numY - 64), colorkey=-1)
                    numX += self.sizeTitle
                numY += self.sizeTitle
                numX = 0
