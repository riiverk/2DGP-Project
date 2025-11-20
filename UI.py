from pico2d import load_image

class Health :
    def __init__(self, x, character, is_right=False):
        self.image = load_image('health.png')
        self.base_x = x
        self.y = 1200 - 142 - 15 - 1 + 50
        self.character = character
        self.is_right = is_right  # 오른쪽 체력바인지
        self.max_width = 550
        self.height = 30

    def draw(self):
        ratio = self.character.hp / 100
        width = int(self.max_width * ratio)

        if self.is_right:
            # 오른쪽 체력바: 바깥쪽(오른쪽)부터 줄어듦
            x = self.base_x - (self.max_width - width) // 2
        else:
            # 왼쪽 체력바: 바깥쪽(왼쪽)부터 줄어듦
            x = self.base_x + (self.max_width - width) // 2

        self.image.draw(x, self.y, width, self.height)

    def update(self):
        pass

class HealthBar:
    def __init__(self):
        self.image = load_image('healthbar.png')

    def draw(self):
        self.image.draw(800, 1050, 1400, 202)

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