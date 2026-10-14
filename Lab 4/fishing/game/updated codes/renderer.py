"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
SURFACE_Y = 80
MAX_DEPTH_Y = HEIGHT - 40

WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_SKY = (140, 200, 230)
COLOR_WATER = (30, 90, 150)
COLOR_BOAT = (120, 80, 50)
COLOR_LINE = (240, 240, 240)
COLOR_HOOK = (220, 220, 220)
COLOR_TEXT = (255, 255, 255)
COLOR_BANNER = (255, 220, 80)


def draw_scene(surface, hook, fish_list):
    surface.fill(COLOR_SKY, pygame.Rect(0, 0, WIDTH, SURFACE_Y))
    surface.fill(COLOR_WATER, pygame.Rect(0, SURFACE_Y, WIDTH, HEIGHT - SURFACE_Y))

    pygame.draw.rect(surface, COLOR_BOAT, (hook.x - 40, SURFACE_Y - 20, 80, 22))

    pygame.draw.line(surface, COLOR_LINE, (hook.x, SURFACE_Y), (hook.x, hook.y), 2)
    pygame.draw.circle(surface, COLOR_HOOK, (int(hook.x), int(hook.y)), 7)

    for fish in fish_list:
        pygame.draw.ellipse(surface, fish.color, fish.get_rect())


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_text_right(surface, font, text, y, margin=10, color=COLOR_TEXT):
    surf = font.render(text, True, color)
    surface.blit(surf, (surface.get_width() - surf.get_width() - margin, y))


def draw_overlay(surface, alpha=160):
    """Dim the whole screen (used behind the end-of-round banner)."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    surface.blit(overlay, (0, 0))


def draw_banner(surface, font, text, y_offset=0, color=COLOR_BANNER):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(surface.get_width() // 2,
                                 surface.get_height() // 2 + y_offset))
    surface.blit(surf, rect)