import pygame as pg
from numba import njit
import numpy as np
import math
import os

color_map_img = pg.image.load('maps/fnaf/color_map.jpg')
color_map = pg.surfarray.array3d(color_map_img)

height_map_img1 = pg.image.load('maps/fnaf/height_map.jpg')
openm = pg.surfarray.array3d(height_map_img1)

height_map_img2 = pg.image.load('maps/fnaf_left/height_map.jpg')
left = pg.surfarray.array3d(height_map_img2)

height_map_img3 = pg.image.load('maps/fnaf_right/height_map.jpg')
right = pg.surfarray.array3d(height_map_img3)

height_map_img4 = pg.image.load('maps/fnaf_close/height_map.jpg')
block = pg.surfarray.array3d(height_map_img4)

map_height = len(openm[0])
map_width = len(openm)
bright = 100

posters_name = []
posters_image = []
for image in os.listdir('posters'):
    im = pg.transform.scale(pg.image.load('posters/' + image), (100, 200))
    posters_name.append(image.split('.')[0])
    posters_image.append(pg.surfarray.array3d(im))


@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height,
                all_posters, all_posters_names, p_x, p_y, p_z, p_im, height_map):
    screen_array[:] = np.array((0, 0, 0))
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
                            # Отрисовка "плакатов" (столько мучений)
                            for el in range(len(p_x)):
                                vp_x = p_x[el]
                                vp_y = p_y[el]
                                vp_z = p_z[el]
                                vp_im = p_im[el]
                                if vp_z == 'x' and x in range(vp_x, vp_x + 50) and y in range(vp_y - 5, vp_y + 5):
                                    if 300 < int(height_map[x, y][0] - (screen_y - player_pitch) * (depth / 500)) \
                                            + player_height * 2 < 600:
                                        key = all_posters_names.index(vp_im)
                                        certain_poster = all_posters[key]
                                        r, g, b = certain_poster[(x - vp_x) * 2 + 1, int(((screen_y - player_pitch)
                                                                                          * (depth / 500))
                                                                                         - player_height * 2 - 17)]
                                elif vp_z == 'y' and y in range(vp_y, vp_y + 50) and x in range(vp_x - 5, vp_x + 5):
                                    if 300 < int(height_map[x, y][0] - (screen_y - player_pitch) * (depth / 500)) \
                                            + player_height * 2 < 600:
                                        key = all_posters_names.index(vp_im)
                                        certain_poster = all_posters[key]
                                        r, g, b = certain_poster[(y - vp_y) * 2 + 1, int(((screen_y - player_pitch)
                                                                                          * (depth / 500))
                                                                                         - player_height * 2 - 17)]
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
        self.door = 'openm'
        self.height_map = openm
        self.app = app
        self.player = app.player
        self.fov = math.pi / 5
        self.h_fov = self.fov / 2
        self.num_rays = app.width * 2
        self.delta_angle = self.fov / self.num_rays * 2
        self.ray_distance = 1200
        self.scale_height = 920
        self.screen_array = np.full((1000, 450, 3), (0, 0, 0))

    def update(self):
        x, y, z, images = self.app.posters
        self.screen_array = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                        self.player.height, self.player.pitch, 1000,
                                        450, self.delta_angle, self.ray_distance,
                                        self.h_fov, self.scale_height, posters_image,
                                        posters_name, x, y, z, images, self.height_map)

    def draw(self):
        screen = pg.surfarray.make_surface(self.screen_array)
        h = self.app.height
        w = h / 450 * 800
        screen = pg.transform.scale(screen, (w, h))
        # screen = pg.transform.rotate(screen, 5 * self.player.move)

        self.app.screen.blit(screen, ((self.app.width - w) // 2, 0))
        # pg.surfarray.blit_array(self.app.screen, self.screen_array)

    def change(self, map):
        self.door = map
        self.height_map = globals()[map]
