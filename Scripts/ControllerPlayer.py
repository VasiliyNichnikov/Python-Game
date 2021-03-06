import os
import pygame


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
                        #  print("Right OK")
                        self.isMoveRight = True
                        self.isMoveLeft = False
                    else:
                        #  print("Left OK")
                        self.isMoveRight = False
                        self.isMoveLeft = True
        if not check:
            self.isMoveRight = True
            self.isMoveLeft = True
            #  print(self.rect.x, blockTwo.rect.x)
            #  print(str(self.rect.y) + " Player", str(blockTwo.rect.y) + " Block")
            #  return True  # , blockTwo.rect.y
        #  return False  # , 0

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
