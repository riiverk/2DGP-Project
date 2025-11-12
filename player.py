from pico2d import load_image

class JoJo:
    def __init__(self):
        self.x, self.y = 1300, 400
        self.frame = 0
        self.face_dir = 1
        self.image = load_image('JoJo.png')
        self.image_h = 4800

    def draw(self):
        self.image.clip_draw(int(self.frame) * 70 + 2, self.image_h - 145, 70, 120, self.x, self.y, 210, 360)

    def update(self):
        pass

class DIO:
    def draw(self):
        pass
    def update(self):
        pass