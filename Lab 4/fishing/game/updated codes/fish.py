"""
Fish: swims horizontally at a fixed depth, wrapping around when it
exits the screen. Several fish types exist, differing in speed, point
value and look (size + color).
"""

import pygame

# Task 2: fish types. Slow/low-value -> fast/high-value.
FISH_TYPES = {
    "minnow": dict(speed=1.5, point_value=10, width=30, height=14, color=(150, 200, 230)),
    "bass":   dict(speed=2.5, point_value=25, width=46, height=22, color=(90, 190, 110)),
    "golden": dict(speed=4.5, point_value=50, width=32, height=16, color=(255, 190, 40)),
}


class Fish:
    def __init__(self, x, y, speed, width=36, height=18, point_value=10,
                 color=(80, 180, 220), kind="minnow"):
        self.x = float(x)
        self.y = y
        self.y_home = y          # swimming depth; self.y is overwritten while hooked
        self.speed = speed
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color
        self.kind = kind

    @classmethod
    def from_type(cls, kind, x, y, direction=1):
        """Build a fish of a named type. direction: 1 = right, -1 = left."""
        spec = FISH_TYPES[kind]
        return cls(
            x, y, spec["speed"] * direction,
            width=spec["width"], height=spec["height"],
            point_value=spec["point_value"], color=spec["color"], kind=kind,
        )

    def update(self, screen_width):
        self.x += self.speed
        if self.speed > 0 and self.x > screen_width:
            self.x = -self.width
        elif self.speed < 0 and self.x < -self.width:
            self.x = screen_width

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )