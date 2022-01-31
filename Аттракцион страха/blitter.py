import pygame as pg
import os

pg.font.init()


class Blitter:
    def __init__(self, app, item, pos: list, size: list, show=True, text_size=10, color='white', click=0, ed='-', cp=0):
        self.click = click
        self.arg = ed
        self.show_hide = show
        self.app = app
        self.pos = pos
        self.size = size
        self.app.blitter.append(self)
        if type(cp) is list:
            cp.append(self)
        if not item in os.listdir('tech'):
            self.font = pg.font.Font(None, text_size)
            self.item = self.font.render(item, True, color)
        else:
            self.item = pg.transform.scale(pg.image.load('tech/' + item), size).convert_alpha()
        if type(click) is not int:
            h = self.app.height
            w = h / 450 * 800
            self.button = self.item.get_rect(topleft=self.pos)
            for i, n in enumerate(self.button):
                if i % 2 == 0:
                    self.button[i] = round(n * (w / 800) + (self.app.width - w) / 2)
                else:
                    self.button[i] = round(n * (h / 450))
                if i // 2:
                    self.button[i] += self.button[i - 2]

    def update(self):
        if type(self.click) is not int and self.show_hide:
            if pg.mouse.get_pressed()[0]:
                bt = self.button
                mouse = pg.mouse.get_pos()
                if mouse[0] in range(bt[0], bt[2]) and mouse[1] in range(bt[1], bt[3]):
                    if self.arg != '-':
                        self.click(self.arg)
                    else:
                        self.click()

    def draw(self):
        if self.show_hide:
            surf = pg.surface.Surface([800, 450], pg.SRCALPHA, 32)
            surf.blit(self.item, self.pos)
            h = self.app.height
            w = h / 450 * 800
            surf = pg.transform.scale(surf, [w, h]).convert_alpha()
            self.app.screen.blit(surf, ((self.app.width - w) / 2, 0))

    def change(self, new_item, color=(255, 255, 255)):
        if not new_item in os.listdir('tech'):
            self.item = self.font.render(new_item, True, color)
        else:
            self.item = pg.transform.scale(pg.image.load('tech/' + new_item), self.size).convert_alpha()

    def __del__(self):
        del self.app.blitter[self.app.blitter.index(self)]

    def show(self):
        self.show_hide = True

    def hide(self):
        self.show_hide = False
