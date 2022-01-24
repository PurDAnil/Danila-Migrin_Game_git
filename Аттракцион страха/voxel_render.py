import pygame as pg
from numba import njit
import numpy as np
import math
import os

height_map_img = pg.image.load('maps/test/height_map.jpg')
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load('maps/test/color_map.jpg')
color_map = pg.surfarray.array3d(color_map_img)

map_height = len(height_map[0])
map_width = len(height_map)
filling_color = (0, 0, 0)
bright = 100
roof = False

for image in os.listdir('posters'):
    im = pg.transform.scale(pg.image.load('posters/' + image), (100, 200))
    globals()[image.split('.')[0]] = pg.surfarray.array3d(im)


@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):
    screen_array[:] = np.array(filling_color)
    y_buffer = np.full(screen_width, screen_height)

    ray_angle = player_angle - h_fov
    for num_ray in range(screen_width):
        first_contact = False
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        for depth in range(1, ray_distance):
            x = int(player_pos[0] + depth * cos_a)
            if 0 < x < map_width:
                y = int(player_pos[1] + depth * sin_a)
                if 0 < y < map_height:

                    # убираем эффект рыбьего глаза
                    depth *= math.cos(player_angle - ray_angle)

                    # высота экрана
                    height_on_screen = int((player_height - height_map[x, y][0]) /
                                           depth * scale_height + player_pitch)

                    # убираем нежелательные линии
                    if not first_contact:
                        y_buffer[num_ray] = min(height_on_screen, screen_height)
                        first_contact = True

                    # убираем зеркаьный баг
                    if height_on_screen < 0:
                        height_on_screen = 0

                    # создаём линию для данного луча
                    if height_on_screen < y_buffer[num_ray]:
                        bright_proc = bright / 100 * (ray_distance - depth) / ray_distance
                        for screen_y in range(height_on_screen, y_buffer[num_ray]):
                            r, g, b = color_map[x, y]
                            if x in range(30, 30 + 100 // 2) and y in range(900 - 10, 900 + 80):
                                if 300 < int(height_map[x, y][0] - (screen_y - player_pitch) * (depth / 500)) + player_height * 2 < 600:
                                    r, g, b = fnaf_poster[(x - 30) * 2 + 1, int(((screen_y - player_pitch) * (depth / 500)) - player_height * 2 - 17)]
                            r *= bright_proc
                            g *= bright_proc
                            b *= bright_proc
                            screen_array[num_ray, screen_y] = (int(r), int(g), int(b))

                        # подойдёт для создания пыли
                        # if dust and screen_y == height_on_screen:
                        #     screen_array[num_ray, screen_y] = dust

                        y_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle
    return screen_array


class VoxelRender:
    def __init__(self, app):
        self.app = app
        self.player = app.player
        self.fov = math.pi / 5
        self.h_fov = self.fov / 2
        self.num_rays = app.width * 2
        self.delta_angle = self.fov / self.num_rays * 2
        self.ray_distance = 2000
        self.scale_height = 920
        self.screen_array = np.full((800, 450, 3), (0, 0, 0))

    def update(self):
        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                        self.player.height, self.player.pitch, 800,
                                        450, self.delta_angle, self.ray_distance,
                                        self.h_fov, self.scale_height)

    def draw(self):
        screen = pg.surfarray.make_surface(self.screen_array)
        h = self.app.height
        w = round(h // 450 * 1200)
        screen = pg.transform.scale(screen, (w, h))
        # screen = pg.transform.rotate(screen, 5 * self.player.move)

        self.app.screen.blit(screen, ((self.app.width - w) // 2, 0))
        # pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def changes(self, map, fill_color=filling_color, roof_color=False):
        global height_map, color_map, map_height, map_width, filling_color, roof
        height_map_img1 = pg.image.load(f'maps/{map}/height_map.jpg')
        height_map = pg.surfarray.array3d(height_map_img1)

        color_map_img1 = pg.image.load(f'maps/{map}/color_map.jpg')
        color_map = pg.surfarray.array3d(color_map_img1)

        map_height = len(height_map[0])
        map_width = len(height_map)
        filling_color = fill_color
        roof = roof_color
