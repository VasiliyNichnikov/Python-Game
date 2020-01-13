import pygame
from Scripts.CreateScene import CreateScene
#from Scripts.ControllerPlayer import ControllerPlayer


class Level:
    playerGroup = pygame.sprite.Group()  # Группа с персонажем

    def __init__(self, player):
        self.player = player
        #self.player = ControllerPlayer(self.playerGroup, "../data/Person", self)
        self.classLoadScene = CreateScene(self, 85, self.player, "../Scene_plans/Levels/Level_1.txt")
        #self.player = player
        self.MainFunction()

    def MainFunction(self):
        # Инициализируем и задаем размеры
        pygame.init()
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)


        FPS = 60
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Рисование Titles
            self.classLoadScene.spritesTitles.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)
        pygame.quit()