# coding: utf-8
import math

from deworld.layers.base_layer import BaseLayer


class TemperatureLayer(BaseLayer):

    MIN = 0
    MAX = 1.0

    def __init__(self, **kwargs):
        super(TemperatureLayer, self).__init__(default=(self.MAX+self.MIN)/2, default_power=0.0, **kwargs)

    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                power_points = self.power[y][x]

                power_points = min(self.MAX, max(self.MIN, power_points))

                temperature = power_points * (1 - math.fabs(self.world.layer_height.data[y][x]))

                self.next_data[y][x] = temperature

                self.power[y][x] = 0
