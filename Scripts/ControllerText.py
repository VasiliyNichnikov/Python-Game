import pygame


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
            self.sizeFont = 100
            self.condition = "selected"
        else:
            self.btnColor = self.colorStandard
            self.sizeFont = 80
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

