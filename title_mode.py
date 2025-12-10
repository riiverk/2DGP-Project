from pico2d import *
import game_framework
import play_mode

import os

print("exists:", os.path.exists("Sound/giorno.ogg"))
print("cwd:", os.getcwd())



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
                game_framework.change_mode(play_mode)

def update():
    global logo_y, gogo_y, bkg
    LOGO_SPEED_PPS = 800
    if logo_y > 500:
        logo_y -= LOGO_SPEED_PPS * game_framework.frame_time
    else:
        bkg = True
    if gogo_y < 900 and bkg:
        gogo_y += 1



def draw():
    clear_canvas()
    background.clip_draw(0, 0, 10, 10, 800, 600, 1600, 1200)
    if (bkg):
        J.clip_draw(3291, 7750 - 7357, 262, 224, 1300, 200, 524, 448)
        # D.clip_draw(2767, 10400 - 9817 - 224, 370, 224, 300, 800, 555, 336)
        # D.clip_draw(1950, 10400 - 6112 - 223, 302, 223, 300, 800, 604, 446)

    logo.draw(800, logo_y)
    if (bkg): gogo.draw(1200, gogo_y)
    update_canvas()
