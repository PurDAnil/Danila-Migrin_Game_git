import os
import json
import pygame as pg
from random import randrange, choice, random


class Animatronic:
    def __init__(self, app, name):
        self.gluc = False
        self.tr = 0
        self.tr_im = 0
        self.time = 0
        if name == 'echo':
            self.time += 40
        self.app = app
        self.night = app.night
        self.name = name
        self.screamers = []
        special_cof = {'freddy': self.night // 3 * self.night * 5, 'chika': self.night * 10,
                       'bonni': self.night / 4 * self.night * 10,
                       'foxy': 20 - self.night // 2 * self.night + self.night // 3 * 4,
                       'echo': self.night * self.night, 'over': 0}
        # 'marionette': self.night * 0.8
        self.cof = special_cof[name]
        if name == 'foxy':
            self.time += self.cof
        start_poss = {'freddy': 1, 'chika': 1,
                      'bonni': 1, 'foxy': 1,
                      'marionette': 5, 'echo': 8, 'over': 0}
        self.pos = start_poss[name]
        self.posible_pos = {}
        self.cords = {}
        for im in os.listdir('animatronics/' + name):
            if not 'screamer' in im:
                self.posible_pos[im.split('.')[0]] = pg.image.load('animatronics/' + name + '/' + im)
                self.cords[im.split('.')[0]] = im.split('.')[1]
            else:
                self.screamers.append(pg.transform.scale(pg.image.load('animatronics/' + name + '/' + im), (800, 450)))

    def update(self):
        if self.name is 'foxy' and self.app.cam.cam == 2 and self.pos != 4 and self.app.player.camera:
            self.time = int(self.app.time) + self.cof
        if self.name is 'freddy' and self.pos == self.app.cam.cam:
            self.time = int(self.app.time) + 20 - self.night
        if self.app.time > 40 - self.night * 10 and self.time <= int(self.app.time) - 1:
            self.time = int(self.app.time)
            if randrange(100) in range(round(self.cof)) or self.name == 'foxy':
                if self.pos == self.app.cam.cam and self.app.player.camera and self.name != 'foxy':
                    self.gluc = True

                if self.name is 'foxy' and self.tr == 0 and self.night >= 2:
                    if self.pos < 4:
                        self.app.foxy_song.play()
                        self.pos += 1
                        if self.pos == 4:
                            self.time = int(self.app.time) + 6
                        else:
                            self.time = int(self.app.time) + self.cof
                    elif not self.app.doors[1]:
                        self.pos = 0
                    else:
                        if randrange(10) > 6:
                            self.app.pound.play()
                        if self.app.cam.cam == 2:
                            self.gluc = True
                        self.pos = 1
                        self.app.battery.charge -= randrange(5, 15)

                if self.name is 'chika':
                    if self.pos == 1:
                        self.pos = 2
                    elif self.pos == 2:
                        self.pos = choice([1, 1, 3, 3, 3])
                    elif self.pos == 3:
                        self.pos = choice([2, 2, 7, 7, 7])
                    elif self.pos == 7:
                        self.pos = choice([0, 0, 0, 3, 3])
                        if self.pos == 0:
                            if not self.app.doors[1]:
                                self.pos = 0
                            else:
                                self.pos = choice([3, 3, 7])
                    self.time += 13 - self.night

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

                if self.name is 'freddy':
                    if self.pos == 1:
                        self.pos = 2
                    elif self.pos == 2:
                        self.pos = 3
                    elif self.pos == 3:
                        self.pos = 7
                    elif self.pos == 7:
                        self.pos = choice([0, 7])
                        if self.pos == 0:
                            if not self.app.doors[1]:
                                self.pos = 0
                    self.time += 20 - self.night

                if self.name == 'echo':
                    self.pos = 0
                    self.time += self.cof * randrange(1, 4)

                if self.pos == self.app.cam.cam and self.app.player.camera:
                    self.gluc = True
            elif self.name == 'echo':
                self.time += 20

    def draw(self):
        surf = pg.surface.Surface([800, 450], pg.SRCALPHA, 32)
        if self.pos == 0:
            self.screamer()
        else:
            if ((self.app.cam.cam == self.pos and self.name != 'foxy')
                    or (self.app.cam.cam == 2 and self.name == 'foxy')) and self.app.player.camera:
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
            if self.gluc:
                for i in range(60):
                    surf.fill((250, 250, 250),
                              ((self.app.width - w) // 2,
                               random() * self.app.height, w, random() * 10))
                self.gluc = False
            surf = pg.transform.scale(surf, [w, h]).convert_alpha()
            self.app.screen.blit(surf, ((self.app.width - w) / 2, 0))

    def screamer(self):
        if self.tr == 0:
            if self.name != 'echo' and self.name != 'over':
                self.app.battery.charge = 0
                self.app.scream.play()
            else:
                self.app.echo_scream.play()
        surf = pg.surface.Surface([800, 450], pg.SRCALPHA, 32)
        try:
            surf.blit(self.screamers[self.tr_im], (0, 0))
        except IndexError:
            self.tr_im = 0
            surf.blit(self.screamers[self.tr_im], (0, 0))
        h = self.app.height
        w = h / 450 * 800
        surf = pg.transform.scale(surf, [w, h]).convert_alpha()
        self.app.screen.blit(surf, ((self.app.width - w) / 2, 0))
        self.tr += 1
        self.tr_im += 1
        if self.tr == 10 and self.name != 'echo':
            if self.name == 'over' and self.night != 7:
                items = {}
                items['night'] = self.night + 1
                json.dump(items, open('data.json', 'w'))
                self.app.menu.data = json.load(open('data.json'))
            self.app.menu.run()
        elif self.name == 'echo' and self.tr == 10:
            self.pos = 8
            self.tr = 0
