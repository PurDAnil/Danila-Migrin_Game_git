import os
import pygame as pg
from random import randrange, choice
from blitter import Blitter


class Animatronic:
    def __init__(self, app, name):
        self.time = 0
        self.app = app
        self.night = app.night
        self.name = name
        self.screamers = []
        special_cof = {'freddy': self.night // 3 * self.night * 5, 'chika': self.night * 10,
                       'bonni': self.night / 4 * self.night * 10, 'foxy': 20 - self.night // 2 * self.night}
        # 'marionette': self.night * 0.8, 'echo': self.night * self.night / 4
        self.cof = special_cof[name]
        start_poss = {'freddy': 1, 'chika': 1,
                      'bonni': 6, 'foxy': 2,
                      'marionette': 5, 'echo': 0}
        self.pos = start_poss[name]
        self.posible_pos = {}
        self.cords = {}
        print(self.cof)
        name = 'freddy'
        for image in os.listdir('animatronics/' + name):
            if not 'screamer' in image:
                self.posible_pos[image.split('.')[0]] = pg.image.load('animatronics/' + name + '/' + image)
                self.cords[image.split('.')[0]] = image.split('.')[1]
            else:
                self.screamers.append(pg.image.load('animatronics/' + name + '/' + image))

    def update(self):
        if self.app.time > 40 - self.night * 10 and self.time <= int(self.app.time) - 1:
            self.time = int(self.app.time)
            if randrange(100) in range(round(self.cof)):
                if self.name is 'bonni':
                    if self.pos == 1:
                        self.pos = 4
                    elif self.pos == 4:
                        self.pos = choice([1, 5, 5, 6, 6])
                    elif self.pos == 5:
                        self.pos = 4
                    elif self.pos == 6:
                        self.pos = choice([0, 0, 0, 0, 4])
                        if self.pos == 0:
                            if not self.app.doors[0]:
                                self.pos = 0
                            else:
                                self.pos = choice([4, 4, 6])
                self.time += 13 - self.night

    def draw(self):
        surf = pg.surface.Surface([800, 450], pg.SRCALPHA, 32)
        if self.pos == 0:
            self.screamer()
        else:
            if self.app.cam.cam == self.pos and self.app.player.camera:
                pos = (int(self.cords[str(self.pos)]) - self.app.cam.real_angle * 1750, 0)
                surf.blit(self.posible_pos[str(self.pos)], pos)
            elif self.pos == 6 and not self.app.player.camera and not self.app.doors[0]:
                pos = (int(self.cords[str(self.pos)]) - (self.app.player.angle - 4.10) * 1750, 0)
                surf.blit(self.posible_pos[str(self.pos)], pos)
            elif self.pos == 7 and not self.app.player.camera and not self.app.doors[1]:
                pos = (int(self.cords[str(self.pos)]) - (self.app.player.angle - 5.38) * 1750, 0)
                surf.blit(self.posible_pos[str(self.pos)], pos)
            h = self.app.height
            w = h / 450 * 800
            surf = pg.transform.scale(surf, [w, h]).convert_alpha()
            self.app.screen.blit(surf, ((self.app.width - w) / 2, 0))


    def screamer(self):
        pg.quit()
