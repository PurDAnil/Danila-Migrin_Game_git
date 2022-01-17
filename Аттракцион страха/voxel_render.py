import pygame as pg
from numba import njit
import numpy as np
import math

height_map_img = pg.image.load('maps/test/height_map.jpg')
height_map = pg.surfarray.array3d(height_map_img)

color_map_img = pg.image.load('maps/test/color_map.jpg')
color_map = pg.surfarray.array3d(color_map_img)

map_height = len(height_map[0])
map_width = len(height_map)
filling_color = (0, 0, 0)
bright = 100
roof = False


# def poster(x, y, h, z):
#     print(POSTERS)


@njit(fastmath=True)
def ray_casting(screen_array, player_pos, player_angle, player_height, player_pitch,
                screen_width, screen_height, delta_angle, ray_distance, h_fov, scale_height):
    screen_array[:] = np.array(filling_color)
    y_buffer = np.full(screen_width, screen_height)
    posters = []

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
                            r *= bright_proc
                            g *= bright_proc
                            b *= bright_proc
                            screen_array[num_ray, screen_y] = (int(r), int(g), int(b))
                        posters.append((x, y, height_on_screen, y_buffer[num_ray], num_ray, bright_proc))

                        # подойдёт для создания пыли
                        # if dust and screen_y == height_on_screen:
                        #     screen_array[num_ray, screen_y] = dust

                        y_buffer[num_ray] = height_on_screen

        ray_angle += delta_angle
    return screen_array, posters


def poster_render(screen_array, posters, poster_cords, player_height):
    for poster in posters:
        poster.flag = True
        for i in poster_cords:
            x, y, height_on_screen, y_buffer, num_ray, bright_proc = i
            if poster.flag and (
                    poster.z == 'x' and y == poster.y and x in range(poster.x, poster.x + poster.size[0])) or \
                    (poster.z == 'y' and x == poster.x and y in range(poster.y, poster.y + poster.size[0])):
                if poster.z == 'x':
                    for x1 in range(num_ray, num_ray + poster.size[0]):
                        if 0 <= x1 - x < 800:
                            for h1 in range(poster.h - poster.size[1], poster.h):
                                if 450 > height_on_screen - abs(h1 - poster.size[1]) + height_map[x, y][0] >= 0:
                                    r, g, b = poster.image[x1 - num_ray - 1, h1 - poster.h + 1]
                                    r *= bright_proc
                                    g *= bright_proc
                                    b *= bright_proc
                                    screen_array[
                                        x1 - x, height_on_screen - abs(h1 - poster.size[1]) + height_map[x, y][0]] = (
                                    int(r), int(g), int(b))
                                    poster.flag = False
                                    # for screen_y in range(height_on_screen, y_buffer):
                                    #     print(player_height, y_buffer)
                                    #     height = map_height - screen_y
                                    #     if height in range(poster.h - poster.size[1], poster.h):
                                    #         if poster.z == 'x':
                                    #             r, g, b = poster.image[x - poster.x, abs(height - poster.h)]
                                    #         else:
                                    #             r, g, b = poster.image[y - poster.y, abs(height - poster.h)]
                                    #         r *= bright_proc
                                    #         g *= bright_proc
                                    #         b *= bright_proc
                                    #         screen_array[num_ray, screen_y] = (int(r), int(g), int(b))
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
        self.screen_array, posters = ray_casting(self.screen_array, self.player.pos, self.player.angle,
                                                 self.player.height, self.player.pitch, 800,
                                                 450, self.delta_angle, self.ray_distance,
                                                 self.h_fov, self.scale_height)
        if self.app.posters:
            self.screen_array = poster_render(self.screen_array, self.app.posters, posters, self.player.height)

    def draw(self):
        screen = pg.surfarray.make_surface(self.screen_array)
        h = self.app.height
        w = int(h // 4.5 * 8)
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
