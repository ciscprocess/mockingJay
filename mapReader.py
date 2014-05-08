__author__ = 'Whitney'

import sys
import PIL
import pygame
from locationDef import LocationDefinition
from PIL import Image


def deep_forest(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID deep_forest\n')
    test_file.close()
    terrain_type = 0

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.3)
    definition.set_water_chance(0)
    definition.set_short_stick_chance(0.8)
    definition.set_visibility(0.2)
    definition.set_sharp_stone_chance(0.1)
    definition.set_feather_chance(0.2)
    definition.set_vine_chance(0.4)
    definition.set_speed_change(2)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.6)
    definition.set_broad_stone_chance(0.05)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.05)
    definition.set_thorns_chance(0.3)

    return definition

def dirt(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID Dirt\n')
    test_file.close()
    terrain_type = 1

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.5)
    definition.set_feather_chance(0.05)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.1)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.2)
    definition.set_thorns_chance(0.0)

    return definition


def grass(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID Grass\n')
    test_file.close()
    terrain_type = 2

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.1)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.1)
    definition.set_feather_chance(0.2)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.1)
    definition.set_long_grass_chance(0.2)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.1)
    definition.set_thorns_chance(0.0)

    return definition

def ice(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID Ice\n')
    test_file.close()
    terrain_type = 3

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.6)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.0)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(3)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.0)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.0)
    definition.set_thorns_chance(0.0)

    return definition

def light_forest(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID light_forest\n')
    test_file.close()
    terrain_type = 4

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.3)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.9)
    definition.set_visibility(0.9)
    definition.set_sharp_stone_chance(0.3)
    definition.set_feather_chance(0.6)
    definition.set_vine_chance(0.05)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.6)
    definition.set_broad_stone_chance(0.1)
    definition.set_long_grass_chance(0.1)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.1)
    definition.set_thorns_chance(0.1)

    return definition

def low_vegetation(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID low_vegetation\n')
    test_file.close()
    terrain_type = 5

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.6)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.05)
    definition.set_visibility(0.05)
    definition.set_sharp_stone_chance(0.2)
    definition.set_feather_chance(0.2)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.1)
    definition.set_long_grass_chance(0.1)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.05)
    definition.set_thorns_chance(0.6)

    return definition

def mud(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID Mud\n')
    test_file.close()
    terrain_type = 6

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.05)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.1)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.1)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.1)
    definition.set_thorns_chance(0.0)

    return definition

def rock(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID Rock\n')
    test_file.close()
    terrain_type = 7

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.9)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.7)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.8)
    definition.set_thorns_chance(0.0)

    return definition

def sand(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID Sand\n')
    test_file.close()
    terrain_type = 8

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.2)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.0)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.1)
    definition.set_thorns_chance(0.0)

    return definition

def shallow_water(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID shallow_water\n')
    test_file.close()
    terrain_type = 9

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(1)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(0.0)
    definition.set_sharp_stone_chance(0.2)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.05)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.05)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.6)
    definition.set_pebbles_chance(0.5)
    definition.set_thorns_chance(0.0)

    return definition

def snow(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID snow\n')
    test_file.close()
    terrain_type = 10

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.2)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(0.0)
    definition.set_sharp_stone_chance(0.1)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(2)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.05)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.1)
    definition.set_thorns_chance(0.0)

    return definition

def swimming_water(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID swimming_water\n')
    test_file.close()
    terrain_type = 11

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0)
    definition.set_water_chance(1)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(0.5)
    definition.set_sharp_stone_chance(0.0)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0)
    definition.set_broad_stone_chance(0.1)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.5)
    definition.set_thorns_chance(0.0)

    return definition

def tall_grass(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID tall_grass\n')
    test_file.close()
    terrain_type = 12

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.2)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.1)
    definition.set_visibility(0.7)
    definition.set_sharp_stone_chance(0.2)
    definition.set_feather_chance(0.2)
    definition.set_vine_chance(0.4)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.05)
    definition.set_broad_stone_chance(0.0)
    definition.set_long_grass_chance(1)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.05)
    definition.set_thorns_chance(0.05)

    return definition

def wading_water(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID wading_water\n')
    test_file.close()
    terrain_type = 13

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(1)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.4)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.1)
    definition.set_speed_change(3)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.2)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.7)
    definition.set_pebbles_chance(0.2)
    definition.set_thorns_chance(0.0)

    return definition

def cornucopia(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID cornucopia\n')
    test_file.close()
    terrain_type = 14

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.5)
    definition.set_water_chance(0.3)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.0)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.9)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.0)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.0)
    definition.set_thorns_chance(0.0)

    return definition

def start_spot(definition):
    test_file = open('maptest.txt', 'a')
    test_file.write('Pixel ID start_spot\n')
    test_file.close()
    terrain_type = 15

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(1)
    definition.set_sharp_stone_chance(0.0)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(1)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.0)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.0)
    definition.set_thorns_chance(0.0)

    return definition

def color_error(definition):
    terrain_type = 16

    definition.set_terrain(terrain_type)
    definition.set_food_chance(0.0)
    definition.set_water_chance(0.0)
    definition.set_short_stick_chance(0.0)
    definition.set_visibility(0)
    definition.set_sharp_stone_chance(0.0)
    definition.set_feather_chance(0.0)
    definition.set_vine_chance(0.0)
    definition.set_speed_change(0)
    definition.set_weapon_chance(0.0)
    definition.set_long_stick_chance(0.0)
    definition.set_broad_stone_chance(0.0)
    definition.set_long_grass_chance(0.0)
    definition.set_reeds_chance(0.0)
    definition.set_pebbles_chance(0.0)
    definition.set_thorns_chance(0.0)

    return definition

"""My Python Switch Case Based on Pixel Value"""
switch = {(1, 35, 18) : deep_forest,
          (97, 63, 2) : dirt,
          (70, 152, 18) : grass,
          (233, 244, 248) : ice,
          (2, 117, 62) : light_forest,
          (104, 142, 65) : low_vegetation,
          (58, 43, 20) : mud,
          (155, 154, 150) : rock,
          (246, 238, 176) : sand,
          (184, 224, 236) : shallow_water,
          (247, 249, 248) : snow,
          (38, 100, 121): swimming_water,
          (169, 153, 18): tall_grass,
          (88, 156, 179): wading_water,
          (0,0,0): cornucopia,
          (84,86,90): start_spot,
          (300,300,300): color_error

}


def read_map(map_input):
    test_file = open('maptest.txt', 'a')
    test_file.write('\n\n=============================\n_new Map Test\n=============================\n\n')
    map = Image.open(map_input)

    game_map = [[0 for t in xrange(map.size[0])] for r in xrange(map.size[1])]

    pixel_map = map.load()
    for i in range(map.size[0]):    # for every pixel:
        for j in range(map.size[1]):
            pixel = pixel_map[i,j]
            if pixel in switch:
                definition = LocationDefinition()
                loc_def  = switch[pixel](definition)
                game_map[i][j] = loc_def
            else:
                definition = LocationDefinition()
                loc_def = switch[(300,300,300)](definition)
                game_map[i][j] = loc_def
    test_file.close()
    return game_map


def get_neighbors(map, location):
    w = len(map)
    h = len(map[0])
    up = (location[0], (location[1] - 1) % h)
    left = ((location[0] - 1) % w, location[1])
    down = (location[0], (location[1] + 1) % h)
    right = ((location[0] + 1) % w, location[1])
    return [up, left, down, right]


def get_neighbors2(map, location):
    w = len(map)
    h = len(map[0])
    up = (location[0], (location[1] - 1) % h)
    left = ((location[0] - 1) % w, location[1])
    down = (location[0], (location[1] + 1) % h)
    right = ((location[0] + 1) % w, location[1])
    return [up, down, right, left]


def l1_dist(state1, state2):
    return abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])


def add_states(state1, state2):
    t = (state1[0] + state2[0], state1[1] + state2[1])
    return t
