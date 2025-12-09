from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_RETURN
import json

from state_machine import StateMachine
import game_world
import game_framework

# 모듈 로드 시 JSON 한 번만 읽기
with open('jojo.json', 'r') as f:
    _sprite_list = json.load(f)
Sprite_data = {sprite['name']: sprite for sprite in _sprite_list}

JoJo_Sprite = {
    'idle': [
        (4, 7627, 64, 117), (80, 7627, 64, 117), (155, 7627, 64, 117), (232, 7627, 67, 117),
        (310, 7627, 69, 117), (390, 7627, 67, 117), (467, 7627, 64, 117), (541, 7627, 64, 117),
        (615, 7627, 64, 117), (688, 7627, 64, 117), (759, 7627, 64, 117), (834, 7627, 67, 117),
        (912, 7627, 69, 117), (989, 7627, 67, 117), (1065, 7627, 64, 117), (1141, 7627, 64, 117),
        (1216, 7627, 64, 117), (1290, 7627, 64, 117), (1362, 7627, 64, 117), (1436, 7627, 67, 117),
        (1516, 7627, 69, 117), (1595, 7627, 67, 117), (1671, 7627, 64, 117), (1749, 7627, 64, 117)
    ], 'forward': [
        (4, 6779, 67, 115), (94, 6779, 56, 113), (174, 6779, 47, 113), (247, 6779, 48, 113),
        (316, 6779, 53, 113), (387, 6779, 70, 113), (473, 6779, 77, 114), (564, 6779, 72, 115),
        (658, 6779, 69, 115), (746, 6779, 62, 115), (826, 6779, 47, 115), (897, 6779, 54, 113),
        (959, 6779, 71, 113), (1037, 6779, 75, 113), (1124, 6779, 76, 113), (1209, 6779, 72, 113)
    ], 'backward': [
        (1395, 6779, 94, 113), (1497, 6779, 78, 113), (1583, 6779, 59, 113), (1656, 6779, 52, 113),
        (1723, 6779, 46, 113), (1782, 6779, 59, 113), (1854, 6779, 64, 113), (1931, 6779, 72, 113),
        (2016, 6779, 77, 113), (2105, 6779, 70, 113), (2186, 6779, 53, 113), (2253, 6779, 48, 113),
        (2314, 6779, 47, 113), (2374, 6779, 56, 113), (2443, 6779, 67, 113), (2523, 6779, 72, 113),
    ], 'crouch': [  # 6번째 인덱스에서 기다림
        (914, 6905, 97, 102), (1026, 6905, 91, 75), (1128, 6905, 104, 72), (1245, 6905, 89, 72),
        (1348, 6905, 95, 72), (1455, 6905, 89, 72), (2186, 6905, 90, 76), (2290, 6905, 90, 74),
        (2392, 6905, 71, 102), (2471, 6905, 76, 118), (2558, 6905, 74, 117), (2641, 6905, 76, 117),
        (2725, 6905, 71, 117), (2804, 6905, 69, 117), (2883, 6905, 65, 117), (2956, 6905, 64, 117)
    ], 'jump': [
        (2, 6496, 97, 102), (109, 6486, 57, 127), (183, 6490, 90, 117), (281, 6504, 88, 99),
        (383, 6522, 80, 83), (480, 6529, 85, 79), (576, 6514, 99, 112), (683, 6494, 100, 142),
        (793, 6491, 111, 138), (914, 6488, 125, 144), (1043, 6488, 104, 151), (1154, 6488, 102, 150),
        (1269, 6497, 91, 75), (1372, 6497, 90, 74), (1476, 6496, 71, 102), (1557, 6496, 76, 118),
        (1649, 6496, 74, 117), (1740, 6496, 76, 117), (1830, 6496, 71, 117), (1923, 6496, 69, 117),
        (2010, 6496, 65, 117), (2095, 6496, 64, 117)
    ], 'intro': [   # 여기서부터는 y = 7750 - y - h로 draw
        (2669, 6494, 74, 116), (2755, 6494, 82, 116), (2848, 6494, 92, 116), (2951, 6494, 100, 116),
        (3064, 6495, 84, 115), (3163, 6495, 82, 115), (3258, 6495, 103, 115), (3373, 6495, 102, 115),
        (3489, 6495, 103, 115), (3600, 6495, 102, 115), (3710, 6495, 102, 115), (3820, 6495, 103, 115),
        (3935, 6495, 93, 115), (4040, 6495, 82, 115), (4136, 6494, 74, 116)
    ], 'lightattack': [
        (6, 1977, 74, 113), (88, 1978, 91, 112), (185, 1977, 88, 113), (281, 1977, 102, 113),
        (390, 1975, 88, 115), (486, 1973, 69, 117), (562, 1973, 65, 117), (637, 1973, 64, 117)
    ], 'crouch_la': [
        (827, 2022, 97, 69), (932, 2024, 112, 67), (1050, 2019, 141, 72), (1199, 2008, 108, 81),
        (1314, 2007, 100, 82), (1423, 2011, 97, 78), (1527, 2011, 96, 78), (1633, 2016, 91, 75)
    ]
}

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


def crouch_end_run(e):
    return e[0] == 'CROUCH_END_RUN'


def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


class Idle:
    def __init__(self, jojo):
        self.jojo = jojo
        self.TIME_PER_ACTION = 2.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 24

    def enter(self, e):
        self.jojo.dir = 0
        self.jojo.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame = (self.jojo.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 24

    def draw(self):
        frame_index = int(self.jojo.frame)
        x, y, w, h = JoJo_Sprite['idle'][frame_index]
        self.jojo.image.clip_composite_draw(x, y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class Run:
    def __init__(self, jojo):
        self.jojo = jojo
        self.TIME_PER_ACTION = 0.8
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 16
        self.RUN_SPEED_PPS = 200

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.jojo.dir = 1
            self.jojo.face_dir = 1
        elif left_down(e) or right_up(e):
            self.jojo.dir = -1
            self.jojo.face_dir = -1
        elif jump_end_run(e) or crouch_end_run(e):
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
        self.jojo.frame = (self.jojo.frame + self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time) % 16
        self.jojo.x += self.jojo.dir * self.RUN_SPEED_PPS * game_framework.frame_time

    def draw(self):
        frame_index = int(self.jojo.frame)
        if self.jojo.dir == -1:
            x, y, w, h = JoJo_Sprite['forward'][frame_index]
        else:
            x, y, w, h = JoJo_Sprite['backward'][frame_index]
        self.jojo.image.clip_composite_draw(x, y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class Jump:
    def __init__(self, jojo):
        self.jojo = jojo
        self.start_y = 0
        self.TIME_PER_ACTION = 1.1
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 22
        self.JUMP_SPEED_PPS = 400

    def enter(self, e):
        self.jojo.frame = 0
        self.start_y = self.jojo.y

    def exit(self, e):
        self.jojo.y = self.start_y

    def do(self):
        self.jojo.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time

        if self.jojo.frame < 7:
            self.jojo.y += 2
        elif self.jojo.frame < 15:
            self.jojo.y -= 7 / 8 * 2

        if self.jojo.left_pressed:
            self.jojo.x -= self.JUMP_SPEED_PPS * game_framework.frame_time
        if self.jojo.right_pressed:
            self.jojo.x += self.JUMP_SPEED_PPS * game_framework.frame_time

        if self.jojo.frame >= 22:
            self.jojo.frame = 21.9
            if self.jojo.left_pressed or self.jojo.right_pressed:
                self.jojo.state_machine.handle_state_event(('JUMP_END_RUN', None))
            else:
                self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.jojo.frame)
        x, y, w, h = JoJo_Sprite['jump'][frame_index]
        self.jojo.image.clip_composite_draw(x, y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class LightAttack:
    def __init__(self, jojo):
        self.jojo = jojo
        self.TIME_PER_ACTION = 0.4
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 8
        self.hitpoint = 2
        self.hit = False

    def enter(self, e):
        self.jojo.frame = 0
        self.hit = False

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.jojo.frame >= 8:
            self.jojo.frame = 7.9
            self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.jojo.frame)
        x, y, w, h = JoJo_Sprite['lightattack'][frame_index]
        src_y = self.jojo.image_h - y - h
        self.jojo.image.clip_composite_draw(x, src_y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class Crouch:
    def __init__(self, jojo):
        self.jojo = jojo
        self.TIME_PER_ACTION = 1.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 16

    def enter(self, e):
        self.jojo.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time

        if self.jojo.down_pressed and self.jojo.frame >= 6:
            self.jojo.frame = 6
        elif not self.jojo.down_pressed and self.jojo.frame >= 16:
            self.jojo.frame = 15.9
            if self.jojo.left_pressed or self.jojo.right_pressed:
                self.jojo.state_machine.handle_state_event(('CROUCH_END_RUN', None))
            else:
                self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.jojo.frame)
        x, y, w, h = JoJo_Sprite['crouch'][frame_index]
        self.jojo.image.clip_composite_draw(x, y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class CrouchLA:
    def __init__(self, jojo):
        self.jojo = jojo
        self.TIME_PER_ACTION = 0.4
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 8
        self.hitpoint = 4
        self.hit = False

    def enter(self, e):
        self.jojo.frame = 0
        self.hit = False

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.jojo.frame >= 8:
            self.jojo.frame = 7.9
            self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.jojo.frame)
        x, y, w, h = JoJo_Sprite['crouch_la'][frame_index]
        src_y = self.jojo.image_h - y - h
        self.jojo.image.clip_composite_draw(x, src_y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class Intro:
    def __init__(self, jojo):
        self.jojo = jojo
        self.TIME_PER_ACTION = 1.5
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = 15

    def enter(self, e):
        self.jojo.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.jojo.frame += self.FRAMES_PER_ACTION * self.ACTION_PER_TIME * game_framework.frame_time
        if self.jojo.frame >= 15:
            self.jojo.frame = 14.9
            self.jojo.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        frame_index = int(self.jojo.frame)
        x, y, w, h = JoJo_Sprite['intro'][frame_index]
        src_y = self.jojo.image_h - y - h
        self.jojo.image.clip_composite_draw(x, src_y, w, h, 0, 'h', self.jojo.x, self.jojo.y, w * 3, h * 3)


class JoJo:
    def __init__(self):
        self.x, self.y = 1300, 200
        self.frame = 0
        self.face_dir = -1
        self.dir = 0
        self.image = load_image('JoJo_fix.png')
        self.image_h = 7750
        self.speed = 1
        self.left_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        self.hp = 100
        self.point = 0
        self.theWorld = False

        self.IDLE = Idle(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        self.LIGHTATTACK = LightAttack(self)
        self.CROUCH = Crouch(self)
        self.CROUCH_LA = CrouchLA(self)
        self.INTRO = Intro(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN, up_down: self.JUMP, enter_down: self.LIGHTATTACK, down_down: self.CROUCH},
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE, left_down: self.IDLE, up_down: self.JUMP, enter_down: self.LIGHTATTACK, down_down: self.CROUCH},
                self.JUMP: {time_out: self.IDLE, jump_end_run: self.RUN},
                self.LIGHTATTACK: {time_out: self.IDLE},
                self.CROUCH: {time_out: self.IDLE, enter_down: self.CROUCH_LA, crouch_end_run: self.RUN},
                self.CROUCH_LA: {time_out: self.CROUCH},
                self.INTRO: {time_out: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if self.state_machine.cur_state == self.INTRO:
            return

        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.left_pressed = True
            elif event.key == SDLK_RIGHT:
                self.right_pressed = True
            elif event.key == SDLK_DOWN:
                self.down_pressed = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.left_pressed = False
            elif event.key == SDLK_RIGHT:
                self.right_pressed = False
            elif event.key == SDLK_DOWN:
                self.down_pressed = False

        if self.state_machine.cur_state == self.CROUCH and not self.down_pressed:
            return

        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        frame_index = int(self.frame)

        if self.state_machine.cur_state == self.IDLE:
            x, y, w, h = JoJo_Sprite['idle'][frame_index]
        elif self.state_machine.cur_state == self.RUN:
            if self.dir == -1:
                x, y, w, h = JoJo_Sprite['forward'][frame_index]
            else:
                x, y, w, h = JoJo_Sprite['backward'][frame_index]
        elif self.state_machine.cur_state == self.CROUCH:
            x, y, w, h = JoJo_Sprite['crouch'][frame_index]
        elif self.state_machine.cur_state == self.JUMP:
            x, y, w, h = JoJo_Sprite['jump'][frame_index]
        elif self.state_machine.cur_state == self.LIGHTATTACK:
            x, y, w, h = JoJo_Sprite['lightattack'][frame_index]
            y = 7750 - y - h
            w, h = w * 3, h * 3
            extend = 80
            if self.face_dir == -1:
                return self.x - w // 2 - extend, self.y - h // 2, self.x + w // 2, self.y + h // 2
            else:
                return self.x - w // 2, self.y - h // 2, self.x + w // 2 + extend, self.y + h // 2
        elif self.state_machine.cur_state == self.CROUCH_LA:
            x, y, w, h = JoJo_Sprite['crouch_la'][frame_index]
            y = 7750 - y - h
            w, h = w * 3, h * 3
            extend = 100
            if self.face_dir == -1:
                return self.x - w // 2 - extend, self.y - h // 2, self.x + w // 2, self.y + h // 2
            else:
                return self.x - w // 2, self.y - h // 2, self.x + w // 2 + extend, self.y + h // 2
        elif self.state_machine.cur_state == self.INTRO:
            x, y, w, h = JoJo_Sprite['intro'][frame_index]
            y = 7750 - y - h
        else:
            x, y, w, h = JoJo_Sprite['idle'][0]

        w, h = w * 3, h * 3
        return self.x - w // 2, self.y - h // 2, self.x + w // 2, self.y + h // 2

    def handle_collision(self, group, other):
       if group == 'DIO:JoJo':
            attack_state = other.state_machine.cur_state
            if attack_state == other.LIGHTATTACK or attack_state == other.CROUCH_LA:
                if not attack_state.hit and int(other.frame) == attack_state.hitpoint:
                    attack_state.hit = True
                    if attack_state == other.LIGHTATTACK:
                        self.hp -= 8
                    elif attack_state == other.CROUCH_LA:
                        self.hp -= 5
                    self.point += 2



