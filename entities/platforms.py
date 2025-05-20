import pygame

class Platform:
    def __init__(self, x, y):
        original_image = pygame.image.load("assets/platforma.com.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (150, 50))  # ширина 100, высота 20
        self.rect = self.image.get_rect(topleft=(x, y))


    def draw(self, surface):
        surface.blit(self.image, self.rect)
