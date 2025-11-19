from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_RETURN
import json

from state_machine import StateMachine

# 모듈 로드 시 JSON 한 번만 읽기
with open('jojo.json', 'r') as f:
    _sprite_list = json.load(f)
Sprite_data = {sprite['name']: sprite for sprite in _sprite_list}


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def time_out(e):
    return e[0] == 'TIME_OUT'


def jump_end_run(e):
    return e[0] == 'JUMP_END_RUN'


def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN


class Idle:
    def __init__(self, jojo):
        self.jojo = jojo

    def enter(self, e):
        self.jojo.dir = 0
        self.jojo.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame = (self.jojo.frame + 0.01) % 16

    def draw(self):
        frame_name = f'Idle{int(self.jojo.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        pic_y = self.jojo.image_h - y - h
        self.jojo.image.clip_draw(x, pic_y, w, h, self.jojo.x, self.jojo.y, w * 3, h * 3)


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
        elif jump_end_run(e):
            if self.jojo.right_pressed:
                self.jojo.dir = 1
                self.jojo.face_dir = 1
            elif self.jojo.left_pressed:
                self.jojo.dir = -1
                self.jojo.face_dir = -1
        self.jojo.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame = (self.jojo.frame + 0.03) % 10
        self.jojo.x += self.jojo.dir * self.jojo.speed

    def draw(self):
        frame_name = f'Walk{int(self.jojo.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        src_y = self.jojo.image_h - y - h
        self.jojo.image.clip_draw(x, src_y, w, h, self.jojo.x, self.jojo.y, w * 3, h * 3)


class Jump:
    def __init__(self, jojo):
        self.jojo = jojo
        self.start_y = 0

    def enter(self, e):
        self.jojo.frame = 0
        self.start_y = self.jojo.y

    def exit(self, e):
        self.jojo.y = self.start_y

    def do(self):
        self.jojo.frame += 0.05
        # Jump1~Jump8: 상승, Jump8~Jump14: 하강, Jump14~Jump17: 제자리
        if self.jojo.frame < 7:
            self.jojo.y += 2
        elif self.jojo.frame < 13:
            self.jojo.y -= 7 / 6 * 2  # 상승/하강 비율 맞춤

        # 좌우 이동
        if self.jojo.left_pressed:
            self.jojo.x -= self.jojo.speed * 2
        if self.jojo.right_pressed:
            self.jojo.x += self.jojo.speed * 2

        if self.jojo.frame >= 17:
            self.jojo.frame = 16.9
            if self.jojo.left_pressed or self.jojo.right_pressed:
                self.jojo.state_machine.handle_state_event(('JUMP_END_RUN', None))
            else:
                self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_name = f'Jump{int(self.jojo.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        src_y = self.jojo.image_h - y - h
        self.jojo.image.clip_draw(x, src_y, w, h, self.jojo.x, self.jojo.y, w * 3, h * 3)


class Kick:
    def __init__(self, jojo):
        self.jojo = jojo

    def enter(self, e):
        self.jojo.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame += 0.05
        if self.jojo.frame >= 9:
            self.jojo.frame = 8.9
            self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_name = f'Kick{int(self.jojo.frame) + 1}'
        frame_data = Sprite_data[frame_name]
        x, y, w, h = frame_data['x'], frame_data['y'], frame_data['width'], frame_data['height']
        src_y = self.jojo.image_h - y - h
        self.jojo.image.clip_draw(x, src_y, w, h, self.jojo.x, self.jojo.y, w * 3, h * 3)


class JoJo:
    def __init__(self):
        self.x, self.y = 1300, 400
        self.frame = 0
        self.face_dir = -1
        self.dir = 0
        self.image = load_image('JoJo.png')
        self.image_h = 4800
        self.speed = 1
        self.left_pressed = False
        self.right_pressed = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.KICK = Kick(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN, up_down: self.JUMP, enter_down: self.KICK},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, up_down: self.JUMP, enter_down: self.KICK},
                self.JUMP: {time_out: self.IDLE, jump_end_run: self.RUN},
                self.KICK: {time_out: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.left_pressed = True
            elif event.key == SDLK_RIGHT:
                self.right_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.left_pressed = False
            elif event.key == SDLK_RIGHT:
                self.right_pressed = False
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
