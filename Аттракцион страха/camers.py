import pygame as pg
import random


class Cam:
    def __init__(self, app):
        self.app = app
        self.cam_cof = 1
        self.cam_angle = 0

    def draw(self):
        if self.app.player.camera:
            self.app.player.angle += self.app.player.angle_vel * self.cam_cof / 15
            self.cam_angle += self.cam_cof / 4
            if 0 > self.cam_angle or self.cam_angle > 20:
                self.cam_cof *= -1

            w = self.app.height // 450 * 1200
            for i in range(10000):
                self.app.screen.fill(pg.Color(random.choice(['darkgray', 'black'])),
                                     (random.random() * w + (self.app.width - w) // 2,
                                      random.random() * self.app.height, 3, 1))