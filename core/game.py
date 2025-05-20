from entities.player import Player
from entities.platforms import Platform
from entities.enemy import Enemy  # 💥 Новый импорт

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.platforms = [Platform(50, 400), Platform(200, 300)]
        self.enemies = [Enemy(300, 200), Enemy(500, 400)]  # 💥 Добавим врагов
        self.player = Player(100, 300)

    def update(self):
        self.player.update(self.platforms, self.enemies)  # 💥 Передаём врагов
        for enemy in self.enemies:
            enemy.update()

    def draw(self):
        self.screen.fill((135, 206, 235))
        for platform in self.platforms:
            platform.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)  # 💥 Отрисовка врагов
        self.player.draw(self.screen)
