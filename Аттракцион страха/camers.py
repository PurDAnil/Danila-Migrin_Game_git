import random
from blitter import Blitter

cameras = [[240.0, [594.04, 1372.38], 50, 4.66], [-80, [723.7, 548.38], 270, 3.9], [-200, [663.27, 536.0], 330, 5.2],
           [40, [710.82, 572.46], 230, 13.54], [0, [320.06, 563.29], 220, 14.51], [-200, [669.94, 560.96], 270, 21.21]]


class Cam:
    # self.pitch, self.pos, self.height, self.angle
    # -80.0 [723.69674572 548.38077551] 270
    # -200.0 [663.26748272 536.00193018] 330 5.233333333333362
    def __init__(self, app):
        self.zamedl = 0
        self.app = app
        self.cam = 1
        self.cam_cof = 1
        self.real_angle = 0
        self.cam_angle = 0
        self.all_blit = []
        self.cam_im = Blitter(self.app, 'cam.jpg', [0, 0], [800, 450], cp=self.all_blit)
        self.cam_text = Blitter(self.app, 'CAM #1', [80, 60], [80, 80], text_size=40, cp=self.all_blit)
        self.cam_map = Blitter(self.app, 'map.png', [85, 200], [150, 200], cp=self.all_blit)
        self.plansh = []
        Blitter(self.app, 'button.png', [230, 400], [300, 30], cp=self.plansh, click=self.change_cam, ed=0)
        Blitter(self.app, 'down.png', [330, 400], [100, 30], cp=self.plansh)

        Blitter(self.app, 'button.png', [145, 265], [38, 10], cp=self.all_blit, click=self.change_cam, ed=1)
        Blitter(self.app, 'Cam #1', [145, 265], [150, 200], cp=self.all_blit, text_size=15)
        Blitter(self.app, 'button.png', [185, 265], [38, 10], cp=self.all_blit, click=self.change_cam, ed=2)
        Blitter(self.app, 'Cam #2', [185, 265], [150, 200], cp=self.all_blit, text_size=15)
        Blitter(self.app, 'button.png', [185, 281], [38, 10], cp=self.all_blit, click=self.change_cam, ed=3)
        Blitter(self.app, 'Cam #3', [185, 281], [150, 200], cp=self.all_blit, text_size=15)
        Blitter(self.app, 'button.png', [93, 281], [38, 10], cp=self.all_blit, click=self.change_cam, ed=4)
        Blitter(self.app, 'Cam #4', [93, 281], [150, 200], cp=self.all_blit, text_size=15)
        Blitter(self.app, 'button.png', [140, 281], [38, 10], cp=self.all_blit, click=self.change_cam, ed=5)
        Blitter(self.app, 'Cam #5', [140, 281], [150, 200], cp=self.all_blit, text_size=15)
        self.change_cam(1)

    def change_cam(self, n):
        self.app.player.pitch, self.app.player.pos, self.app.player.height, self.app.player.angle = cameras[n]
        if n == 0:
            self.zamedl = 0
            [i.hide() for i in self.plansh]
            if self.app.player.camera:
                self.app.player.camera = 0
            else:
                self.change_cam(self.cam)
        else:
            self.app.player.camera = 1
            self.cam = n
            self.app.player.angle += self.real_angle
            self.cam_text.change('Cam #' + str(n))

    def update(self):
        self.zamedl += 1
        if self.zamedl == 3:
            [i.show() for i in self.plansh]

    def draw(self):
        [i.hide() for i in self.all_blit]
        if self.app.player.camera:
            [i.show() for i in self.all_blit]
            self.app.player.angle += self.app.player.angle_vel * self.cam_cof / 15
            self.real_angle += self.app.player.angle_vel * self.cam_cof / 15
            self.cam_angle += self.cam_cof / 4
            if 0 > self.cam_angle or self.cam_angle > 20:
                self.cam_cof *= -1

            w = self.app.height / 450 * 800
            for i in range(2500):
                rand = random.random() * 100
                self.app.screen.fill((rand, rand, rand),
                                     (random.random() * w + (self.app.width - w) // 2,
                                      random.random() * self.app.height, 3, 2))
