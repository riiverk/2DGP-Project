from pico2d import load_image

class Health :
    def __init__(self, x):
        self.image = load_image('health.png')
        self.x = x
        self.y = 1200 - 142 - 15 - 1
        self.image_bkg = load_image('healthbar.png')

    def draw(self):
        self.image_bkg.draw(800, 1000, 1400, 202)
        self.image.draw(self.x, self.y, 550, 30)

    def update(self):
        pass

class Background:
    def __init__(self):
        self.image = load_image('match_background.png')

    def draw(self):
        self.image.draw(800,600)

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