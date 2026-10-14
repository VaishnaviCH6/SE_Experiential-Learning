"""
Fishing Game

Run with:  python main.py
Controls:  SPACE = cast the hook,  R = restart after the round ends
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Fishing")
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 48, bold=True)

    engine = GameEngine()
    clock = pygame.time.Clock()   # created after fonts load so the first dt isn't inflated
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    engine.handle_cast()
                elif event.key == pygame.K_r and engine.is_over():
                    engine.restart()

        engine.update(dt)
        engine.draw(screen, font, big_font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()