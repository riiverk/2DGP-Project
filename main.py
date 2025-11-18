from pico2d import *
from UI import *
import game_world
from JoJo import JoJo
from DIO import DIO

def reset_world():
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


def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                jojo.move_left()
            elif event.key == SDLK_RIGHT:
                jojo.move_right()

running = True

open_canvas(1600, 1200)
reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()