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

        self.is_dashing = False
        self.dash_time = 0
        self.dash_duration = 200  # мс
        self.dash_speed = 20
        self.dash_cooldown = 1000  # мс
        self.last_dash = -self.dash_cooldown

    def handle_attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            self.attack_timer = pygame.time.get_ticks()

    def handle_dash(self):
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if keys[pygame.K_LSHIFT] and not self.is_dashing and (now - self.last_dash) >= self.dash_cooldown:
            self.is_dashing = True
            self.dash_time = now
            self.last_dash = now

    def update(self, platforms):
        self.handle_attack()
        self.handle_dash()

        now = pygame.time.get_ticks()

        # Обработка атаки
        if self.is_attacking:
            if now - self.attack_timer > 70:
                self.attack_frame += 1
                self.attack_timer = now
                if self.attack_frame >= len(self.images_attack):
                    self.is_attacking = False
                    self.attack_frame = 0

        keys = pygame.key.get_pressed()
        dx = 0

        # Обработка Dash
        if self.is_dashing:
            if now - self.dash_time < self.dash_duration:
                if keys[pygame.K_a]:
                    dx = -self.dash_speed
                elif keys[pygame.K_d]:
                    dx = self.dash_speed
            else:
                self.is_dashing = False
        else:
            # Обычное движение
            if keys[pygame.K_a]:
                dx = -PLAYER_SPEED
            elif keys[pygame.K_d]:
                dx = PLAYER_SPEED

            # Прыжок
            if keys[pygame.K_w] and self.on_ground:
                self.vel_y = JUMP_FORCE
                self.on_ground = False

        # Применение гравитации
        self.vel_y += GRAVITY
        dy = self.vel_y

        self.on_ground = False  # Сброс перед проверкой

        # Столкновение с платформами
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

        # Применение перемещения
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):
        if self.is_attacking:
            self.image = self.images_attack[self.attack_frame]
        else:
            self.image = self.images_idle[0]
        surface.blit(self.image, self.rect)
