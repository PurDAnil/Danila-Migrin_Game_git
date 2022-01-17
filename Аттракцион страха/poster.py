import pygame as pg


class Poster:
    def __init__(self, app, image, p_width, p_height, x, y, h, z):
        # z - либо х, либо у. Если х, то по х кординате и наоборот.
        self.flag = True
        self.app = app
        im = pg.transform.scale(pg.image.load('posters/' + image + '.jpg'), (p_width, p_height))
        self.size = (p_width, p_height)
        self.image = pg.surfarray.array3d(im)
        self.x = x
        self.y = y
        self.h = h
        self.z = z
        app.posters.append(self)

    def update(self):
        pass

    def draw(self):
        # self.app.screen.blit(self.image, (0, 0))
        pass
