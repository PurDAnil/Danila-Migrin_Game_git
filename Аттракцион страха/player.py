import pygame as pg
import numpy as np
import math
from voxel_render import VoxelRender


class Player:
    def __init__(self, app):
        self.app = app
        self.pos = np.array([742, 556], dtype=float)
        self.angle = 3.9
        self.height = 300
        self.pitch = -80
        self.angle_vel = 0.04
        self.vel = 5
        self.move = 0
        self.cof = 0.04
        self.camera = 1

    def update_god(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_UP]:
            self.pitch += self.angle_vel * 1000
            if self.pitch > 1200:
                self.pitch = 1200
        if pressed_key[pg.K_DOWN]:
            self.pitch -= self.angle_vel * 1000
            if self.pitch < -1200:
                self.pitch = -1200

        if pressed_key[pg.K_LEFT]:
            self.angle -= self.angle_vel
        if pressed_key[pg.K_RIGHT]:
            self.angle += self.angle_vel

        moving = False
        if pressed_key[pg.K_w]:
            self.pos[0] += self.vel * cos_a
            self.pos[1] += self.vel * sin_a
            moving = True
        if pressed_key[pg.K_s]:
            self.pos[0] -= self.vel * cos_a
            self.pos[1] -= self.vel * sin_a
            moving = True
        if pressed_key[pg.K_a]:
            self.pos[0] += self.vel * sin_a
            self.pos[1] -= self.vel * cos_a
            moving = True
        if pressed_key[pg.K_d]:
            self.pos[0] -= self.vel * sin_a
            self.pos[1] += self.vel * cos_a
            moving = True

        if moving:
            if not -0.5 <= self.move <= 0.5:
                self.cof *= -1
            self.move += self.cof
        else:
            self.move = 0

        if pressed_key[pg.K_SPACE]:
            self.height += 10
            if self.height > 1500:
                self.height = 1500
        if pressed_key[pg.K_z]:
            self.height -= 10
            if self.height < 40:
                self.height = 40

        if pressed_key[pg.K_g]:
            print([self.pitch, self.pos, self.height, self.angle])

        if pressed_key[pg.K_k]:
            self.camera = 0

        if pressed_key[pg.K_l]:
            self.camera = 1

        if pressed_key[pg.K_1]:
            self.app.voxel_render.change('openm')

        if pressed_key[pg.K_2]:
            self.app.voxel_render.change('left')

        if pressed_key[pg.K_3]:
            self.app.voxel_render.change('right')

        if pressed_key[pg.K_4]:
            self.app.voxel_render.change('block')

    def update(self):
        if self.camera == 0:
            mouse = pg.mouse.get_pos()[0]
            zona = self.app.width / 3
            if self.angle >= 4.02 and mouse <= zona:
                self.angle -= self.angle_vel * 3
            if self.angle <= 5.18 and mouse >= zona * 2:
                self.angle += self.angle_vel * 3
