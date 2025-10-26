from pico2d import *
from UI import *

def reset_world():
    pass

def update_world():
    pass

def render_world():
    pass

def handle_events():
    pass

running = True

open_canvas()
reset_world()
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()