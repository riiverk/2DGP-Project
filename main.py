from pico2d import *
import game_framework
import title_mode
import play_mode

open_canvas(1600, 1000)
game_framework.run(title_mode)
bgm = load_music('Sound/giorno.mp3')
bgm.set_volume(255)
bgm.repeat_play()
close_canvas()

