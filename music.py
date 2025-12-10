from pico2d import*
import random

def load():
    global title_bgm, select_bgm, play_bgm, result_bgm
    global dio_sound1, dio_sound2, dio_sound3
    global jojo_sound1, jojo_sound2
    global dio_theworld, jojo_theworld

    title_bgm = load_music('Sound/giorno.mp3')
    select_bgm = load_wav('Sound/menuselect.mp3')
    play_bgm = load_music('Sound/eyesofheaven.mp3')
    result_bgm = load_music('Sound/tobecontinued.mp3')

    dio_sound1 = load_wav('Sound/dioheavy.wav')
    dio_sound2 = load_wav('Sound/diomedium.wav')
    dio_sound3 = load_wav('Sound/dioweak.wav')

    jojo_sound1 = load_wav('Sound/mudamedium.wav')
    jojo_sound2 = load_wav('Sound/mudaweak.wav')

    dio_theworld = load_wav('Sound/zawarudoshout.wav')
    jojo_theworld = load_wav('Sound/zawarudocall.wav')

    play_bgm.set_volume(255)
    select_bgm.set_volume(150)
    title_bgm.set_volume(150)
    result_bgm.set_volume(150)
    dio_sound1.set_volume(150)
    dio_sound2.set_volume(150)
    dio_sound3.set_volume(150)
    jojo_sound1.set_volume(150)
    jojo_sound2.set_volume(150)
    dio_theworld.set_volume(150)
    jojo_theworld.set_volume(150)

def play_random_jojo_attack_sound():
    sounds = [jojo_sound1, jojo_sound2]
    selected = random.choice(sounds)
    selected.play()

def play_random_dio_attack_sound():
    sounds = [dio_sound1, dio_sound2, dio_sound3]
    selected = random.choice(sounds)
    selected.play()
