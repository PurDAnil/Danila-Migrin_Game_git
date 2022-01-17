import pygame as pg
from player import Player
from voxel_render import VoxelRender
from poster import Poster


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
        self.res = self.width, self.height = (w, h)
        self.screen = pg.display.set_mode(self.res)
        self.clock = pg.time.Clock()
        self.player = Player()
        self.voxel_render = VoxelRender(self)
        self.voxel_render.changes('fnaf', (0, 0, 0), (255, 0, 0))
        self.posters = []
        # self.poster = Poster(self, 'matrix', 200, 200, 550, 40, 200, 'x')

    def update(self):
        self.player.update()
        self.voxel_render.update()
        # self.poster.update()

    def draw(self):
        self.voxel_render.draw()
        # self.poster.draw()
        pg.display.flip()

    def run(self):
        pg.display.set_caption('immortal')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.clock.tick(60)
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
