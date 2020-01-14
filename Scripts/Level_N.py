import pygame
from Scripts.CreateScene import CreateScene
from Scripts.LoadImages import WorkWithImage
from Scripts.Camera import Camera
from Scripts.ControllerPlayer import ControllerPlayer


class Level:
    classLoadImage = WorkWithImage()  # Класс для работы с изображением
    playerGroup = pygame.sprite.Group()  # Группа с персонажем

    def __init__(self):
        #self.player = player
        self.player = ControllerPlayer(self.playerGroup, "../data/Person", self, False)
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/Levels/Level_1.txt")
        self.camera = Camera(1280, 720)
        #self.player = player
        self.MainFunction()

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

        FPS = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # if self.player.rect.x > 615:
            #     self.camera.update(self.player)
            #     for sprite in self.classLoadScene.spritesTitles:
            #         self.camera.apply(sprite)
            # Рисование Titles (Начало)
            spritesBackgroundMenuGroup.draw(screen)
            self.classLoadScene.spritesTitles.draw(screen)
            # Рисование Titles (Конец)

            # Рисование и движение игрока (Начало)
            self.player.update(self.classLoadScene.spritesTitles)
            self.playerGroup.draw(screen)
            # Рисование и движение игрока (Конец)

            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()