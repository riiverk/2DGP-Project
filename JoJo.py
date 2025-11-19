from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

from state_machine import StateMachine


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


class Idle:
    def __init__(self, jojo):
        self.jojo = jojo

    def enter(self, e):
        self.jojo.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame = (self.jojo.frame + 1) % 8

    def draw(self):
        self.jojo.image.clip_draw(
            int(self.jojo.frame) * 70 + 2,
            self.jojo.image_h - 145,
            70, 120,
            self.jojo.x, self.jojo.y,
            210, 360
        )


class Run:
    def __init__(self, jojo):
        self.jojo = jojo

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.jojo.dir = 1
            self.jojo.face_dir = 1
        elif left_down(e) or right_up(e):
            self.jojo.dir = -1
            self.jojo.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame = (self.jojo.frame + 1) % 8
        self.jojo.x += self.jojo.dir * self.jojo.speed

    def draw(self):
        self.jojo.image.clip_draw(
            int(self.jojo.frame) * 70 + 2,
            self.jojo.image_h - 145,
            70, 120,
            self.jojo.x, self.jojo.y,
            210, 360
        )


class JoJo:
    def __init__(self):
        self.x, self.y = 1300, 400
        self.frame = 0
        self.face_dir = -1
        self.dir = 0
        self.image = load_image('JoJo.png')
        self.image_h = 4800
        self.speed = 1

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
