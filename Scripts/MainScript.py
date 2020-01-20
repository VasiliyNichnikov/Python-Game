import pygame
from Scripts.Levels import Levels
from Scripts.ControllerText import WorkWithButtons
from Scripts.LoadImages import WorkWithImage
from Scripts.ControllerText import WorkWithText


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


if __name__ == "__main__":
    StartGame = MenuScene()