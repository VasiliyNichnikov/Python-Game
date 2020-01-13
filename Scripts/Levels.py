import pygame
import os
from Scripts.ControllerPlayer import ControllerPlayer
from Scripts.LoadImages import WorkWithImage


class Levels:
    classLoadImage = WorkWithImage()  # Класс для работы с изображением
    sizeTitle = 85  # Размер блока
    spritesTitles = pygame.sprite.Group()
    # Шрифт
    # Цвета шрифта
    colorStandard = pygame.Color('#F04643')
    colorLevelDoor = pygame.Color('white')
    # Список с блоками по которым может ходить игрок
    listAllSpritesGrass = []
    # Хранит все текста и их имена
    dictAllTexts = {}
    # Информация об игроке
    dictInfoPlayer = {}
    # Информация о дверях
    dictInfoDoor = {}

    def __init__(self):
        self.fontLevels = pygame.font.Font("../Fonts/Font01.otf", 80)
        self.fontLevelsDoor = pygame.font.Font("../Fonts/Font01.otf", 15)

    def MainFunction(self):
        # Инициализируем и задаем размеры
        pygame.init()
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)
        # Загружаем спрайты для заднего фона меню
        spritesBackgroundMenuGroup = pygame.sprite.Group()
        # Спрайт заднего фона с размером 1280 на 720
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Sky.png", (width, height))
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Hills_2.png", (width, height), way="../data/Levels",
                                      colorkey=-1)
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Hills_1.png", (width, height), way="../data/Levels",
                                      colorkey=-1)
        # Загрузка сцены
        self.LoadScene()
        # Группа спрайтов с персонажем и создание персонажа
        playerGroup = pygame.sprite.Group()
        player = ControllerPlayer(playerGroup, "../data/Person")
        # Работа с текстом
        # Все текста в выборе уровня
        textLevels = self.fontLevels.render("ВЫБОР УРОВНЯ", 1, self.colorStandard)

        FPS = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Работа с изображением (Начало)
            spritesBackgroundMenuGroup.draw(screen)
            self.spritesTitles.draw(screen)
            # Работа с изображением (Конец)

            # Работа с текстом (Начало)
            screen.blit(textLevels, (width // 2 - textLevels.get_width() // 2, height // 2 - 350))
            for text in self.dictAllTexts:
                self.dictAllTexts[text]["text"] = self.fontLevelsDoor.render(self.dictAllTexts[text]["name"], 1,
                                                                             self.colorLevelDoor)
                screen.blit(self.dictAllTexts[text]["text"], self.dictAllTexts[text]["position"])
            # Работа с текстом (Конец)

            # Рисование (Для теста)
            #  for i in self.listAllSpritesGrass:
            #    pygame.draw.line(screen, pygame.Color("black"), [i.rect.x, i.rect.y], [i.rect.x + 100, i.rect.y], 3)
            # Работа с персонажем (Начала)
            player.update(self.spritesTitles, self)
            playerGroup.draw(screen)
            # Работа с персонажем (Конец)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()

    # Загрузка уровня с помощью текстового документа
    def LoadScene(self):
        numX, numY = 0, 0
        numberDoorLevel = 1  # Уровень двери
        with open("../Scene_plans/PlanSceneLevel.txt") as file:
            fileRead = file.readlines()
            for line in fileRead:
                for block in range(len(line)):
                    if line[block] == '-':  # Трава со всех сторон
                        self.classLoadImage.AddSprite(self.spritesTitles, "GrassMid.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.AddSpriteInDictionary(self.spritesTitles.sprites()[-1], '-')
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
                        self.CreateGrassInBlock()
                        self.AddSpriteInDictionary(self.spritesTitles.sprites()[-1], '&')
                    elif line[block] == '.':  # Земля с права
                        self.classLoadImage.AddSprite(self.spritesTitles, "DirtRight.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                    elif line[block] == ',':  # Земля с лева
                        self.classLoadImage.AddSprite(self.spritesTitles, "DirtLeft.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                    elif line[block] == '/':  # Трава с права
                        self.classLoadImage.AddSprite(self.spritesTitles, "GrassRight.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.AddSpriteInDictionary(self.spritesTitles.sprites()[-1], '/')
                    elif line[block] == '!':  # Трава с лева
                        self.classLoadImage.AddSprite(self.spritesTitles, "GrassLeft.png",
                                                      (self.sizeTitle, self.sizeTitle), way="../data/Levels",
                                                      position=(numX, numY))
                        self.AddSpriteInDictionary(self.spritesTitles.sprites()[-1], '!')
                    elif line[block] == '^':  # Дверь с уровнями (Доделать)
                        self.classLoadImage.AddSprite(self.spritesTitles, "Door.png", (self.sizeTitle, self.sizeTitle),
                                                      way="../data/Levels",
                                                      position=(numX, numY), colorkey=-1)
                        self.dictInfoDoor["Door" + str(numberDoorLevel)] = {"level": numberDoorLevel,
                                                                            "sprite": self.spritesTitles.sprites()[-1]}
                        with open("../Scene_plans/Player_Information.txt") as fileInformation:
                            fileInformationRead = fileInformation.readlines()
                            for info in fileInformationRead:
                                if info.split():
                                    self.dictInfoPlayer[info.split()[0]] = info.split()[-1]

                        if int(self.dictInfoPlayer['Level']) < numberDoorLevel:  # Уровень подходит
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

                        self.dictAllTexts["level" + str(numberDoorLevel)] = {"name": "Уровень " + str(numberDoorLevel),
                                                                             "position": (numX + 6, numY, 10, 10),
                                                                             "text": None}
                        numberDoorLevel += 1
                    elif line[block] == '|':  # Дерево
                        self.classLoadImage.AddSprite(self.spritesTitles, "Tree_01.png", (300, 300),
                                                      way="../data/Levels",
                                                      position=(numX - 150, numY - 213), colorkey=-1)
                    numX += self.sizeTitle
                    #print(line[block], end='')
                numY += self.sizeTitle
                numX = 0
                print()

    def AddSpriteInDictionary(self, sprite, sign):
        self.listAllSpritesGrass.append(sprite)

    # Случайно создает траву на блоке (Не на всех блоках)
    def CreateGrassInBlock(self, posX=0, posY=0):
        listAllGrass = []
        directory = "../data/Grass"
        files = os.listdir(directory)
        print(files)
