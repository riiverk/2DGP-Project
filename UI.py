from pico2d import load_image

class HealthBar:
    def __init__(self, x):
        self.image = load_image('health.png')
        self.x = x
        self.y = 750

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass

class Background:
    def __init__(self):
        self.image = load_image('match_background.png')

    def draw(self):
        self.image.draw(0,0)

    def update(self):
        pass

class Gauge:
    def __init__(self, x):
        self.image = load_image('gauge.png')
        self.x = x
        self.y = 10

    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass