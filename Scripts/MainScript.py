import pygame
from Scripts.Levels import Levels
from Scripts.LoadImages import WorkWithImage


# Инициализируем и задаем размеры
pygame.init()
classLoadImage = WorkWithImage()  # Класс для работы с изображением
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

# Работа с текстом
fontMenu = pygame.font.Font("../Fonts/Font01.otf", 80)

# Все цвета кнопок
colorPress = pygame.Color("#FFB633")
colorChoice = pygame.Color('#F04643')
colorStandard = pygame.Color('#E8822E')

# Все текста в меню
textPlay = fontMenu.render("ИГРАТЬ", 1, colorStandard)
textShop = fontMenu.render("МАГАЗИН", 1, colorStandard)
textSettings = fontMenu.render("НАСТРОЙКИ", 1, colorStandard)
textExit = fontMenu.render("ВЫХОД", 1, colorStandard)


# Функция для запуска сцены с уровнями
def ButtonPlay(nameButton):
    if nameButton == "ИГРАТЬ":
        levels = Levels()
        levels.MainFunction()
    elif nameButton == "МАГАЗИН":
        print("Shop")
    elif nameButton == "НАСТРОЙКИ":
        print("Settings")
    elif nameButton == "ВЫХОД":
        print("EXIT")


listButtonsMenu = {
    "btnPlay": {"name": "ИГРАТЬ", "num": 1, "btn": textPlay, "active": "select", "position": (width // 2 - textPlay.get_width() // 2, height // 2 - 180)},
    "btnShop": {"name": "МАГАЗИН", "num": 2, "btn": textShop, "active": "standard", "position": (width // 2 - textShop.get_width() // 2, height // 2 - 100)},
    "btnSettings": {"name": "НАСТРОЙКИ", "num": 3, "btn": textSettings, "active": "standard", "position": (width // 2 - textSettings.get_width() // 2, height // 2 - 20)},
    "btnExit": {"name": "ВЫХОД", "num": 4, "btn": textExit, "active": "standard", "position": (width // 2 - textExit.get_width() // 2, height // 2 + 60)}
}

# Загружаем спрайты для заднего фона меню
spritesBackgroundMenuGroup = pygame.sprite.Group()
# Спрайт заднего фона с размером 1280 на 720
classLoadImage.AddSprite(spritesBackgroundMenuGroup, "Background.png", (width, height))


# Меняет цвет кнопки (direction(true) - вверх, direction(false) - вниз)
def ChangeButton(direction=False):
    btnNumSelected = None
    for btn in listButtonsMenu:
        if listButtonsMenu[btn]["active"] == "select":
            btnNumSelected = int(listButtonsMenu[btn]["num"])
    # Двигаем кнопку вверх
    if direction and btnNumSelected - 1 >= 1:
        for btn in listButtonsMenu:
            if listButtonsMenu[btn]["active"] == "select":
                listButtonsMenu[btn]["active"] = "standard"
            elif listButtonsMenu[btn]["num"] == btnNumSelected - 1:
                listButtonsMenu[btn]["active"] = "select"
    # Двигаем кнопку вниз
    elif not direction and btnNumSelected + 1 <= 4:
        for btn in listButtonsMenu:
            if listButtonsMenu[btn]["active"] == "select":
                listButtonsMenu[btn]["active"] = "standard"
            elif listButtonsMenu[btn]["num"] == btnNumSelected + 1:
                listButtonsMenu[btn]["active"] = "select"


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
            if event.key == pygame.K_UP:
                print("UP")
                ChangeButton(True)
            elif event.key == pygame.K_DOWN:
                print("DOWN")
                ChangeButton()
            elif event.key == pygame.K_RETURN:
                print("ENTER")
                for btn in listButtonsMenu:
                    if listButtonsMenu[btn]["active"] == "select":
                        listButtonsMenu[btn]["active"] = "transition"
                        print(listButtonsMenu[btn]["name"], "происходит действие")
                        ButtonPlay(listButtonsMenu[btn]["name"])
    # Игровой цикл (Начало)
    spritesBackgroundMenuGroup.draw(screen)
    # Игровой цикл (Конец)

    # Начало работы с текстом (Вывод текста)
    for btn in listButtonsMenu:
        if listButtonsMenu[btn]["active"] == "select":
            listButtonsMenu[btn]["btn"] = fontMenu.render(listButtonsMenu[btn]["name"], 1, colorChoice)
        elif listButtonsMenu[btn]["active"] == "standard":
            listButtonsMenu[btn]["btn"] = fontMenu.render(listButtonsMenu[btn]["name"], 1, colorStandard)
        elif listButtonsMenu[btn]["active"] == "transition":
            listButtonsMenu[btn]["btn"] = fontMenu.render(listButtonsMenu[btn]["name"], 1, colorPress)
        screen.blit(listButtonsMenu[btn]["btn"], listButtonsMenu[btn]["position"])
    # Конец работы с текстом
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()