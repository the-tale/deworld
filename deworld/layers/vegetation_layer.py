# coding: utf-8
import random

from deworld.layers.base_layer import BaseLayer


class VEGETATION_TYPE:

    DESERT = 0
    GRASS = 1
    FOREST = 2



class VegetationLayer(BaseLayer):

    MIN = 0.0
    MAX = 1.0

    HEIGHT_FOREST_BARIER_START = None
    HEIGHT_FOREST_BARIER_END = None
    HEIGHT_GRASS_BARIER_START = None
    HEIGHT_GRASS_BARIER_END = None

    TEMPERATURE_FOREST_BARIER_START = None
    TEMPERATURE_FOREST_BARIER_END = None
    TEMPERATURE_GRASS_BARIER_START = None
    TEMPERATURE_GRASS_BARIER_END = None

    WETNESS_FOREST_BARIER_START = None
    WETNESS_FOREST_BARIER_END = None
    WETNESS_GRASS_BARIER_START = None
    WETNESS_GRASS_BARIER_END = None

    FOREST_BORDER = None
    GRASS_BORDER = None

    SPAWN_PROBABILITY = None


    def __init__(self, **kwargs):
        super(VegetationLayer, self).__init__(default=VEGETATION_TYPE.DESERT, default_power=(0.0, 0.0), **kwargs)
        self._merge_config(self.config.LAYERS.VEGETATION)

    def add_power(self, x, y, power):
        old_power = self.power[y][x]
        self.power[y][x] = (old_power[0] + power[0], old_power[1] + power[1])


    def _border_right_power(self, power, value, border_start, border_end):
        if value > border_start:
            if value > border_end:
                power = 0
            else:
                power -= float(value - border_start) / (border_end - border_start)

        return power

    def _border_left_power(self, power, value, border_start, border_end):
        if value < border_start:
            if value < border_end:
                power = 0
            else:
                power -= float(border_start - value) / (border_start - border_end)

        return power

    def can_spawn(self, x, y, type_):
        for y in xrange(y-1, y+1+1):
            for x in xrange(x-1, x+1+1):
                if not (0 <= y < self.h and 0 <= x < self.w):
                    continue
                if self.data[y][x] in type_:
                    return True

        return random.uniform(0, 1) < self.SPAWN_PROBABILITY

    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                power_points = self.power[y][x]

                power_grass, power_forest = power_points


                height = self.world.layer_height.data[y][x]
                power_forest = self._border_right_power(power_forest, height, self.HEIGHT_FOREST_BARIER_START, self.HEIGHT_FOREST_BARIER_END)
                power_grass = self._border_right_power(power_grass, height, self.HEIGHT_GRASS_BARIER_START, self.HEIGHT_GRASS_BARIER_END)

                temperature = self.world.layer_temperature.data[y][x]
                power_forest = self._border_right_power(power_forest, temperature, self.TEMPERATURE_FOREST_BARIER_START, self.TEMPERATURE_FOREST_BARIER_END)
                power_grass = self._border_right_power(power_grass, temperature, self.TEMPERATURE_GRASS_BARIER_START, self.TEMPERATURE_GRASS_BARIER_END)

                wetness = self.world.layer_wetness.data[y][x]
                power_forest = self._border_left_power(power_forest, wetness, self.WETNESS_FOREST_BARIER_START, self.WETNESS_FOREST_BARIER_END)
                power_grass = self._border_left_power(power_grass, wetness, self.WETNESS_GRASS_BARIER_START, self.WETNESS_GRASS_BARIER_END)


                if power_forest > power_grass and power_forest > self.FOREST_BORDER and self.can_spawn(x, y, [VEGETATION_TYPE.FOREST]):
                    self.next_data[y][x] = VEGETATION_TYPE.FOREST
                elif power_grass > self.GRASS_BORDER and self.can_spawn(x, y, [VEGETATION_TYPE.GRASS, VEGETATION_TYPE.FOREST]):
                    self.next_data[y][x] = VEGETATION_TYPE.GRASS
                else:
                    self.next_data[y][x] = VEGETATION_TYPE.DESERT

                self.power[y][x] = (0.0, 0.0)
