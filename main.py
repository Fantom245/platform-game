"""
Создание объекта и запуск игры
"""

import pygame

from settings import *
from core.game import Game


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Платформер")
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.draw()

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()