from pico2d import *
from UI import *
import game_world
import game_framework
from JoJo import JoJo
from DIO import DIO

jojo = None
dio = None
intro_played = False
fight_signal = None
signal_shown = False

def init():
    global jojo, dio, intro_played, fight_signal, signal_shown

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
    global jojo, dio
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            jojo.handle_event(event)
            dio.handle_event(event)

def update():
    global fight_signal, signal_shown
    game_world.update()
    game_world.handle_collision()

    if not signal_shown:
        if jojo.state_machine.cur_state != jojo.INTRO and dio.state_machine.cur_state != dio.INTRO:
            signal_shown = True
            fight_signal.start()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

