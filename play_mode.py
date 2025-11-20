from pico2d import *
from UI import *
import game_world
import game_framework
from JoJo import JoJo
from DIO import DIO

jojo = None
dio = None
dio_hit = False  # DIO의 Jap이 이미 맞췄는지 체크

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def init():
    global jojo, dio

    background = Background()
    game_world.add_object(background, 0)

    jojo = JoJo()
    dio = DIO()
    player = [jojo, dio]
    game_world.add_objects(player, 2)

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
    global dio_hit
    game_world.update()

    # DIO의 Jap이 JoJo에게 맞으면 체력 감소
    if dio.state_machine.cur_state == dio.JAP:
        if not dio_hit and collide(dio, jojo):
            jojo.hp -= 10
            dio_hit = True
            print(f'JoJo HP: {jojo.hp}')
    else:
        dio_hit = False

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
