import pygame as pg
from player import Player
from voxel_render import VoxelRender
from poster import Poster
from camers import Cam
from battery import Battery


class App:
    def __init__(self):
        self.test = 0
        if self.test:
            h = 450
            w = 800
        else:
            pg.display.set_mode()
            h = pg.display.Info().current_h
            w = pg.display.Info().current_w
        pg.display.set_icon(pg.image.load('tech/icon.jpg'))
        self.blitter = []
        self.posters = [[], [], [], []]
        self.res = self.width, self.height = (w, h)
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()
        self.player = Player(self)
        self.voxel_render = VoxelRender(self)
        self.voxel_render.changes('fnaf', (0, 0, 0), (255, 0, 0))
        self.cam = Cam(self)
        self.battery = Battery(self)
        Poster(self, 30, 25, 'x', 'matrix')
        Poster(self, 20, 900, 'y', 'fnaf_poster')

    def update(self):
        self.battery.update()
        self.player.update_god()
        self.voxel_render.update()
        self.cam.update()
        [i.update() for i in self.blitter]

    def draw(self):
        self.voxel_render.draw()
        self.cam.draw()
        [i.draw() for i in self.blitter]
        pg.display.flip()

    def run(self):
        pg.display.set_caption('immortal')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.clock.tick(20)
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
    app = App()
    app.run()
