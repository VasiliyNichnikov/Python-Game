import pygame
from Scripts.CreateScene import CreateScene
from Scripts.LoadImages import WorkWithImage
from Scripts.Camera import Camera
from Scripts.ControllerPlayer import ControllerPlayer


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
        #self.player = player
        self.sceneLevels = sceneLevels
        self.player = ControllerPlayer(self.playerGroup, "../data/Person", self, False, (1280 // 2, 265))
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/Levels/Level_1.txt")
        self.camera = Camera(self.player)
        # Работа с текстом
        self.fontMenu = pygame.font.Font("../Fonts/Font01.otf", 40)
        # Все текста в меню
        self.textMenu = self.fontMenu.render("ВЫБОР УРОВНЯ", 1, self.colorStandard)
        self.listButtonsMenu = {
            "btnMenu": {"name": "ВЫБОР УРОВНЯ", "num": 1, "btn": self.textMenu, "active": "select",
                        "position": (self.width // 2 - self.textMenu.get_width() // 2, self.height // 2 - 180)},
        }
        self.MainFunction()

    # Функция для запуска сцены с уровнями
    def ButtonLevel(self, nameButton):
        if nameButton == "ВЫБОР УРОВНЯ":
            self.sceneLevels.MainFunction()

    def DrawText(self, screen):
        # Отображение текста (Начало)
        for btn in self.listButtonsMenu:
            if self.listButtonsMenu[btn]["active"] == "select":
                self.listButtonsMenu[btn]["btn"] = self.fontMenu.render(self.listButtonsMenu[btn]["name"], 1, self.colorChoice)
            elif self.listButtonsMenu[btn]["active"] == "standard":
                self.listButtonsMenu[btn]["btn"] = self.fontMenu.render(self.listButtonsMenu[btn]["name"], 1, self.colorStandard)
            elif self.listButtonsMenu[btn]["active"] == "transition":
                self.listButtonsMenu[btn]["btn"] = self.fontMenu.render(self.listButtonsMenu[btn]["name"], 1, self.colorPress)
            screen.blit(self.listButtonsMenu[btn]["btn"], self.listButtonsMenu[btn]["position"])
        # Отображение текста (Конец)

    def MainFunction(self):
        # Инициализируем и задаем размеры
        pygame.init()
        size = self.width, self.height
        screen = pygame.display.set_mode(size)

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

        for sprite in self.classLoadScene.spritesTitles:
            self.camera.StartPos(sprite, self.player, 1000, self.width // 2)

        FPS = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # Проверка нажатий с клавиатуры
                if event.type == pygame.KEYDOWN:
                    # Проверка на нажатия стрелок и Enter
                    if event.key == pygame.K_RETURN:
                        print("ENTER")
                        for btn in self.listButtonsMenu:
                            if self.listButtonsMenu[btn]["active"] == "select":
                                self.listButtonsMenu[btn]["active"] = "transition"
                                print(self.listButtonsMenu[btn]["name"], "происходит действие")
                                self.ButtonLevel(self.listButtonsMenu[btn]["name"])
                    elif event.key == pygame.K_ESCAPE:
                        self.isPauseGame = not self.isPauseGame

            #self.camera.update(self.player)
            #if self.player.isMove:
            if not self.player.isDead:
                for sprite in self.classLoadScene.spritesTitles:
                    self.camera.apply(sprite)
            # Рисование Titles (Начало)
            spritesBackgroundMenuGroup.draw(screen)
            self.classLoadScene.spritesTitles.draw(screen)
            # Рисование Titles (Конец)

            # Рисование и движение игрока (Начало)
            self.player.update(self.classLoadScene.spritesTitles)
            self.playerGroup.draw(screen)
            # Рисование и движение игрока (Конец)
            if self.player.isDead or self.isPauseGame:
                self.DrawText(screen)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()