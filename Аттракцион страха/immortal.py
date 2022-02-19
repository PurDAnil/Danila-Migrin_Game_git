import pygame as pg
from player import Player
from voxel_render import VoxelRender
from poster import Poster
from camers import Cam
from battery import Battery
from animatronic import Animatronic


class App:
    def __init__(self, night):
        self.night = night
        self.time = 30
        self.test = 0
        if self.test:
            h = 250
            w = 800
        else:
            pg.display.set_mode()
            h = pg.display.Info().current_h
            w = pg.display.Info().current_w
        pg.display.set_icon(pg.image.load('tech/icon.jpg'))
        self.anim = Animatronic(self, 'bonni')
        self.doors = [0, 0]
        self.blitter = []
        self.posters = [[], [], [], []]
        self.res = self.width, self.height = (w, h)
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()
        self.player = Player(self)
        self.voxel_render = VoxelRender(self)
        self.cam = Cam(self)
        self.battery = Battery(self)
        Poster(self, 30, 25, 'x', 'matrix')
        Poster(self, 20, 900, 'y', 'fnaf_poster')

    def update(self):
        self.battery.update()
        self.player.update()
        self.voxel_render.update()
        self.cam.update()
        self.anim.update()

    def draw(self):
        self.voxel_render.draw()
        self.anim.draw()
        self.cam.draw()
        pg.display.flip()

    def run(self):
        pg.display.set_caption('immortal')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.clock.tick(20)
            self.time += self.clock.tick(20) * 4 / 1000
            pg.display.set_caption(str(self.clock.get_fps()))
            self.update()
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
        pg.quit()


if __name__ == '__main__':
    app = App(1)
    app.run()
