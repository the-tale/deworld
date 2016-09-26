# coding: utf-8

import math
import collections

from deworld.utils import prepair_to_approximation
from deworld.layers.base_layer import BaseLayer
from deworld.layers.vegetation_layer import VEGETATION_TYPE
from functools import reduce


class AtmospherePoint(collections.namedtuple('AtmospherePointBase', ['wind', 'temperature', 'wetness'])):
    pass


def points_reduces(accamulator, power_and_point):
    power, point = power_and_point

    return AtmospherePoint(wind=(point.wind[0]*power + accamulator.wind[0],
                                 point.wind[1]*power + accamulator.wind[1]),
                           temperature=point.temperature*power + accamulator.temperature,
                           wetness=point.wetness*power + accamulator.wetness)


class AtmosphereLayer(BaseLayer):
    DEFAULT = AtmospherePoint(wind=(0.0, 0.0), temperature=0.0, wetness=0.0)

    # configs
    MAX_WIND_SPEED = None
    DELTA = None

    WIND_AK = None
    WIND_WK = None

    WIND_FOREST_MULTIPLIER = None

    TEMP_AK = None
    TEMP_WK = None

    WET_AK = None
    WET_WK = None

    def __init__(self, **kwargs):
        super(AtmosphereLayer, self).__init__(default=self.DEFAULT, **kwargs)

        self._merge_config(self.config.LAYERS.ATMOSPHERE)

        self.area_deltas = []
        for y in range(-self.DELTA, self.DELTA+1):
            for x in range(-self.DELTA, self.DELTA+1):
                if math.hypot(y, x) > self.DELTA:
                    continue
                self.area_deltas.append((x, y))

    def serialize(self):
        return super(AtmosphereLayer, self).serialize()

    @classmethod
    def deserialize(cls, world, data):
        for row in data['data']:
            row[:] = [AtmospherePoint(wind=tuple(e[0]), temperature=e[1], wetness=e[2]) for e in row]

        power = data.get('power')

        return cls(world=world, data=data['data'], power=power)

    def sync(self):

        for y in range(0, self.h):
            for x in range(0, self.w):
                self.power[y][x] = []

        for y in range(0, self.h):
            for x in range(0, self.w):
                point = self.data[y][x]
                next_x = x+point.wind[0]*self.MAX_WIND_SPEED
                next_y = y+point.wind[1]*self.MAX_WIND_SPEED

                for dx, dy in self.area_deltas:
                    affected_x = int(next_x+dx)
                    affected_y = int(next_y+dy)

                    if not (0 <= affected_x < self.w and 0 <= affected_y < self.h):
                        continue

                    dist = math.hypot(next_x-affected_x, next_y-affected_y)
                    self.power[affected_y][affected_x].append((dist, point))


        for y in range(0, self.h):
            for x in range(0, self.w):
                powers = prepair_to_approximation(self.power[y][x], default=self.DEFAULT)
                point = reduce(points_reduces, powers, self.DEFAULT)

                wind_multiplier = 1.0

                if self.world.layer_vegetation.data[y][x] == VEGETATION_TYPE.FOREST:
                    wind_multiplier *= self.WIND_FOREST_MULTIPLIER

                result = AtmospherePoint(wind=( (point.wind[0]*self.WIND_AK+self.world.layer_wind.data[y][x][0]*self.WIND_WK) * wind_multiplier,
                                                (point.wind[1]*self.WIND_AK+self.world.layer_wind.data[y][x][1]*self.WIND_WK) * wind_multiplier),
                                        temperature=point.temperature*self.TEMP_AK+self.world.layer_temperature.data[y][x]*self.TEMP_WK,
                                        wetness=point.wetness*self.WET_AK+self.world.layer_wetness.data[y][x]*self.WET_WK)
                self.next_data[y][x] = result
