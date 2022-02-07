import pygame as pg
from blitter import Blitter
from random import random
import json
from immortal import App


class Menu:
    def __init__(self):
        pg.display.set_mode()
        h = pg.display.Info().current_h
        w = pg.display.Info().current_w
        pg.display.set_icon(pg.image.load('tech/icon.jpg'))
        self.res = self.width, self.height = (w, h)
        self.screen = pg.display.set_mode(self.res)
        self.im = Blitter(self, 'freddy.png', [0, 0], [400, 450])
        self.buttons = []
        try:
            self.data = json.load(open('data.json'))
        except FileNotFoundError:
            items = {}
            items['night'] = 1
            json.dump(items, open('data.json', 'w'))
            self.data = json.load(open('data.json'))
        Blitter(self, 'Новая игра', [500, 100], [0, 0], text_size=50, cp=self.buttons, click=self.new_game)
        Blitter(self, 'Продолжить', [500, 170], [0, 0], text_size=50, cp=self.buttons, click=self.start_game)
        night = 'Ночь ' + str(self.data['night'])
        Blitter(self, night, [640, 200], [0, 0], text_size=25, cp=self.buttons, color=(155, 155, 155))
        Blitter(self, 'Инструкция', [500, 240], [0, 0], text_size=50, cp=self.buttons)

    def update(self):
        [i.update() for i in self.buttons]

    def draw(self):
        self.im.draw()
        w = self.height / 450 * 800
        for i in range(20):
            rand = random() * 100
            self.screen.fill((rand, rand, rand),
                             ((self.width - w) // 2,
                              random() * self.height, w, random() * 10))
        [i.draw() for i in self.buttons]

        pg.display.flip()

    def run(self):
        pg.display.set_caption('immortal menu')
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.update()
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
        pg.quit()

    def start_game(self):
        self.screen.fill((0, 0, 0))
        night = 'Ночь ' + str(self.data['night'])
        Blitter(self, night, [240, 150], [0, 0], text_size=150).draw()
        pg.display.flip()
        App(self.data['night']).run()

    def new_game(self):
        self.data['night'] = 1
        json.dump(self.data, open('data.json', 'w'))
        self.start_game()


if __name__ == '__main__':
    app = Menu()
    app.run()
