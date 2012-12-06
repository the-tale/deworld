# coding: utf-8

from deworld.layers.base_layer import BaseLayer

class HeightLayer(BaseLayer):

    def __init__(self, **kwargs):
        super(HeightLayer, self).__init__(default=self.MAX/2, **kwargs)


    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                if power_points > original_value:
                    self.next_data[y][x] = min(original_value + 1, self.MAX)
                elif power_points < original_value - self.MAX / 2:
                    self.next_data[y][x] = max(original_value - 1, 0)

                self.power[y][x] = 0
