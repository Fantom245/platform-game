from entities.player import Player
from entities.platforms import Platform

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.platforms = [Platform(50, 400), Platform(200, 300)]  # создаём платформы один раз
        self.player = Player(100, 300)

    def update(self):
        self.player.update(self.platforms)

    def draw(self):
        self.screen.fill((135, 206, 235))  # фон
        for platform in self.platforms:
            platform.draw(self.screen)
        self.player.draw(self.screen)
