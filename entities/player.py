import pygame

from settings import *
from entities.platforms import Platform


class Player:
    def __init__(self, x, y):
        self.images_idle = [
            pygame.transform.scale(
                pygame.image.load("assets/player.png").convert_alpha(), (60, 50)
            )
        ]
        self.images_attack = [
            pygame.transform.scale(
                pygame.image.load(f"assets/attack/player_attack_{i}.png").convert_alpha(), (60, 50)
            )
            for i in range(3)
        ]
        self.image = self.images_idle[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel_y = 0
        self.on_ground = False

        self.is_attacking = False
        self.attack_frame = 0
        self.attack_timer = 0

    def handle_attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_timer = pygame.time.get_ticks()

    def update(self, platforms):
        self.handle_attack()

        # Обработка атаки
        if self.is_attacking:
            now = pygame.time.get_ticks()
            if now - self.attack_timer > 70:
                self.attack_frame += 1
                self.attack_timer = now
                if self.attack_frame >= len(self.images_attack):
                    self.is_attacking = False
                    self.attack_frame = 0

        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            dx = PLAYER_SPEED

        if keys[pygame.K_w] and self.on_ground:
            self.vel_y = JUMP_FORCE
            self.on_ground = False

        # Применение гравитации всегда (но vel_y будет = 0 при приземлении)
        self.vel_y += GRAVITY
        dy = self.vel_y

        self.on_ground = False  # Сброс перед проверкой

        # Столкновение с платформами (в том числе пол и "земля")
        for platform in platforms:
            future_rect = self.rect.move(0, dy)
            if future_rect.colliderect(platform.rect):
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.vel_y = 0
                    self.on_ground = True

        # Столкновение с землёй
        if self.rect.bottom + dy >= HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            dy = 0
            self.vel_y = 0
            self.on_ground = True

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        if self.is_attacking:
            self.image = self.images_attack[self.attack_frame]
        else:
            self.image = self.images_idle[0]
        surface.blit(self.image, self.rect)
