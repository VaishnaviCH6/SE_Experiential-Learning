"""
GameEngine: owns the hook and the fish, and runs one frame's worth of
game logic.

- Task 1: catch detection is overlap based (see game/catch.py).
- Task 2: several fish types (see game/fish.py); caught fish respawn as
  the same type so the pond never empties.
- Task 3: casting is player-controlled via handle_cast().
- Task 4: 30-second round timer, game-over screen, restart().
"""

import math

from game.hook import Hook, IDLE
from game.fish import Fish
from game.catch import check_catch
from game import renderer
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y

ROUND_SECONDS = 30

PLAYING = "playing"
GAME_OVER = "game_over"

# (fish type, start x, depth y, direction)
INITIAL_FISH = [
    ("minnow", 100, 180, 1),
    ("bass",   450, 230, -1),
    ("golden", 250, 290, 1),
    ("minnow", 550, 350, -1),
    ("bass",   200, 410, 1),
]


class GameEngine:
    def __init__(self):
        self.restart()

    # ---- round control -------------------------------------------------

    def restart(self):
        """Start a fresh round: score, timer, hook and fish all reset."""
        self.hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
        self.fish_list = [
            Fish.from_type(kind, x, y, direction)
            for kind, x, y, direction in INITIAL_FISH
        ]
        self.hooked_fish = None
        self.score = 0
        self.time_left = float(ROUND_SECONDS)
        self.state = PLAYING

    def is_over(self):
        return self.state == GAME_OVER

    def handle_cast(self):
        """Player pressed the cast key. Ignored unless the round is on
        and the hook is idle (so it can't interrupt a cast in progress)."""
        if self.state == PLAYING:
            self.hook.try_cast()

    def _respawn(self, fish):
        """Put a fresh fish of the same type back at the screen edge."""
        direction = 1 if fish.speed > 0 else -1
        x = -fish.width if direction > 0 else WIDTH
        self.fish_list.append(Fish.from_type(fish.kind, x, fish.y_home, direction))

    def _end_round(self):
        self.state = GAME_OVER
        self.time_left = 0.0
        if self.hooked_fish is not None:      # never scored -> release it
            self._respawn(self.hooked_fish)
            self.hooked_fish = None
        self.hook.reset()

    # ---- per-frame logic -----------------------------------------------

    def update(self, dt):
        """Advance one frame. dt = seconds since the previous frame."""
        if self.state == GAME_OVER:
            for fish in self.fish_list:       # pond keeps swimming behind the banner
                fish.update(WIDTH)
            return

        self.time_left -= dt
        if self.time_left <= 0:
            self._end_round()                 # no catches are processed on this frame
            return

        self.hook.update()

        for fish in self.fish_list:
            fish.update(WIDTH)

        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y
            if self.hook.state == IDLE:
                self.score += self.hooked_fish.point_value
                self._respawn(self.hooked_fish)
                self.hooked_fish = None
        elif self.hook.state != IDLE:
            caught = check_catch(self.hook, self.fish_list)
            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

    # ---- drawing ---------------------------------------------------------

    def draw(self, surface, font, big_font=None):
        big_font = big_font or font
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)
        renderer.draw_scene(surface, self.hook, draw_list)

        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        secs = math.ceil(self.time_left)
        timer_color = (255, 90, 90) if secs <= 5 else renderer.COLOR_TEXT
        renderer.draw_text_right(surface, font, f"Time: {secs}", 10, color=timer_color)

        if self.state == PLAYING:
            renderer.draw_text(surface, font, "SPACE: cast", (10, HEIGHT - 30))
        else:
            renderer.draw_overlay(surface)
            renderer.draw_banner(surface, big_font, "Time's up!", y_offset=-50)
            renderer.draw_banner(surface, big_font, f"Final score: {self.score}", y_offset=10)
            renderer.draw_banner(surface, font, "Press R to play again", y_offset=70,
                                 color=renderer.COLOR_TEXT)