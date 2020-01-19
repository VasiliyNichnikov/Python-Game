import pygame
from Scripts.ControllerPlayer import ControllerPlayer
from Scripts.LoadImages import WorkWithImage
from Scripts.CreateScene import CreateScene
from Scripts.Level_N import Level
from Scripts.ControllerText import WorkWithText


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
        self.level_N = Level(self)
        self.menuGame = menuGame

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
                        self.LoadLevel()
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

    # Загрзка уровня
    def LoadLevel(self):
        self.level_N.MainFunction()
