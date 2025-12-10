from pico2d import *

import music
from UI import *
import game_world
import game_framework
import result_mode
from JoJo import JoJo
from DIO import DIO

jojo = None
dio = None
intro_played = False
fight_signal = None
signal_shown = False
fight_signal_was_active = False
jojo_stand_active = False
dio_stand_active = False
stand_timer = 0
background = None
game_over = False

def init():
    global jojo, dio, intro_played, fight_signal, signal_shown, background, bgm
    global jojo_stand_active, dio_stand_active, stand_timer, fight_signal_was_active
    bgm = music.play_bgm
    bgm.repeat_play()

    jojo_stand_active = False
    dio_stand_active = False
    stand_timer = 0
    fight_signal_was_active = False
    background = Background()
    game_world.add_object(background, 0)

    jojo = JoJo()
    dio = DIO()

    if not intro_played:
        jojo.state_machine.cur_state = jojo.INTRO
        jojo.state_machine.cur_state.enter(('START', None))
        dio.state_machine.cur_state = dio.INTRO
        dio.state_machine.cur_state.enter(('START', None))
        intro_played = True

    signal_shown = False
    fight_signal = FightSignal()
    game_world.add_object(fight_signal, 3)

    player = [jojo, dio]
    game_world.add_objects(player, 2)
    game_world.add_collision_pair('DIO:JoJo', dio, None)
    game_world.add_collision_pair('DIO:JoJo', None, jojo)

    healthbar = HealthBar()
    game_world.add_object(healthbar, 3)
    p1_gauge = Gauge(jojo, is_right = True)
    p2_gauge = Gauge(dio)
    gauge = [p1_gauge, p2_gauge]
    game_world.add_objects(gauge, 3)
    p1_health = Health(406, dio, is_right=False)
    p2_health = Health(1194, jojo, is_right=True)
    health = [p1_health, p2_health]
    game_world.add_objects(health, 3)
    portraits = Portraits()
    game_world.add_object(portraits, 0)

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    global jojo, dio, jojo_stand_active, dio_stand_active, fight_signal
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            # Fight signal 중에는 KEYUP만 처리
            if fight_signal.active:
                if event.type == SDL_KEYUP:
                    jojo.handle_event(event)
                    dio.handle_event(event)
                continue

            # Stand 활성화 키는 항상 처리 (ENTER for JoJo, SPACE for DIO)
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RETURN:  # JoJo Stand 활성화
                    jojo.handle_event(event)
                if event.key == SDLK_SPACE:  # DIO Stand 활성화
                    dio.handle_event(event)

            # Stand 공격 조작 제한 로직
            if jojo_stand_active and dio_stand_active:
                jojo.handle_event(event)
                dio.handle_event(event)
            elif jojo_stand_active:
                jojo.handle_event(event)
            elif dio_stand_active:
                dio.handle_event(event)
            else:
                jojo.handle_event(event)
                dio.handle_event(event)

def update():
    global fight_signal, signal_shown, jojo_stand_active, dio_stand_active, stand_timer, background, fight_signal_was_active, game_over, bgm

    if not game_over:
        if jojo.hp <= 0 or dio.hp <= 0:
            bgm.pause()
            bgm = music.result_bgm
            bgm.repeat_play()
            game_over = True
            result_mode.handle_events()
            if jojo.hp < dio.hp:
                game_world.remove_object(jojo)
                dio.x = 800
                dio.state_machine.cur_state = dio.IDLE
            else:
                game_world.remove_object(dio)
                jojo.x = 800
                jojo.state_machine.cur_state = jojo.IDLE

        else:
            # Intro 종료 감지 및 키 상태 초기화
            if not signal_shown:
                if jojo.state_machine.cur_state != jojo.INTRO and dio.state_machine.cur_state != dio.INTRO:
                    signal_shown = True
                    fight_signal.start()
                    jojo.reset_key_states()
                    dio.reset_key_states()

            # Fight signal 종료 감지 및 키 상태 초기화
            if fight_signal_was_active and not fight_signal.active:
                jojo.reset_key_states()
                dio.reset_key_states()
            fight_signal_was_active = fight_signal.active

            jojo_in_stand = jojo.state_machine.cur_state == jojo.STAND
            dio_in_stand = dio.state_machine.cur_state == dio.STAND

            if jojo_in_stand and not jojo_stand_active:
                jojo_stand_active = True
                stand_timer = 5.0
                background.use_skill = True

            if dio_in_stand and not dio_stand_active:
                dio_stand_active = True
                stand_timer = 5.0
                background.use_skill = True

            if not jojo_in_stand and jojo_stand_active and stand_timer > 0:
                pass

            if not dio_in_stand and dio_stand_active and stand_timer > 0:
                pass

            if stand_timer > 0:
                stand_timer -= game_framework.frame_time
                if stand_timer <= 0:
                    jojo_stand_active = False
                    dio_stand_active = False
                    background.use_skill = False
                    stand_timer = 0
                    jojo.reset_key_states()
                    dio.reset_key_states()

            game_world.update()
            game_world.handle_collision()
    else:

        result_mode.handle_events()
        # if jojo.hp <= 0 or dio.hp <=0:
        #     game_framework.change_mode(result_mode)


def draw():
    clear_canvas()
    game_world.render()
    if game_over:
        winner = load_image('wintxt.png')
        if jojo.hp > dio.hp:  # 2P 승
            winner.clip_draw(1536 // 2, 0, 1536 // 2, 364, 900, 600)
        elif jojo.hp < dio.hp:  # 1P 승
            winner.clip_draw(0, 0, 1536 // 2, 364, 900, 600)
        else:  # draw
            pass
    update_canvas()

