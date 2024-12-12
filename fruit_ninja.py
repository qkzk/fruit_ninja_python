import os
from random import randint

import pgzrun
from pgzero import tone
from pgzero.keyboard import Keyboard
from pgzero.screen import Screen

screen: Screen
keyboard: Keyboard

os.environ["SDL_VIDEO_CENTERED"] = "1"

WIDTH = 1024
HEIGHT = 768
TITLE = "Fruit Ninja"


TONES = [tone.create(f"{letter}5", 0.2) for letter in "ABCDEF"]
RADIUS = 60
REFRESH_COUNT = 60


class Color:
    @staticmethod
    def random():
        return (
            randint(30, 150),
            randint(30, 150),
            randint(30, 150),
        )


class Ball:
    def __init__(self):
        self.position = [randint(1, WIDTH), randint(1, HEIGHT)]
        self.speed = [randint(-1, 1), randint(-1, 1)]
        self.is_hit = False
        self.color = Color.random()
        self.radius = RADIUS

    def move(self):
        if self.is_hit:
            return
        self.position[0] += self.speed[0]
        self.position[1] += self.speed[1]

    def shrink(self):
        if not self.is_hit:
            return
        self.radius -= 1

    def draw(self):
        screen.draw.filled_circle(self.position, self.radius, self.color)

    def is_out(self) -> bool:
        return (
            self.position[0] + self.radius < 0
            or self.position[0] - self.radius > WIDTH
            or self.position[1] + self.radius < 0
            or self.position[1] - self.radius > HEIGHT
        )

    def is_inside(self, pos: tuple[int, int]) -> bool:
        dsquare = (pos[0] - self.position[0]) ** 2 + (pos[1] - self.position[1]) ** 2
        return dsquare < self.radius**2


class Game:
    def __init__(self) -> None:
        self.balls: list[Ball]
        self.frame_counter: int
        self.tone_index: int
        self.reset()

    def reset(self):
        self.balls = [Ball() for _ in range(5)]
        self.frame_counter = 0
        self.tone_index = 0

    def draw(self):
        for ball in self.balls:
            ball.draw()

    def keyboard(self):
        if keyboard.Escape or keyboard.Q:
            exit()

    def update(self):
        for ball in self.balls:
            ball.move()
            ball.shrink()

        self.balls = [
            ball for ball in self.balls if not ball.is_out() and ball.radius > 0
        ]

        self.frame_counter += 1
        if self.frame_counter > REFRESH_COUNT:
            self.balls.append(Ball())
            self.balls.append(Ball())
            self.frame_counter = 0

    def mouse(self, pos: tuple[int, int]):
        for ball in self.balls:
            if ball.is_hit:
                continue
            if ball.is_inside(pos):
                TONES[self.tone_index].play()
                self.tone_index = (self.tone_index + 1) % len(TONES)
                ball.is_hit = True


def update():
    game.keyboard()
    game.update()


def draw():
    screen.fill("GREY")
    game.draw()


def on_mouse_move(pos: tuple[int, int]):
    game.mouse(pos)


game = Game()

pgzrun.go()
