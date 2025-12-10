from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_a, SDLK_d, SDLK_w, SDLK_s, SDLK_h, SDLK_f, SDLK_SPACE
import json

from state_machine import StateMachine
import game_framework

# 모듈 로드 시 JSON 한 번만 읽기
with open('dio.json', 'r') as f:
    _sprite_list = json.load(f)
Sprite_data = {sprite['name']: sprite for sprite in _sprite_list}

DIO_Sprite = {  # 디오 y는 src_y = 10400 - y - h로 draw
    'intro': [
        (1431, 7600, 66, 122), (1502, 7600, 66, 122), (1573, 7600, 66, 122), (1645, 7600, 66, 122), (1715, 7601, 66, 121),
        (1787, 7600, 66, 122), (1857, 7604, 90, 118), (1951, 7604, 94, 118), (2049, 7603, 80, 116),
        (2135, 7605, 69, 114), (2209, 7605, 67, 118)
    ], 'idle': [
        (3, 14, 64, 120), (72, 14, 64, 120), (142, 14, 64, 120), (211, 14, 64, 120), (280, 14, 64, 120),
        (349, 14, 63, 120), (418, 14, 62, 120), (486, 14, 63, 120), (555, 14, 64, 120), (625, 14, 64, 120),
        (695, 14, 64, 120), (765, 14, 64, 120), (834, 14, 64, 120), (904, 14, 64, 120), (974, 14, 64, 120),
        (1043, 14, 67, 120), (1116, 14, 66, 120), (1188, 14, 65, 120), (1259, 14, 65, 120), (1329, 14, 64, 120),
        (1399, 14, 64, 120), (1470, 14, 64, 120), (1539, 14, 64, 120), (1608, 14, 64, 120), (1677, 14, 63, 120),
        (1747, 14, 62, 120), (1815, 14, 63, 120), (1884, 14, 64, 120), (1954, 14, 64, 120), (2024, 14, 64, 120),
        (2094, 14, 64, 120), (2164, 14, 64, 120), (2233, 14, 64, 120), (2303, 14, 64, 120), (2372, 14, 67, 120),
        (2444, 14, 66, 120), (2516, 14, 65, 120), (2587, 14, 65, 120)
    ], 'crouch': [  # 4에서 대기
        (460, 145, 67, 118), (536, 158, 83, 106), (626, 186, 79, 78), (712, 186, 78, 78),
        (1478, 185, 79, 78), (1566, 157, 83, 106), (1656, 145, 67, 118)
    ], 'forward': [
        (7, 272, 60, 115), (74, 273, 72, 114), (155, 274, 73, 113), (237, 274, 70, 113), (315, 273, 71, 114),
        (391, 272, 64, 113), (465, 271, 55, 114), (527, 271, 48, 114), (582, 271, 53, 114), (643, 272, 69, 114),
        (722, 273, 79, 114), (810, 273, 73, 114), (892, 273, 69, 114), (970, 273, 69, 114), (1048, 271, 57, 116),
        (1112, 271, 56, 116)
    ], 'backward': [
        (1297, 271, 53, 114), (1358, 272, 69, 114), (1436, 273, 79, 114), (1523, 273, 73, 114), (1605, 273, 69, 114),
        (1683, 272, 69, 115), (1763, 271, 58, 116), (1832, 271, 56, 116), (1896, 272, 60, 115), (1965, 272, 72, 115),
        (2046, 273, 73, 114), (2130, 273, 70, 114), (2209, 272, 71, 115), (2287, 272, 64 ,113), (2362, 271, 56, 114),
        (2425, 271, 48, 114)
    ], 'jump': [
        (1716, 453, 67, 118), (1790, 416, 78, 130), (1876, 415, 78, 131),
        (1962, 422, 77, 78), (2046, 423, 83, 71), (2136, 426, 85, 64), (2229, 411, 78, 88), (2317, 395, 60, 136),
        (2389, 396, 54, 148), (2389, 396, 54, 148), (2520, 493, 79, 78), (2608, 465, 83, 106), (2698, 453, 67, 118)
    ], 'lightattack': [
        (15, 1223, 50, 113), (72, 1224, 112, 112), (190, 1224, 86, 112), (282, 1223, 72, 113), (360, 1218, 67, 118)
    ], 'crouch_la': [
        (535, 1265, 98, 71), (638, 1267, 133, 70), (777, 1265, 105, 71), (888, 1264, 90, 72), (984, 1258, 79, 78)
    ], 'stand': [
        (9, 1073, 174, 129), (188, 1073, 174, 129), (369, 1072, 151, 130), (527, 1072, 151, 130), (685, 1072, 151, 130),
        (842, 1072, 151, 130), (998, 1079, 128, 123), (1133, 1065, 102, 137), (1240, 1065, 103, 137), (1349, 1064, 95, 139),
        (1451, 1063, 87, 139)
    ]
}

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


def crouch_end_run(e):
    return e[0] == 'CROUCH_END_RUN'


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


def h_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_h

def f_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_f

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


class Idle:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 38

    def enter(self, e):
        self.dio.dir = 0
        self.dio.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame = (self.dio.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 38

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['idle'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Run:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 0.8
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 16
        self.RUN_SPEED_PPS = 200

    def enter(self, e):
        if d_down(e) or a_up(e):
            self.dio.dir = 1
            self.dio.face_dir = 1
        elif a_down(e) or d_up(e):
            self.dio.dir = -1
            self.dio.face_dir = -1
        elif jump_end_run(e) or crouch_end_run(e):
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
        self.dio.frame = (self.dio.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 16
        self.dio.x += self.dio.dir * self.RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        frame_index = int(self.dio.frame)
        if self.dio.dir == 1:
            x, y, w, h = DIO_Sprite['forward'][frame_index]
        else:
            x, y, w, h = DIO_Sprite['backward'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Jump:
    def __init__(self, dio):
        self.dio = dio
        self.start_y = 0
        self.TIME_PER_ACTION = 0.65
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 13
        self.JUMP_SPEED_PPS = 400

    def enter(self, e):
        self.dio.frame = 0
        self.start_y = self.dio.y

    def exit(self, e):
        self.dio.y = self.start_y

    def do(self):
        self.dio.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time

        if self.dio.frame < 5:
            self.dio.y += 2.8
        elif self.dio.frame < 10:
            self.dio.y -= 2.8

        if self.dio.a_pressed:
            self.dio.x -= self.JUMP_SPEED_PPS * game_framework.frame_time
        if self.dio.d_pressed:
            self.dio.x += self.JUMP_SPEED_PPS * game_framework.frame_time

        if self.dio.frame >= 13:
            self.dio.frame = 12.9
            if self.dio.a_pressed or self.dio.d_pressed:
                self.dio.state_machine.handle_state_event(('JUMP_END_RUN', None))
            else:
                self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['jump'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Crouch:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 0.35
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 7
        self.base_idle_h = 120

    def enter(self, e):
        self.dio.frame = 0
        self.base_y = self.dio.y

    def exit(self, e):
        self.dio.y = self.base_y

    def do(self):
        self.dio.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time

        if self.dio.s_pressed and self.dio.frame >= 4:
            self.dio.frame = 4
        elif not self.dio.s_pressed and self.dio.frame >= 7:
            self.dio.frame = 6.9
            if self.dio.a_pressed or self.dio.d_pressed:
                self.dio.state_machine.handle_state_event(('CROUCH_END_RUN', None))
            else:
                self.dio.state_machine.handle_state_event(('TIME_OUT', None))

        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['crouch'][frame_index]
        height_diff = (self.base_idle_h - h) * 3 / 2
        self.dio.y = self.base_y - height_diff

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['crouch'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class LightAttack:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 0.25
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 5
        self.hitpoint = 2
        self.hit = False

    def enter(self, e):
        self.dio.frame = 0
        self.hit = False

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.dio.frame >= 5:
            self.dio.frame = 4.9
            self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['lightattack'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class CrouchLA:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 0.25
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 5
        self.hitpoint = 2
        self.hit = False

    def enter(self, e):
        self.dio.frame = 0
        self.hit = False

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.dio.frame >= 5:
            self.dio.frame = 4.9
            self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['crouch_la'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Intro:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 11

    def enter(self, e):
        self.dio.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.dio.frame >= 11:
            self.dio.frame = 10.9
            self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['intro'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class Stand:
    def __init__(self, dio):
        self.dio = dio
        self.TIME_PER_ACTION = 0.55
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 11
        self.hitpoint = [1, 2]
        self.hit = False
        self.damage_applied = False

    def enter(self, e):
        if self.dio.point >= 20:
            self.dio.point -= 20
            self.dio.frame = 0
            self.hit = False
            self.damage_applied = False
        else:
            self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def exit(self, e):
        pass

    def do(self):
        self.dio.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.dio.frame >= 11:
            self.dio.frame = 10.9
            self.dio.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.dio.frame)
        x, y, w, h = DIO_Sprite['stand'][frame_index]
        src_y = self.dio.image_h - y - h
        self.dio.image.clip_draw(x, src_y, w, h, self.dio.x, self.dio.y, w * 3, h * 3)


class DIO:
    def __init__(self):
        self.x, self.y = 300, 200
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('DIO_fix.png')
        self.image_h = 10400
        self.speed = 1
        self.a_pressed = False
        self.d_pressed = False
        self.s_pressed = False
        self.hp = 100
        self.point = 0
        self.theWorld = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.CROUCH = Crouch(self)
        self.LIGHTATTACK = LightAttack(self)
        self.CROUCH_LA = CrouchLA(self)
        self.INTRO = Intro(self)
        self.STAND = Stand(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {d_down: self.RUN, a_down: self.RUN, d_up: self.RUN, a_up: self.RUN, w_down: self.JUMP, s_down: self.CROUCH, f_down: self.LIGHTATTACK, space_down: self.STAND},
                self.RUN: {d_up: self.IDLE, a_up: self.IDLE, d_down: self.IDLE, a_down: self.IDLE, w_down: self.JUMP, s_down: self.CROUCH, f_down: self.LIGHTATTACK, space_down: self.STAND},
                self.JUMP: {time_out: self.IDLE, jump_end_run: self.RUN},
                self.CROUCH: {time_out: self.IDLE, f_down: self.CROUCH_LA, crouch_end_run: self.RUN},
                self.LIGHTATTACK: {time_out: self.IDLE},
                self.CROUCH_LA: {time_out: self.CROUCH},
                self.INTRO: {time_out: self.IDLE},
                self.STAND: {time_out: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def reset_key_states(self):
        self.a_pressed = False
        self.d_pressed = False
        self.s_pressed = False

    def handle_event(self, event):
        if self.state_machine.cur_state == self.INTRO:
            if event.type == SDL_KEYUP:
                if event.key == SDLK_a:
                    self.a_pressed = False
                elif event.key == SDLK_d:
                    self.d_pressed = False
                elif event.key == SDLK_s:
                    self.s_pressed = False
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.a_pressed = True
            elif event.key == SDLK_d:
                self.d_pressed = True
            elif event.key == SDLK_s:
                self.s_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.a_pressed = False
            elif event.key == SDLK_d:
                self.d_pressed = False
            elif event.key == SDLK_s:
                self.s_pressed = False

        if self.state_machine.cur_state == self.CROUCH and not self.s_pressed:
            return

        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        frame_index = int(self.frame)

        if self.state_machine.cur_state == self.IDLE:
            x, y, w, h = DIO_Sprite['idle'][frame_index]
        elif self.state_machine.cur_state == self.RUN:
            if self.dir == 1:
                x, y, w, h = DIO_Sprite['forward'][frame_index]
            else:
                x, y, w, h = DIO_Sprite['backward'][frame_index]
        elif self.state_machine.cur_state == self.JUMP:
            x, y, w, h = DIO_Sprite['jump'][frame_index]
        elif self.state_machine.cur_state == self.CROUCH:
            x, y, w, h = DIO_Sprite['crouch'][frame_index]
        elif self.state_machine.cur_state == self.LIGHTATTACK:
            x, y, w, h = DIO_Sprite['lightattack'][frame_index]
            w, h = w * 3, h * 3
            extend = 80
            if self.face_dir == 1:
                return self.x - w // 2, self.y - h // 2, self.x + w // 2 + extend, self.y + h // 2
            else:
                return self.x - w // 2 - extend, self.y - h // 2, self.x + w // 2, self.y + h // 2
        elif self.state_machine.cur_state == self.CROUCH_LA:
            x, y, w, h = DIO_Sprite['crouch_la'][frame_index]
            w, h = w * 3, h * 3
            extend = 100
            if self.face_dir == 1:
                return self.x - w // 2, self.y - h // 2, self.x + w // 2 + extend, self.y + h // 2
            else:
                return self.x - w // 2 - extend, self.y - h // 2, self.x + w // 2, self.y + h // 2
        elif self.state_machine.cur_state == self.INTRO:
            x, y, w, h = DIO_Sprite['intro'][frame_index]
        elif self.state_machine.cur_state == self.STAND:
            x, y, w, h = DIO_Sprite['stand'][frame_index]
            w, h = w * 3, h * 3
            extend = 150
            if self.face_dir == 1:
                return self.x - w // 2, self.y - h // 2, self.x + w // 2 + extend, self.y + h // 2
            else:
                return self.x - w // 2 - extend, self.y - h // 2, self.x + w // 2, self.y + h // 2
        else:
            x, y, w, h = DIO_Sprite['idle'][0]

        w, h = w * 3, h * 3
        return self.x - w // 2, self.y - h // 2, self.x + w // 2, self.y + h // 2

    def handle_collision(self, group, other):
        if group == 'DIO:JoJo':
            attack_state = other.state_machine.cur_state
            if attack_state == other.LIGHTATTACK or attack_state == other.CROUCH_LA:
                if not attack_state.hit and int(other.frame) == attack_state.hitpoint:
                    attack_state.hit = True
                    if attack_state == other.LIGHTATTACK:
                        if self.state_machine.cur_state == self.CROUCH:
                            self.hp -= 4
                        else:
                            self.hp -= 8
                    elif attack_state == other.CROUCH_LA:
                        if self.state_machine.cur_state == self.CROUCH:
                            self.hp -= 3
                        else:
                            self.hp -= 5
                    self.point += 5
                    other.point += 8
                    if self.point > 40: self.point = 40
                    if other.point > 40: other.point = 40
            elif attack_state == other.STAND:
                if not attack_state.hit and int(other.frame) in attack_state.hitpoint:
                    attack_state.hit = True
                last_frame = attack_state.FRAMES_PER_ACTION - 1
                if attack_state.hit and int(other.frame) == last_frame and not attack_state.damage_applied:
                    attack_state.damage_applied = True
                    self.hp -= 15
                    self.point += 10
                    other.point += 15
                    if self.point > 40: self.point = 40
                    if other.point > 40: other.point = 40