# coding: utf-8
import math

from deworld.layers.base_layer import BaseLayer


class TemperatureLayer(BaseLayer):

    MIN = 0
    MAX = 1.0

    HEIGHT_PENALTY = None
    POWER_AK = None
    POWER_WK = None

    def __init__(self, **kwargs):
        super(TemperatureLayer, self).__init__(default=(self.MAX+self.MIN)/2, default_power=0.0, **kwargs)
        self._merge_config(self.config.LAYERS.TEMPERATURE)

    def serialize(self):
        return super(TemperatureLayer, self).serialize()

    @classmethod
    def deserialize(cls, world, data):
        return cls(world=world, data=data['data'], power=data.get('power'))

    def sync(self):

        for y in range(0, self.h):
            for x in range(0, self.w):
                power_points = self.power[y][x]

                power_points = min(self.MAX, max(self.MIN, power_points))

                temperature = power_points - (math.fabs(self.world.layer_height.data[y][x]) * self.HEIGHT_PENALTY)

                temperature = temperature * self.POWER_WK + self.world.layer_atmosphere.data[y][x].temperature * self.POWER_AK

                self.next_data[y][x] = temperature

                self.power[y][x] = power_points
