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

    healthbar = HealthBar()
    game_world.add_object(healthbar, 3)
    p1_health = Health(406)
    p2_health = Health(1194)
    health = [p1_health, p2_health]
    game_world.add_objects(health, 3)

    jojo = JoJo()
    dio = DIO()
    player = [jojo, dio]
    game_world.add_objects(player, 2)

def finish():
    game_world.clear()

def pause():
    pass

def resume():
    pass

def handle_events():
    global jojo
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:
                jojo.move_left()
            elif event.key == SDLK_RIGHT:
                jojo.move_right()

def update():
    game_world.update()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
