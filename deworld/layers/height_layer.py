# coding: utf-8

from deworld.layers.base_layer import BaseLayer

class HeightLayer(BaseLayer):

    MIN = -1.0
    MAX = 1.0
    STEP = 0.01

    def __init__(self, **kwargs):
        super(HeightLayer, self).__init__(default=(self.MAX + self.MIN) / 2, **kwargs)


    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                if power_points > original_value:
                    self.next_data[y][x] = min(original_value + self.STEP, self.MAX)
                elif power_points < original_value:
                    self.next_data[y][x] = max(original_value - self.STEP, self.MIN)

                self.power[y][x] = 0
