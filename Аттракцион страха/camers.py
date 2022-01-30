import random
from blitter import Blitter


class Cam:
    # self.pitch, self.pos, self.height
    # -80.0 [723.69674572 548.38077551] 270
    # -200.0 [663.26748272 536.00193018] 330 5.233333333333362
    def __init__(self, app):
        self.app = app
        self.cam = 1
        self.cam_cof = 1
        self.cam_angle = 0
        self.cam_im = Blitter(self.app, 'cam.jpg', [0, 0], [800, 450])
        self.cam_text = Blitter(self.app, 'CAM #1', [80, 60], [80, 80], text_size=40)
        self.cam_map = Blitter(self.app, 'map.png', [85, 200], [150, 200])

    def draw(self):
        self.cam_im.hide()
        self.cam_text.hide()
        self.cam_map.hide()
        if self.app.player.camera:
            self.cam_map.show()
            self.cam_im.show()
            self.cam_text.show()
            self.app.player.angle += self.app.player.angle_vel * self.cam_cof / 15
            self.cam_angle += self.cam_cof / 4
            if 0 > self.cam_angle or self.cam_angle > 20:
                self.cam_cof *= -1

            w = self.app.height / 450 * 800
            for i in range(2500):
                rand = random.random() * 100
                self.app.screen.fill((rand, rand, rand),
                                     (random.random() * w + (self.app.width - w) // 2,
                                      random.random() * self.app.height, 2, 1))
