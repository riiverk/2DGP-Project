from pico2d import load_image

class DIO:
    def __init__(self):
        self.x, self.y = 300, 400
        self.frame = 1
        self.face_dir = 0
        self.image = load_image('DIO.png')
        self.image_h = 9061

    def draw(self):
        self.image.clip_draw(int(self.frame) * 70 + 15, self.image_h - 150, 70, 130, self.x, self.y, 210, 390)

    def update(self):
        pass