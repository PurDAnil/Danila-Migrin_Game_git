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
        self.buttons = []
        self.information = []
        self.running = True
        items = 0
        try:
            self.data = json.load(open('data.json'))
        except FileNotFoundError:
            items = {}
            items['night'] = 1
            json.dump(items, open('data.json', 'w'))
            self.data = json.load(open('data.json'))
        self.im = Blitter(self, 'freddy.png', [0, 0], [400, 450], cp=self.buttons)
        Blitter(self, 'Новая игра', [500, 100], [0, 0], text_size=50, cp=self.buttons, click=self.new_game)
        Blitter(self, 'Продолжить', [500, 170], [0, 0], text_size=50, cp=self.buttons, click=self.start_game)
        night = 'Ночь ' + str(self.data['night'])
        Blitter(self, night, [640, 200], [0, 0], text_size=25, cp=self.buttons, color=(155, 155, 155))
        Blitter(self, 'Инструкция', [500, 240], [0, 0], text_size=50, cp=self.buttons, click=self.info)
        Blitter(self, 'Выход', [700, 400], [0, 0], text_size=36, cp=self.buttons, show=True, click=self.exit_game)

        Blitter(self, 'Закрывайте двери для защиты и открывайте их в безопасное время, нажимая на эти кнопки',
                [50, 62], [0, 0], text_size=20, cp=self.information, show=False)
        Blitter(self, '->', [680, 50], [0, 0], text_size=50, cp=self.information, show=False)
        Blitter(self, 'right_off.png', [700, -30], [100, 200], cp=self.information, show=False)
        Blitter(self, 'Просматривайте камеры чтобы узнать местоположения аниматроников',
                [45, 350], [0, 0], text_size=30, cp=self.information, show=False)
        Blitter(self, 'ˇ', [370, 370], [0, 0], text_size=100, cp=self.information, show=False)
        Blitter(self, 'button.png', [230, 400], [300, 30], cp=self.information, show=False)
        Blitter(self, 'down.png', [330, 400], [100, 30], cp=self.information, show=False)
        Blitter(self, 'Назад', [50, 400], [0, 0], text_size=36, cp=self.information, show=False, click=self.hide_info)
        text_x = 160
        Blitter(self, 'Всё в этой пиццерии пытается вас убить, так что стоит ',
                [10, text_x], [0, 0], text_size=40, cp=self.information, show=False)
        Blitter(self, 'помнить, что это не просто работа, а игра на выживание.',
                [10, text_x + 25], [0, 0], text_size=40, cp=self.information, show=False)
        Blitter(self, 'Если аниматроник доберётся до вас, закончится энергия',
                [10, text_x + 50], [0, 0], text_size=40, cp=self.information, show=False)
        Blitter(self, 'или вдруг музыка шкатулки оборвётся, то вам конец.',
                [10, text_x + 75], [0, 0], text_size=40, cp=self.information, show=False)
        if type(items) is dict:
            self.info()

    def update(self):
        [i.update() for i in self.buttons]
        [i.update() for i in self.information]

    def draw(self):
        w = self.height / 450 * 800
        for i in range(20):
            rand = random() * 100
            self.screen.fill((rand, rand, rand),
                             ((self.width - w) // 2,
                              random() * self.height, w, random() * 10))
        [i.draw() for i in self.buttons]
        [i.draw() for i in self.information]

        pg.display.flip()

    def run(self):
        pg.display.set_caption('immortal menu')
        while self.running:
            self.screen.fill((0, 0, 0))
            self.update()
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.running = False
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

    def info(self):
        [i.hide() for i in self.buttons]
        [i.show() for i in self.information]

    def hide_info(self):
        [i.hide() for i in self.information]
        [i.show() for i in self.buttons]

    def exit_game(self):
        self.running = False


if __name__ == '__main__':
    app = Menu()
    app.run()
