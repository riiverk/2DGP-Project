from pico2d import *
from UI import *
import game_world
import game_framework
from JoJo import JoJo
from DIO import DIO

jojo = None
dio = None

def init():
    global jojo, dio

    background = Background()
    game_world.add_object(background, 0)

    jojo = JoJo()
    dio = DIO()
    player = [jojo, dio]
    game_world.add_objects(player, 2)
    game_world.add_collision_pair('DIO:JoJo', dio, None)
    game_world.add_collision_pair('DIO:JoJo', None, jojo)

    healthbar = HealthBar()
    game_world.add_object(healthbar, 3)
    p1_health = Health(406, dio, is_right=False)  # 왼쪽: DIO
    p2_health = Health(1194, jojo, is_right=True)  # 오른쪽: JoJo
    health = [p1_health, p2_health]
    game_world.add_objects(health, 3)

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
    game_world.update()
    game_world.handle_collision()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
