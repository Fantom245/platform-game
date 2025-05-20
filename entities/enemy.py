import pygame

class Enemy:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(
            pygame.image.load("assets/enemy/enemy_2.png").convert_alpha(), (60, 50)
        )
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 1  # Можно потом сделать больше
        self.alive = True

    def update(self):
        pass  # Пока враг стоит на месте. Можно добавить патрулирование позже.

    def draw(self, surface):
        if self.alive:
            surface.blit(self.image, self.rect)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
