import pygame
import math

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/enemy/enemy_2.png").convert_alpha(), (60, 50)
        )
        self.base_y = y  # Базовая точка (для плавания)
        self.display_rect = self.image.get_rect(topleft=(x, y))  # для отображения

        self.rect = pygame.Rect(x + 5, y + 4, 50, 40)  # хитбокс для столкновений

        self.health = 1
        self.alive = True

        # параметры анимации "плавания"
        self.float_amplitude = 5
        self.float_speed = 2
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if not self.alive:
            return

        # Плавающее движение
        now = pygame.time.get_ticks()
        offset = math.sin((now - self.spawn_time) / 1000 * self.float_speed) * self.float_amplitude

        self.display_rect.y = self.base_y + offset
        self.rect.y = self.base_y + 4 + offset  # тоже двигаем хитбокс вместе

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.display_rect)
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)  # хитбокс

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
