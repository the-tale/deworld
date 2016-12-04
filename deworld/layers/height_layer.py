# coding: utf-8

from deworld.layers.base_layer import BaseLayer

class HeightLayer(BaseLayer):

    MIN = -1.0
    MAX = 1.0
    E = 0.01

    # config
    STEP = None

    def __init__(self, **kwargs):
        super(HeightLayer, self).__init__(default=(self.MAX + self.MIN) / 2, default_power=(0.0, 0.0), **kwargs)
        self._merge_config(self.config.LAYERS.HEIGHT)

    def serialize(self):
        return super(HeightLayer, self).serialize()

    @classmethod
    def deserialize(cls, world, data):
        return cls(world=world, data=data['data'], power=data.get('power'))

    def add_power(self, x, y, power):
        old_power = self.power[y][x]
        self.power[y][x] = (old_power[0] + power[0], old_power[1] + power[1])

    def sync(self):

        for y in range(0, self.h):
            for x in range(0, self.w):
                original_value = self.data[y][x]
                power_points = self.power[y][x]

                if power_points[1] - power_points[0] > self.E:
                    self.next_data[y][x] = min(original_value + self.STEP, self.MAX)
                elif power_points[0] - power_points[1] > self.E:
                    self.next_data[y][x] = max(original_value - self.STEP, self.MIN)
                else:
                    self.next_data[y][x] = original_value

                self.power[y][x] = power_points
