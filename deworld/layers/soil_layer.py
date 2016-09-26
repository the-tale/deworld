# coding: utf-8
import math

from deworld.layers.base_layer import BaseLayer

from deworld.layers.vegetation_layer import VEGETATION_TYPE

class SoilLayer(BaseLayer):

    MIN = 0
    MAX = 1.0

    STEP = None

    OPTIMAL_TEMPERATURE = None
    OPTIMAL_WETNESS = None
    OPTIMAL_WIND = None

    POWER_PER_TEMPERATURE = None
    POWER_PER_WETNESS = None
    POWER_PER_WIND = None

    POWER_PER_VEGETATION_DESERT = None
    POWER_PER_VEGETATION_GRASS = None
    POWER_PER_VEGETATION_FOREST = None

    def __init__(self, **kwargs):
        super(SoilLayer, self).__init__(default=(self.MAX+self.MIN)/2, default_power=0.0, **kwargs)
        self._merge_config(self.config.LAYERS.SOIL)

    def serialize(self):
        return super(SoilLayer, self).serialize()

    @classmethod
    def deserialize(cls, world, data):
        return cls(world=world, data=data['data'], power=data.get('power'))

    def sync(self):
        for y in range(0, self.h):
            for x in range(0, self.w):
                power_points = self.power[y][x]

                power_points += math.fabs(self.OPTIMAL_TEMPERATURE - self.world.layer_temperature.data[y][x]) * self.POWER_PER_TEMPERATURE
                power_points += math.fabs(self.OPTIMAL_WETNESS - self.world.layer_wetness.data[y][x]) * self.POWER_PER_WETNESS

                vegetation = self.world.layer_vegetation.data[y][x]

                if vegetation != VEGETATION_TYPE.FOREST:
                    wind_speed = math.hypot(*self.world.layer_wind.data[y][x])
                    if wind_speed > self.OPTIMAL_WIND:
                        power_points += math.fabs(self.OPTIMAL_WIND - wind_speed) * self.POWER_PER_WIND

                power_points += {VEGETATION_TYPE.DESERT: self.POWER_PER_VEGETATION_DESERT,
                                 VEGETATION_TYPE.GRASS: self.POWER_PER_VEGETATION_GRASS,
                                 VEGETATION_TYPE.FOREST: self.POWER_PER_VEGETATION_FOREST}[vegetation]

                soil = self.data[y][x]

                if power_points > soil:
                    self.next_data[y][x] = min(self.MAX, soil + self.STEP)
                elif power_points < soil:
                    self.next_data[y][x] = max(self.MIN, soil - self.STEP)
                else:
                    self.next_data[y][x] = soil

                self.power[y][x] = power_points
