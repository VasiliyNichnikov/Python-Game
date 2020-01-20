import pygame
import os


class MenuScene:
    def __init__(self):
        # Все цвета кнопок
        self.colorPress = pygame.Color("#FFB633")
        self.colorChoice = pygame.Color('#F04643')
        self.colorStandard = pygame.Color('#E8822E')

        # Инициализируем и задаем размеры
        pygame.init()

        # Загрузка музыки на задний план
        pygame.mixer.music.load('../BackgroundMusic/music.mp3')
        pygame.mixer.music.play(loops=-1)

        # Загрузка звуков
        self.soundButtonInput = pygame.mixer.Sound('../Sounds/inputButton.mp3')

        self.classLoadImage = WorkWithImage()  # Класс для работы с изображением
        size = width, height = 1280, 720
        self.screen = pygame.display.set_mode(size)

        # Программа запущенна
        self.running = True

        # Загрузка сцены с уровнями
        self.sceneLevels = Levels(self)

        # Загружаем спрайты для заднего фона меню
        self.spritesBackgroundMenuGroup = pygame.sprite.Group()
        # Спрайт заднего фона с размером 1280 на 720
        self.classLoadImage.AddSprite(self.spritesBackgroundMenuGroup, "Background.png", (width, height))

        # Текст с названием игры
        self.textNameGame = WorkWithText(self.screen, size, self.colorPress, "ПЛАТФОРМЕР", (0, 200), sizeFont=100)

        # Создание кнопок
        buttonPlay = WorkWithButtons(self.screen, size, self.colorStandard, "ИГРАТЬ", 0,
                                     colorChoice=self.colorChoice,
                                     colorPress=self.colorPress, posPlusMinusXY=(0, 0))
        buttonExit = WorkWithButtons(self.screen, size, self.colorStandard, "ВЫХОД", 1,
                                     colorChoice=self.colorChoice,
                                     colorPress=self.colorPress, posPlusMinusXY=(0, -100))
        self.listAllButtons = [buttonPlay, buttonExit]
        self.MainProgram()

    # Загрузка сцены с уровнями (Play)
    def LoadSceneLevels(self):
        self.sceneLevels.MainFunction()

    def QuitGame(self):
        self.running = False

    # Определяем наимольший, наименьший и id, который сейчас выбран у кнопки
    def ReturnIdButton(self):
        idMin = 0
        idMax = len(self.listAllButtons)
        idSelected = 0
        for btn in self.listAllButtons:
            if btn.condition == "selected":
                idSelected = btn.id
        return idMin, idMax, idSelected

    # Основная программа
    def MainProgram(self):
        FPS = 60
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Проверка нажатий с клавиатуры
            keys = pygame.key.get_pressed()
            idMin, idMax, idSelected = self.ReturnIdButton()
            if keys[pygame.K_UP]:
                if idSelected - 1 >= idMin:
                    self.listAllButtons[idSelected].SelectBtn()
                    self.listAllButtons[idSelected - 1].SelectBtn(True)
            elif keys[pygame.K_DOWN]:
                if idSelected + 1 < idMax:
                    self.listAllButtons[idSelected].SelectBtn()
                    self.listAllButtons[idSelected + 1].SelectBtn(True)
            elif keys[pygame.K_RETURN]:
                self.soundButtonInput.play()
                title = self.listAllButtons[idSelected].Input()
                if title == "ИГРАТЬ":
                    self.LoadSceneLevels()
                elif title == "ВЫХОД":
                    self.QuitGame()

            # Игровой цикл (Начало)
            self.spritesBackgroundMenuGroup.draw(self.screen)
            # Игровой цикл (Конец)

            # Рендер текста
            self.textNameGame.RenderText()

            # Рендер кнопок(Начало)
            for btn in self.listAllButtons:
                btn.RenderBtn()
            # Рендер кнопок(Конец)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()


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
        self.player.isLock = True
        # Передвижение камеры
        if keys[pygame.K_d] and self.player.isMoveRight:  # and self.pos >= -83600:
            self.stopCamera = False
            obj.rect.x -= 10
            self.pos -= 10
        elif keys[pygame.K_a] and self.player.isMoveLeft:  # and self.pos <= -2000:
            self.stopCamera = False
            self.pos += 10
            obj.rect.x += 10
        else:
            self.stopCamera = True


class ControllerPlayer(pygame.sprite.Sprite):
    def __init__(self, group, directory, parent, isSelectLevel, startPos):
        super().__init__(group)
        self.parent = parent
        # Переменные игрока
        self.posPlayerX = startPos[0]  # 20
        self.posPlayerY = startPos[1]  # 265
        self.speedPlayer = 5
        self.gravity = -12
        self.isJump = False  # Проверка, что игрок прыгает
        self.isGround = True  # Проверка, что игрок на земле
        self.isMove = False  # Проверка, что игрок двигается
        self.isDoor = False  # Проверка, что игрок около двери
        self.isLock = False  # Блокируем движение игрока
        self.isDead = False  # Проверка игрока на проигрыш
        self.isMoveRight = True  # Можно двигаться в право
        self.isMoveLeft = True  # Можно двигаться в лево
        self.moveRight = False  # Игрок двигается в право
        self.moveLeft = False  # Игрок двигается в лево
        self.isBlockGravity = True  # Блокировка гравитации
        self.numDoor = 0  # Дверь около которой стоит игрок
        self.jumpCount = 11
        self.dictInfoPlayer = {}
        # Переменные, которые используются только в сцене выбора уровня
        self.isSelectLevel = isSelectLevel

        # Переменные для анимации
        self.idlePlayer = self.load_images(directory, "Idle New")
        self.runPlayerRight = self.load_images(directory, "Run Right")
        self.runPlayerLeft = self.load_images(directory, "Run Left")
        self.cur_frame = 0
        self.image = self.idlePlayer[self.cur_frame]
        self.rect = self.rect.move(self.posPlayerX, self.posPlayerY)
        self.InformationPlayer()

    # Загрузка изображений
    def load_images(self, directory, nameFolder):
        files = os.listdir(directory + "/" + nameFolder)
        listRes = []
        for image in files:
            loadedImage = pygame.image.load(directory + "/" + nameFolder + "/" + image)
            loadedImage = pygame.transform.scale(loadedImage, (60, 60))
            self.rect = loadedImage.get_rect()
            listRes.append(loadedImage)
            #  self.frames.append(loadedImage)
        return listRes

    # обноление кадров
    def update(self, group):
        if self.cur_frame + 1 >= 60:
            self.cur_frame = 0
        if self.isMove:
            if self.moveRight:
                self.image = self.runPlayerRight[self.cur_frame // 10]
            elif self.moveLeft:
                self.image = self.runPlayerLeft[self.cur_frame // 10]
        else:
            self.image = self.idlePlayer[0]
        self.cur_frame += 1
        self.MovePlayer()

    # Движение игрока
    def MovePlayer(self):
        # Проверка нажатий на кнопки
        keys = pygame.key.get_pressed()
        self.CheckPosX(self.parent.classLoadScene.listAllSpritesGrassX)
        #  print(self.isMoveRight, self.isMoveLeft, self.isMove)
        if keys[pygame.K_d] and self.posPlayerX <= 1210 and self.isMoveRight:
            if not self.isLock:
                self.posPlayerX += self.speedPlayer
            self.moveRight = True
            self.moveLeft = False
            self.isMove = True
        elif keys[pygame.K_a] and self.posPlayerX >= 10 and self.isMoveLeft:
            if not self.isLock:
                self.posPlayerX -= self.speedPlayer
            self.moveRight = False
            self.moveLeft = True
            self.isMove = True
        else:
            self.isMove = False
        self.rect.x = self.posPlayerX

        if self.rect.y >= 800 and self.isSelectLevel:
            self.MoveToStart([20, 265])
        elif self.rect.y >= 800 and not self.isSelectLevel:
            self.isDead = True
        if not self.isJump:
            if self.CheckGravity(self.parent.classLoadScene.listAllSpritesGrassY)[0] is False or not self.isBlockGravity:
                self.rect.y -= self.gravity
            else:
                self.isGround = True
            if keys[pygame.K_SPACE] and self.isGround:
                self.isJump = True
        else:
            # Прыжок
            if self.jumpCount >= 0:
                self.rect.y -= (self.jumpCount ** 2) / 2
                self.isGround = False
            else:
                self.isJump = False
                self.jumpCount = 11
            self.jumpCount -= 1

        if self.isSelectLevel:
            self.isDoor, self.numDoor = self.Doors(self.parent.dictInfoDoor)

    # Перемещение на старт
    def MoveToStart(self, start):
        self.rect.x = start[0]
        self.rect.y = start[1]
        self.posPlayerX = start[0]
        self.posPlayerY = start[1]

    def CheckPosX(self, allBlocks):
        check = False
        blocksZone = pygame.sprite.spritecollide(self, allBlocks, False)
        for blockOne in blocksZone:
            for blockTwo in allBlocks:
                if blockTwo == blockOne and self.rect.y >= blockTwo.rect.y:
                    check = True
                    if self.rect.x > blockTwo.rect.x:
                        self.isMoveRight = True
                        self.isMoveLeft = False
                    else:
                        self.isMoveRight = False
                        self.isMoveLeft = True
        if not check:
            self.isMoveRight = True
            self.isMoveLeft = True

    # Проверяем, если под игроком блоки
    def CheckGravity(self, allBlocks):
        blocksZone = pygame.sprite.spritecollide(self, allBlocks, False)
        for blockOne in blocksZone:
            for blockTwo in allBlocks:
                if blockTwo == blockOne and self.rect.y <= blockTwo.rect.y - 30:
                    #  print(str(self.rect.y) + " Player", str(blockTwo.rect.y) + " Block")
                    return True, blockTwo.rect.y
        return False, 0

    # Проверка на то, что игрок около двери
    def Doors(self, allBlocksDoors):
        listBlocks = []
        for i in allBlocksDoors:
            listBlocks.append(allBlocksDoors[i]['sprite'])
        blocksZone = pygame.sprite.spritecollide(self, listBlocks, False)

        for blockOne in blocksZone:
            for blockTwo in listBlocks:
                if blockTwo == blockOne and int(self.CheckLevel(blockTwo, allBlocksDoors)) <= \
                        int(self.dictInfoPlayer["Level"]):
                    return True, int(self.CheckLevel(blockTwo, allBlocksDoors))
        return False, 0

    # Метод для выхода с уровня
    def EndLevel(self, doorEndGame):
        listDoors = [doorEndGame]
        blocksZone = pygame.sprite.spritecollide(self, listDoors, False)
        for blockOne in blocksZone:
            for blockTwo in listDoors:
                if blockOne == blockTwo:
                    return True
        return False

    # Вывод уровня двери
    def CheckLevel(self, sprite, allBlocksDoors):
        for i in allBlocksDoors:
            if allBlocksDoors[i]['sprite'] == sprite:
                self.parent.infoDoorToPlayer = allBlocksDoors[i]
                return allBlocksDoors[i]['level']
        return "error"

    # Загружаем информацию об игроке
    def InformationPlayer(self):
        with open("../Scene_plans/Player_Information.txt") as fileInformation:
            fileInformationRead = fileInformation.readlines()
            for info in fileInformationRead:
                if info.split():
                    self.dictInfoPlayer[info.split()[0]] = info.split()[-1]


class WorkWithButtons:
    def __init__(self, screen, size, colorStandard, title, id, posPlusMinusXY=(0, 0),
                 condition="standard", sizeFont=80, colorChoice=None, colorPress=None):
        # Цвет кнопки
        self.btnColor = colorStandard
        # Экран отображения
        self.screen = screen
        # Заполняем цвета
        self.colorStandard = colorStandard
        self.colorChoice = colorChoice
        self.colorPress = colorPress
        # Название кнопки
        self.title = title
        # Состояние кнопки
        self.condition = condition
        # Размер кнопки
        self.sizeFont = sizeFont
        # id, уникальный id кнопки
        self.id = id
        # Размер кеопки
        self.size = size
        # Позиция относительно центра кнопки
        self.posPlusMinusXY = posPlusMinusXY
        # Делаем первую кнопку больше всех
        if id == 0:
            self.SelectBtn(True)
        else:
            self.SelectBtn()

    def SelectBtn(self, active=False):
        if active:
            self.btnColor = self.colorChoice
            self.sizeFont += 10
            self.condition = "selected"
        else:
            self.btnColor = self.colorStandard
            self.sizeFont -= 10
            self.condition = "standard"

    def RenderBtn(self):
        fontGame = pygame.font.Font("../Fonts/Font01.otf", self.sizeFont)
        btn = fontGame.render(self.title, 1, self.btnColor)
        position = (self.size[0] // 2 - btn.get_width() // 2 - self.posPlusMinusXY[0],
                    self.size[1] // 2 - btn.get_height() - self.posPlusMinusXY[1])
        self.screen.blit(btn, position)

    def Input(self):
        return self.title


class WorkWithText:
    def __init__(self, screen, size, colorStandard, title, position=(0, 0), sizeFont=80):
        # Цвет кнопки
        self.textColor = colorStandard
        # Экран отображения
        self.screen = screen
        # Название текста
        self.title = title
        # Размер текста
        self.sizeFont = sizeFont
        # Размер текста
        self.size = size
        # Позиция кнопки
        self.position = position

    def RenderText(self):
        fontGame = pygame.font.Font("../Fonts/Font01.otf", self.sizeFont)
        btn = fontGame.render(self.title, 1, self.textColor)
        position = (self.size[0] // 2 - btn.get_width() // 2 - self.position[0],
                    self.size[1] // 2 - btn.get_height() - self.position[1])
        self.screen.blit(btn, position)


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
                        if int(self.player.dictInfoPlayer['Level']) < numberDoorLevel:  # Уровень не подходит
                            self.classLoadImage.AddSprite(self.spritesTitles, "Fence.png",
                                                          (300, 300),
                                                          way="../data/Levels",
                                                          position=(numX - 110, numY - 215), colorkey=-1)
                            self.classLoadImage.AddSprite(self.spritesTitles, "CloseLevel.png",
                                                          (self.sizeTitle, self.sizeTitle),
                                                          way="../data/Levels",
                                                          position=(numX, numY - 64), colorkey=-1)
                        elif int(self.player.dictInfoPlayer['Level']) == numberDoorLevel:
                            self.classLoadImage.AddSprite(self.spritesTitles, "OpenLevel.png",
                                                          (self.sizeTitle, self.sizeTitle),
                                                          way="../data/Levels",
                                                          position=(numX, numY - 64), colorkey=-1)

                        else:
                            self.classLoadImage.AddSprite(self.spritesTitles, "TraversedLevel.png",
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


class Level:
    classLoadImage = WorkWithImage()  # Класс для работы с изображением
    playerGroup = pygame.sprite.Group()  # Группа с персонажем
    width, height = 1280, 720
    # Все цвета кнопок
    colorPress = pygame.Color("#FFB633")
    colorChoice = pygame.Color('#F04643')
    colorStandard = pygame.Color('#E8822E')
    isPauseGame = False  # Пауза в игре

    def __init__(self, sceneLevels, directory):
        # Инициализируем и задаем размеры
        pygame.init()

        # Загрузки звуков
        self.soundButtonInput = pygame.mixer.Sound('../Sounds/inputButton.mp3')

        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        self.sceneLevels = sceneLevels
        self.player = ControllerPlayer(self.playerGroup, "../data/Person", self, False, (1280 // 2, 265))
        self.classLoadScene = CreateScene(self, 85, self.player, directory)
        self.camera = Camera(self.player)
        buttonReturnLevels = WorkWithButtons(self.screen, size, self.colorStandard, "ВЫХОД В ВЫБОР УРОВНЯ", 0,
                                             sizeFont=40,
                                             colorChoice=self.colorChoice,
                                             colorPress=self.colorPress, posPlusMinusXY=(0, 100))
        self.listAllButtons = [buttonReturnLevels]
        self.textPauseMenu = WorkWithText(self.screen, size, self.colorPress, "ПАУЗА", (0, 200))
        self.textGameOverMenu = WorkWithText(self.screen, size, self.colorStandard, "ПОРАЖЕНИЕ", (0, 200))
        for sprite in self.classLoadScene.spritesTitles:
            self.camera.StartPos(sprite, self.player, 600, self.width // 2)
        for sprite in self.classLoadScene.spritesBots:
            self.camera.StartPos(sprite, self.player, 600, self.width // 2)
        for sprite in self.classLoadScene.spritesThings:
            self.camera.StartPos(sprite, self.player, 600, self.width // 2)

    def Reload(self):
        for i in self.classLoadScene.spritesTitles:
            self.classLoadScene.spritesTitles.remove(i)
        for i in self.playerGroup:
            self.playerGroup.remove(i)

    # Загрузка сцены с уровнями (Play)
    def LoadSceneLevels(self, levelEnd=False):
        if levelEnd:
            with open("../Scene_plans/Player_Information.txt") as file:
                fileRead = file.readlines()
            with open("../Scene_plans/Player_Information.txt", 'w') as file:
                for info in fileRead:
                    if info.split() and info.split()[0] == 'Level':
                        file.write(info.split()[0] + " " + str(int(self.player.dictInfoPlayer['Level']) + 1))
                        file.write('\n')
                    elif info.split() and info.split()[0] == 'Money':
                        file.write(info.split()[0] + " 0")
            self.sceneLevels.ReloadMap()
        self.sceneLevels.MainFunction()

    # Определяем наимольший, наименьший и id, который сейчас выбран у кнопки
    def ReturnIdButton(self):
        idMin = 0
        idMax = len(self.listAllButtons)
        idSelected = 0
        for btn in self.listAllButtons:
            if btn.condition == "selected":
                idSelected = btn.id
        return idMin, idMax, idSelected

    def MainFunction(self):
        # Выключаем паузу, смерть игрока и перемещаем игрока на старт
        self.player.MoveToStart((1280 // 2, 265))
        self.isPauseGame = False
        self.player.isDead = False
        self.player.isBlockGravity = True
        # Загружаем спрайты для заднего фона меню
        spritesBackgroundMenuGroup = pygame.sprite.Group()

        # Спрайт заднего фона с размером 1280 на 720
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Sky.png", (self.width, self.height))
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Hills_2.png", (self.width, self.height),
                                      way="../data/Levels",
                                      colorkey=-1)
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Hills_1.png", (self.width, self.height),
                                      way="../data/Levels",
                                      colorkey=-1)
        FPS = 60
        clock = pygame.time.Clock()
        running = True
        levelEnd = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    idMin, idMax, idSelected = self.ReturnIdButton()
                    if event.key == pygame.K_ESCAPE:
                        self.isPauseGame = not self.isPauseGame
                    if event.key == pygame.K_RETURN and (self.isPauseGame or self.player.isDead or levelEnd):
                        self.soundButtonInput.play()
                        title = self.listAllButtons[idSelected].Input()
                        if title == "ВЫХОД В ВЫБОР УРОВНЯ" or levelEnd:
                            self.LoadSceneLevels(levelEnd)
            keys = pygame.key.get_pressed()
            idMin, idMax, idSelected = self.ReturnIdButton()
            if keys[pygame.K_UP]:
                if idSelected - 1 >= idMin:
                    self.listAllButtons[idSelected].SelectBtn()
                    self.listAllButtons[idSelected - 1].SelectBtn(True)
            elif keys[pygame.K_DOWN]:
                if idSelected + 1 < idMax:
                    self.listAllButtons[idSelected].SelectBtn()
                    self.listAllButtons[idSelected + 1].SelectBtn(True)
            levelEnd = self.player.EndLevel(self.classLoadScene.doorEndLevel)

            if not self.player.isDead and not self.isPauseGame:
                for sprite in self.classLoadScene.spritesTitles:
                    self.camera.apply(sprite)
                for sprite in self.classLoadScene.spritesBots:
                    self.camera.apply(sprite)
                for sprite in self.classLoadScene.spritesThings:
                    self.camera.apply(sprite)
            # Рисование Titles (Начало)
            spritesBackgroundMenuGroup.draw(self.screen)
            for thing in self.classLoadScene.listAllThings:
                thing.Update(self.screen)
                thing.CheckPlayer(self.playerGroup, self.player)
            self.classLoadScene.spritesTitles.draw(self.screen)
            self.classLoadScene.spritesBots.draw(self.screen)
            # Рисование Titles (Конец)

            # Работа ботов (Начало)
            #  print(self.classLoadScene.spritesBots)
            for bot in self.classLoadScene.listAllBots:
                bot.update(self.classLoadScene.spritesBots)
                bot.CheckPlayer(self.playerGroup, self.player)
            # Работа ботов (Конец)

            # Рисование и движение игрока (Начало)
            self.player.update(self.classLoadScene.spritesTitles)
            self.playerGroup.draw(self.screen)
            # Рисование и движение игрока (Конец)
            if self.player.isDead or self.isPauseGame:
                for btn in self.listAllButtons:
                    btn.RenderBtn()
                if not self.player.isDead:
                    self.textPauseMenu.RenderText()
                else:
                    self.textGameOverMenu.RenderText()
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()


class Levels:
    classLoadImage = WorkWithImage()  # Класс для работы с изображением
    # Информация о двери около которой находится игрок
    infoDoorToPlayer = {}
    # spritesTitles = pygame.sprite.Group()
    playerGroup = pygame.sprite.Group()  # Группа с персонажем
    # Шрифт
    # Цвета шрифта
    colorStandard = pygame.Color('#F04643')
    colorLevelDoor = pygame.Color('white')
    # Хранит все текста и их имена
    dictAllTexts = {}
    # Информация об игроке
    dictInfoPlayer = {}
    # Информация о дверях
    dictInfoDoor = {}

    def __init__(self, menuGame):
        self.fontLevels = pygame.font.Font("../Fonts/Font01.otf", 80)
        self.fontLevelsDoor = pygame.font.Font("../Fonts/Font01.otf", 15)
        # Группа спрайтов с персонажем и создание персонажа
        self.player = ControllerPlayer(self.playerGroup, "../data/Person", self, True, (20, 265))
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/PlanSceneLevel.txt")
        self.level_N = None
        self.menuGame = menuGame

    def ReloadMap(self):
        for i in self.classLoadScene.spritesTitles:
            self.classLoadScene.spritesTitles.remove(i)
        self.player.InformationPlayer()
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/PlanSceneLevel.txt")

    def MainFunction(self):
        # Инициализируем и задаем размеры
        pygame.init()
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)
        # Загружаем спрайты для заднего фона меню
        spritesBackgroundMenuGroup = pygame.sprite.Group()
        # Создание текста
        textSelectLevel = WorkWithText(screen, size, self.colorStandard, "ВЫБОР УРОВНЯ", (0, 250))

        # Спрайт заднего фона с размером 1280 на 720
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Sky.png", (width, height))
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Hills_2.png", (width, height), way="../data/Levels",
                                      colorkey=-1)
        self.classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Hills_1.png", (width, height), way="../data/Levels",
                                      colorkey=-1)

        FPS = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.menuGame.MainProgram()
                    if event.key == pygame.K_RETURN and self.player.isDoor:
                        self.LoadLevel(self.player.numDoor)
            # Работа с изображением (Начало)
            spritesBackgroundMenuGroup.draw(screen)

            self.classLoadScene.spritesTitles.draw(screen)
            # Работа с изображением (Конец)

            textSelectLevel.RenderText()

            # Работа с текстом (Начало)
            for text in self.dictAllTexts:
                self.dictAllTexts[text]["text"] = self.fontLevelsDoor.render(self.dictAllTexts[text]["name"], 1,
                                                                             self.colorLevelDoor)
                screen.blit(self.dictAllTexts[text]["text"], self.dictAllTexts[text]["position"])
            # Работа с текстом (Конец)
            # Рисование и движение игрока (Начало)
            self.player.update(self.classLoadScene.spritesTitles)
            self.playerGroup.draw(screen)
            # Рисование и движение игрока (Конец)
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()

    # Загрузка уровня
    def LoadLevel(self, numberDoor):
        print(numberDoor)
        dictionary = f'../Scene_plans/Levels/Level_{numberDoor}.txt'
        if self.level_N is not None:
            self.level_N.Reload()
        self.level_N = Level(self, dictionary)
        self.level_N.MainFunction()


if __name__ == "__main__":
    StartGame = MenuScene()