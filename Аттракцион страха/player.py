import pygame as pg
import numpy as np
import math


class Player:
    def __init__(self):
        self.pos = np.array([0, 0], dtype=float)
        self.angle = math.pi / 4
        self.height = 400
        self.pitch = 40
        self.angle_vel = 0.04
        self.vel = 5
        self.move = 0
        self.cof = 0.04

    def update(self):
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
