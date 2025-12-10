from pico2d import *
import game_framework
import title_mode
import play_mode
import music

open_canvas(1600, 1000)
music.load()
game_framework.run(title_mode)
close_canvas()

