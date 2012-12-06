# coding: utf-8

from deworld.layers.base_layer import BaseLayer


class TemperatureLayer(BaseLayer):

    HEIGHT_MULTIPLYER = 0.5

    def __init__(self, **kwargs):
        super(TemperatureLayer, self).__init__(default=0, **kwargs)

    def sync(self):

        for y in xrange(0, self.h):
            for x in xrange(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                # modify power on base of height
                height_norm = (float(self.world.layer_height.data[y][x]) /
                               self.world.layer_height.MAX)
                power_points *= self.HEIGHT_MULTIPLYER * height_norm

                if power_points > original_value:
                    self.next_data[y][x] = min(original_value + 1, self.MAX)
                elif power_points < original_value:
                    self.next_data[y][x] = max(original_value - 1, 0)

                self.power[y][x] = -self.next_data[y][x] # we lost temperature every step
