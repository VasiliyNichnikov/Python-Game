import pygame
from Scripts.ControllerPlayer import ControllerPlayer
from Scripts.LoadImages import WorkWithImage
from Scripts.CreateScene import CreateScene


class Levels:
    classLoadImage = WorkWithImage()  # Класс для работы с изображением
    # Информация о двери около которой находится игрок
    infoDoorToPlayer = {}
    spritesTitles = pygame.sprite.Group()
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

    def __init__(self):
        self.fontLevels = pygame.font.Font("../Fonts/Font01.otf", 80)
        self.fontLevelsDoor = pygame.font.Font("../Fonts/Font01.otf", 15)
        # Группа спрайтов с персонажем и создание персонажа
        self.player = ControllerPlayer(self.playerGroup, "../data/Person", self)
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/PlanSceneLevel.txt")

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
            self.classLoadScene.spritesTitles.draw(screen)
            # Работа с изображением (Конец)

            # Работа с текстом (Начало)
            screen.blit(textLevels, (width // 2 - textLevels.get_width() // 2, height // 2 - 350))
            for text in self.dictAllTexts:
                self.dictAllTexts[text]["text"] = self.fontLevelsDoor.render(self.dictAllTexts[text]["name"], 1,
                                                                             self.colorLevelDoor)
                screen.blit(self.dictAllTexts[text]["text"], self.dictAllTexts[text]["position"])
            # Работа с текстом (Конец)
            self.player.update(self.spritesTitles)
            self.playerGroup.draw(screen)
            # Работа с персонажем (Конец)
            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()

    # Случайно создает траву на блоке (Не на всех блоках)
    def CreateGrassInBlock(self, posX=0, posY=0):
        pass
    #     listAllGrass = []
    #     directory = "../data/Grass"
    #     files = os.listdir(directory)
    #     print(files)
