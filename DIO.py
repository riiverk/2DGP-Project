from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w
import json

from state_machine import StateMachine

# 모듈 로드 시 JSON 한 번만 읽기
with open('dio.json', 'r') as f:
    _sprite_list = json.load(f)
Sprite_data = {sprite['name']: sprite for sprite in _sprite_list}


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def time_out(e):
    return e[0] == 'TIME_OUT'


def jump_end_run(e):
    return e[0] == 'JUMP_END_RUN'


class Idle:
    def __init__(self, dio):
        self.dio = dio

    def enter(self, e):
        self.dio.dir = 0
        self.dio.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame = (self.dio.frame + 0.01) % 5

    def draw(self):
        frame_name = f'Idle{int(self.dio.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        pic_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, pic_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Run:
    def __init__(self, dio):
        self.dio = dio

    def enter(self, e):
        if d_down(e) or a_up(e):
            self.dio.dir = 1
            self.dio.face_dir = 1
        elif a_down(e) or d_up(e):
            self.dio.dir = -1
            self.dio.face_dir = -1
        elif jump_end_run(e):
            if self.dio.d_pressed:
                self.dio.dir = 1
                self.dio.face_dir = 1
            elif self.dio.a_pressed:
                self.dio.dir = -1
                self.dio.face_dir = -1
        self.dio.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame = (self.dio.frame + 0.03) % 16
        self.dio.x += self.dio.dir * self.dio.speed

    def draw(self):
        frame_name = f'Walk{int(self.dio.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Jump:
    def __init__(self, dio):
        self.dio = dio
        self.start_y = 0

    def enter(self, e):
        self.dio.frame = 0
        self.start_y = self.dio.y

    def exit(self, e):
        self.dio.y = self.start_y

    def do(self):
        self.dio.frame += 0.05
        # 상승, 하강, 착지 (JoJo와 동일한 높이)
        if self.dio.frame < 4:
            self.dio.y += 3.5
        elif self.dio.frame < 8:
            self.dio.y -= 3.5

        # 좌우 이동
        if self.dio.a_pressed:
            self.dio.x -= self.dio.speed * 2
        if self.dio.d_pressed:
            self.dio.x += self.dio.speed * 2

        if self.dio.frame >= 10:
            self.dio.frame = 9.9
            if self.dio.a_pressed or self.dio.d_pressed:
                self.dio.state_machine.handle_state_event(('JUMP_END_RUN', None))
            else:
                self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_name = f'Jump{int(self.dio.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class DIO:
    def __init__(self):
        self.x, self.y = 300, 400
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('DIO.png')
        self.image_h = 9061
        self.speed = 1
        self.a_pressed = False
        self.d_pressed = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {d_down: self.RUN, a_down: self.RUN, d_up: self.RUN, a_up: self.RUN, w_down: self.JUMP},
                self.RUN: {d_up: self.IDLE, a_up: self.IDLE, d_down: self.IDLE, a_down: self.IDLE, w_down: self.JUMP},
                self.JUMP: {time_out: self.IDLE, jump_end_run: self.RUN}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.a_pressed = True
            elif event.key == SDLK_d:
                self.d_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.a_pressed = False
            elif event.key == SDLK_d:
                self.d_pressed = False
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
