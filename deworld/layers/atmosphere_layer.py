# coding: utf-8

import math
import collections

from deworld.utils import prepair_to_approximation
from deworld.layers.base_layer import BaseLayer


class AtmospherePoint(collections.namedtuple('AtmospherePointBase', ['wind', 'temperature'])):
    pass


def points_reduces(accamulator, power_and_point):
    power, point = power_and_point

    return AtmospherePoint(wind=(point.wind[0]*power + accamulator.wind[0],
                                 point.wind[1]*power + accamulator.wind[1]),
                           temperature=point.temperature*power + accamulator.temperature)


class AtmosphereLayer(BaseLayer):
    DEFAULT = AtmospherePoint(wind=(0.0, 0.0), temperature=0.0)
    MAX_WIND_SPEED = 4 # in cells
    DELTA = 3

    WIND_AK = 0.95
    WIND_WK = 1 - WIND_AK

    TEMP_AK = 0.75
    TEMP_WK = 1 - TEMP_AK

    def __init__(self, **kwargs):
        super(AtmosphereLayer, self).__init__(default=self.DEFAULT, **kwargs)

        self.area_deltas = []
        for y in xrange(-self.DELTA, self.DELTA+1):
            for x in xrange(-self.DELTA, self.DELTA+1):
                if math.hypot(y, x) > self.DELTA:
                    continue
                self.area_deltas.append((x, y))

    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                self.power[y][x] = []

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                point = self.data[y][x]
                next_x = x+point.wind[0]*self.MAX_WIND_SPEED
                next_y = y+point.wind[1]*self.MAX_WIND_SPEED

                # for affected_y in xrange(int(max(0, next_y-self.DELTA)), int(min(self.h, next_y+self.DELTA+1))):
                #     for affected_x in xrange(int(max(0, next_x-self.DELTA)), int(min(self.w, next_x+self.DELTA+1))):
                for dx, dy in self.area_deltas:
                    affected_x = int(next_x+dx)
                    affected_y = int(next_y+dy)

                    if not (0 <= affected_x < self.w and 0 <= affected_y < self.h):
                        continue

                    dist = math.hypot(next_x-affected_x, next_y-affected_y)
                    self.power[affected_y][affected_x].append((dist, point))


        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                powers = prepair_to_approximation(self.power[y][x], default=self.DEFAULT)
                point = reduce(points_reduces, powers, self.DEFAULT)
                result = AtmospherePoint(wind=(point.wind[0]*self.WIND_AK+self.world.layer_wind.data[y][x][0]*self.WIND_WK,
                                               point.wind[1]*self.WIND_AK+self.world.layer_wind.data[y][x][1]*self.WIND_WK),
                                        temperature=point.temperature*self.TEMP_AK+self.world.layer_temperature.data[y][x]*self.TEMP_WK)
                self.next_data[y][x] = result
