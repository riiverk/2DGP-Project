from pico2d import *
import game_framework
import play_mode

def init():
    pass

def finish():
    pass

def pause():
    pass

def resume():
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_RETURN:
                game_framework.change_mode(play_mode)

def update():
    pass

def draw():
    clear_canvas()
    update_canvas()
