import pygame
from Scripts.CreateScene import CreateScene
from Scripts.LoadImages import WorkWithImage
from Scripts.Camera import Camera
from Scripts.ControllerPlayer import ControllerPlayer
from Scripts.ControllerText import WorkWithButtons
from Scripts.ControllerText import WorkWithText


class Level:
    classLoadImage = WorkWithImage()  # Класс для работы с изображением
    playerGroup = pygame.sprite.Group()  # Группа с персонажем
    width, height = 1280, 720
    # Все цвета кнопок
    colorPress = pygame.Color("#FFB633")
    colorChoice = pygame.Color('#F04643')
    colorStandard = pygame.Color('#E8822E')
    isPauseGame = False  # Пауза в игре

    def __init__(self, sceneLevels):
        # Инициализируем и задаем размеры
        pygame.init()
        size = self.width, self.height
        self.screen = pygame.display.set_mode(size)
        self.sceneLevels = sceneLevels
        self.player = ControllerPlayer(self.playerGroup, "../data/Person", self, False, (1280 // 2, 265))
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/Levels/Level_1.txt")
        self.camera = Camera(self.player)
        buttonReturnLevels = WorkWithButtons(self.screen, size, self.colorStandard, "ВЫХОД В ВЫБОР УРОВНЯ", 0,
                                             sizeFont=40,
                                             colorChoice=self.colorChoice,
                                             colorPress=self.colorPress, posPlusMinusXY=(0, 100))
        self.listAllButtons = [buttonReturnLevels]
        self.textNameMenu = WorkWithText(self.screen, size, self.colorPress, "ПАУЗА", (0, 200))
        for sprite in self.classLoadScene.spritesTitles:
            self.camera.StartPos(sprite, self.player, 1000, self.width // 2)

    # Загрузка сцены с уровнями (Play)
    def LoadSceneLevels(self):
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
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.isPauseGame = not self.isPauseGame
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
            elif keys[pygame.K_RETURN] and (self.isPauseGame or self.player.isDead):
                title = self.listAllButtons[idSelected].Input()
                if title == "ВЫХОД В ВЫБОР УРОВНЯ":
                    self.LoadSceneLevels()

            if not self.player.isDead and not self.isPauseGame:
                for sprite in self.classLoadScene.spritesTitles:
                    self.camera.apply(sprite)
            # Рисование Titles (Начало)
            spritesBackgroundMenuGroup.draw(self.screen)
            self.classLoadScene.spritesTitles.draw(self.screen)
            # Рисование Titles (Конец)

            # Рисование и движение игрока (Начало)
            self.player.update(self.classLoadScene.spritesTitles)
            self.playerGroup.draw(self.screen)
            # Рисование и движение игрока (Конец)
            if self.player.isDead or self.isPauseGame:
                for btn in self.listAllButtons:
                    btn.RenderBtn()
                self.textNameMenu.RenderText()
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()