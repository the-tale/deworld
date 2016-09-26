# coding: utf-8

from deworld.layers.base_layer import BaseLayer


class WetnessLayer(BaseLayer):

    MIN = 0.0
    MAX = 1.0

    STEP = None
    POWER_PER_HEIGHT = None
    POWER_PER_TEMPERATURE = None
    POWER_PER_ATMOSPHERE = None

    def __init__(self, **kwargs):
        super(WetnessLayer, self).__init__(default=0.0, **kwargs)
        self._merge_config(self.config.LAYERS.WETNESS)

    def serialize(self):
        return super(WetnessLayer, self).serialize()

    @classmethod
    def deserialize(cls, world, data):
        return cls(world=world, data=data['data'], power=data.get('power'))

    def sync(self):

        for y in range(0, self.h):
            for x in range(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                power_points += self.world.layer_height.data[y][x] * self.POWER_PER_HEIGHT
                power_points += self.world.layer_temperature.data[y][x] * self.POWER_PER_TEMPERATURE
                power_points += (self.world.layer_atmosphere.data[y][x].wetness - original_value) * self.POWER_PER_ATMOSPHERE

                if power_points > original_value:
                    self.next_data[y][x] = min(original_value + self.STEP, self.MAX)
                elif power_points < original_value:
                    self.next_data[y][x] = max(original_value - self.STEP, self.MIN)
                else:
                    self.next_data[y][x] = original_value

                self.power[y][x] = power_points
