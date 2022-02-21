from blitter import Blitter
import pygame as pg
ener_cost = {
    'openm': 0,
    'right': 1,
    'left': 1,
    'block': 2
}


class Battery:
    def __init__(self, app):
        self.tr = True
        pg.mixer.music.load("sounds/office.mp3")
        pg.mixer.music.play(-1)
        self.app = app
        self.charge = 100
        self.batt = Blitter(self.app, '', [660, 65], [150, 200], cp=self.app.cam.all_blit, text_size=20, color='green')

    def update(self):
        if self.charge > 0:
            e_c = self.app.voxel_render.door
            self.charge -= self.app.clock.tick(20) / (1000 - self.app.player.camera * 200 - ener_cost[e_c] * 250)
            self.batt.change(str(round(self.charge)) + '%', color='green')
        elif self.app.player.camera:
            self.app.cam.change_cam(0)
        else:
            if self.tr:
                self.tr = False
                pg.mixer.music.stop()
                pg.mixer.music.load("sounds/powerdown.mp3")
                pg.mixer.music.play(0)
            self.app.voxel_render.pover_off()
            self.app.voxel_render.change('openm')
            [i.hide() for i in self.app.cam.plansh]
            [i.hide() for i in self.app.cam.door_but]
