class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self, width, height):
        self.dx = 0
        self.dy = 0
        self.width = width
        self.height = height

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        #obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        print(target.rect.w, " player")
        # (20 + 25 - 640)  (1280 + 25 - 640) =
        # x + 25 - 640 = 0
        # x = 640 - 25
        # x = 615
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        #self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)
        print(self.dx, self.dy)