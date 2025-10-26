from _pyrepl.commands import clear_screen

from pico2d import *
from UI import *

def reset_world():
    global world

    world = []

    background = Background()
    world.append(background)

    health = []
    p1_health = HealthBar(0)
    p2_health = HealthBar(450)
    health.append(p1_health)
    health.append(p2_health)
    world.append(health)

    gauge = []
    p1_gauge = Gauge(0)
    p2_gauge = Gauge(650)
    gauge.append(p1_gauge)
    gauge.append(p2_gauge)
    world.append(gauge)

def update_world():
    for o in world:
        o.update()

def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()

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