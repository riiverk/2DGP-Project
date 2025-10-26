from pico2d import load_image

class HealthBar:
    def __init__(self):
        self.image = load_image('health.png')

class Background:
    def __init__(self):
        self.image = load_image('match_background.png')

class Gauge:
    def __init__(self):
        self.image = load_image('gauge.png')