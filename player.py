from pico2d import load_image

class JoJo:
    def __init__(self):
        self.x, self.y = 50, 70
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('JoJo.png')

    def draw(self):
        self.image.clip_draw(int(self.frame) * 100, 100, 100, 100, self.x, self.y)

    def update(self):
        pass

class DIO:
    pass