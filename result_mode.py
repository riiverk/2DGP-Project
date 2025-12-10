from pico2d import *
import game_framework
import title_mode
import play_mode

def init():
    global background, logo, logo_y, bkg, gogo, gogo_y, J, D
    J = load_image('JoJo_fix.png')
    D = load_image('DIO_fix.png')
    background = load_image('white.png')
    logo = load_image('logo.png')
    gogo = load_image('gogo.png')
    logo_y = 1000
    bkg = False
    gogo_y = 400

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
                game_framework.change_mode(title_mode)

def update():
    handle_events()

def draw():
    clear_canvas()
    play_mode.draw()
    winner = load_image('wintxt.png')
    if play_mode.jojo.hp > play_mode.dio.hp:    # 2P 승
        winner.clip_draw(1536//2, 0, 1536//2, 364, 800, 600)
    elif  play_mode.jojo.hp < play_mode.dio.hp:   # 1P 승
        pass
    else:    # draw
        pass

    update_canvas()
