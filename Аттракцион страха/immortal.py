import pygame as pg
from player import Player
from voxel_render import VoxelRender
from poster import Poster
from camers import Cam
from battery import Battery
from animatronic import Animatronic


class App:
    def __init__(self, night, menu):
        pg.mixer.pre_init(frequency=44100, size=-16, channels=8, buffer=512, devicename=None)
        pg.mixer.Sound("sounds/eerie-ambience-largesca.wav").play(-1)
        self.scream = pg.mixer.Sound("sounds/screamer.wav")
        self.foxy_song = pg.mixer.Sound("sounds/piratesong.wav")
        self.echo_scream = pg.mixer.Sound("sounds/computer-digital.wav")
        self.pound = pg.mixer.Sound("sounds/pound-2.wav")
        self.blip = pg.mixer.Sound("sounds/blip3.wav")
        self.door_sound = pg.mixer.Sound("sounds/door.wav")
        self.menu = menu
        self.night = night
        self.time = 0
        self.test = 0
        if self.test:
            h = 250
            w = 800
        else:
            pg.display.set_mode()
            h = pg.display.Info().current_h
            w = pg.display.Info().current_w
        pg.display.set_icon(pg.image.load('tech/icon.jpg'))
        self.anim = [Animatronic(self, 'foxy'), Animatronic(self, 'bonni'), Animatronic(self, 'chika'),
                     Animatronic(self, 'freddy'), Animatronic(self, 'echo')]
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
        [i.update() for i in self.anim]

    def draw(self):
        self.voxel_render.draw()
        [i.draw() for i in self.anim]
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
    app = App(1, None)
    app.run()
