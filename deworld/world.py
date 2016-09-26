# coding: utf-8
import random
import collections

from deworld import layers
from deworld.exceptions import DeworldException

def _randomize_value(value_min, value_max, value, fraction):
    delta = random.uniform(-fraction, fraction) * (value_max - value_min)
    return max(value_min, min(value_max, value+delta))

class CellInfo(collections.namedtuple('CellInfoBase', ['height', 'temperature', 'wind', 'wetness', 'vegetation', 'soil', 'atmo_wind', 'atmo_temperature', 'atmo_wetness'])):

    def randomize(self, seed, fraction):
        state = random.getstate()
        random.seed(seed)

        new_cell = CellInfo(height=_randomize_value(-1.0, 1.0, self.height, fraction),
                            temperature=_randomize_value(0.0, 1.0, self.temperature, fraction),
                            wind=(_randomize_value(-1.0, 1.0, self.wind[0], fraction), _randomize_value(-1.0, 1.0, self.wind[1], fraction)),
                            wetness=_randomize_value(0.0, 1.0, self.wetness, fraction),
                            vegetation=self.vegetation,
                            soil=_randomize_value(0.0, 1.0, self.soil, fraction),
                            atmo_wind=(_randomize_value(-1.0, 1.0, self.atmo_wind[0], fraction), _randomize_value(-1.0, 1.0, self.atmo_wind[1], fraction)),
                            atmo_temperature=_randomize_value(0.0, 1.0, self.atmo_temperature, fraction),
                            atmo_wetness=_randomize_value(0.0, 1.0, self.atmo_wetness, fraction))
        random.setstate(state)
        return new_cell

    @property
    def mid_temperature(self): return (self.temperature + self.atmo_temperature) / 2.0

    @property
    def mid_wetness(self): return (self.wetness + self.atmo_wetness) / 2.0


class CellPowerInfo(collections.namedtuple('CellPowerInfoBase', ['height', 'temperature', 'wind', 'wetness', 'vegetation', 'soil'])):
    pass


class World(object):

    def __init__(self, w, h, config,
                 layer_height=None,
                 layer_temperature=None,
                 layer_wind=None,
                 layer_atmosphere=None,
                 layer_wetness=None,
                 layer_vegetation=None,
                 layer_soil=None):
        self.config = config
        self.w = w
        self.h = h

        self.power_points = {}
        self.biomes = []

        self.layer_height = layers.HeightLayer(world=self) if layer_height is None else layers.HeightLayer.deserialize(world=self, data=layer_height)
        self.layer_temperature = layers.TemperatureLayer(world=self) if layer_temperature is None else layers.TemperatureLayer.deserialize(world=self, data=layer_temperature)
        self.layer_wind = layers.WindLayer(world=self) if layer_wind is None else layers.WindLayer.deserialize(world=self, data=layer_wind)
        self.layer_atmosphere = layers.AtmosphereLayer(world=self) if layer_atmosphere is None else layers.AtmosphereLayer.deserialize(world=self, data=layer_atmosphere)
        self.layer_wetness = layers.WetnessLayer(world=self) if layer_wetness is None else layers.WetnessLayer.deserialize(world=self, data=layer_wetness)
        self.layer_vegetation = layers.VegetationLayer(world=self) if layer_vegetation is None else layers.VegetationLayer.deserialize(world=self, data=layer_vegetation)
        self.layer_soil = layers.SoilLayer(world=self) if layer_soil is None else layers.SoilLayer.deserialize(world=self, data=layer_soil)

    def clear_power_points(self):
        self.power_points.clear()

    def add_power_point(self, power_point):
        if power_point.name in self.power_points:
            raise DeworldException('try to add duplicate power point "%s"' % power_point.name)
        self.power_points[power_point.name] = power_point

    def clear_biomes(self):
        del self.biomes[:]

    def add_biom(self, biom):
        self.biomes.append(biom)

    def cell_info(self, x, y):
        return CellInfo(height=self.layer_height.data[y][x],
                        temperature=self.layer_temperature.data[y][x],
                        wind=self.layer_wind.data[y][x],
                        wetness=self.layer_wetness.data[y][x],
                        vegetation=self.layer_vegetation.data[y][x],
                        soil=self.layer_soil.data[y][x],
                        atmo_wind=self.layer_atmosphere.data[y][x].wind,
                        atmo_temperature=self.layer_atmosphere.data[y][x].temperature,
                        atmo_wetness=self.layer_atmosphere.data[y][x].wetness)

    def cell_power_info(self, x, y):
        return CellPowerInfo(height=self.layer_height.power[y][x],
                             temperature=self.layer_temperature.power[y][x],
                             wind=self.layer_wind.power[y][x],
                             wetness=self.layer_wetness.power[y][x],
                             vegetation=self.layer_vegetation.power[y][x],
                             soil=self.layer_soil.power[y][x] )

    def _select_biom(self, x, y):
        # for biom in self.biomes:
        #     if biom.check(self.cell_info(x, y)):
        #         return biom

        best_points = 0
        best_biom = None

        for biom in self.biomes:
            points =  biom.check(self.cell_info(x, y))
            if best_biom is None or best_points < points:
                best_points = points
                best_biom = biom

        return best_biom

        # raise DeworldException('can not find biom for coordinates (%d, %d). Last biom in biomes list always MUST accept any cell.' % (x, y))

    def get_biomes_map(self):

        biom_map = []

        for y in range(self.h):
            row = []
            biom_map.append(row)
            for x in range(self.w):
                row.append(self._select_biom(x, y))

        return biom_map


    def resize(self, new_w, new_h):
        if self.w == new_w and self.h == new_h:
            return

        dx = (new_w - self.w) // 2
        dy = (new_h - self.h) // 2

        self.w = new_w
        self.h = new_h

        self.layer_height.resize(new_w, new_h, dx, dy)
        self.layer_temperature.resize(new_w, new_h, dx, dy)
        self.layer_wind.resize(new_w, new_h, dx, dy)
        self.layer_wetness.resize(new_w, new_h, dx, dy)
        self.layer_vegetation.resize(new_w, new_h, dx, dy)
        self.layer_soil.resize(new_w, new_h, dx, dy)
        self.layer_atmosphere.resize(new_w, new_h, dx, dy)

        return dx, dy


    def do_step(self):

        self.layer_height.reset_powers()
        self.layer_temperature.reset_powers()
        self.layer_wind.reset_powers()
        self.layer_wetness.reset_powers()
        self.layer_vegetation.reset_powers()
        self.layer_soil.reset_powers()
        self.layer_atmosphere.reset_powers()


        for power_point in self.power_points.values():
            power_point.update_world(self)

        self.layer_height.sync()
        self.layer_temperature.sync()
        self.layer_wind.sync()
        self.layer_wetness.sync()
        self.layer_vegetation.sync()
        self.layer_soil.sync()
        self.layer_atmosphere.sync()

        self.layer_height.apply()
        self.layer_temperature.apply()
        self.layer_wind.apply()
        self.layer_wetness.apply()
        self.layer_vegetation.apply()
        self.layer_soil.apply()
        self.layer_atmosphere.apply()


    def serialize(self):
        return {'w': self.w,
                'h': self.h,
                'layers': {
                    'height': self.layer_height.serialize(),
                    'temperature': self.layer_temperature.serialize(),
                    'wind': self.layer_wind.serialize(),
                    'wetness': self.layer_wetness.serialize(),
                    'vegetation': self.layer_vegetation.serialize(),
                    'soil': self.layer_soil.serialize(),
                    'atmosphere': self.layer_atmosphere.serialize()
                    }
                }

    @classmethod
    def deserialize(cls, config, data):

        world = cls(w=data['w'], h=data['h'], config=config,
                    layer_height=data['layers']['height'],
                    layer_temperature=data['layers']['temperature'],
                    layer_wind=data['layers']['wind'],
                    layer_atmosphere=data['layers']['atmosphere'],
                    layer_wetness=data['layers']['wetness'],
                    layer_vegetation=data['layers']['vegetation'],
                    layer_soil=data['layers'].get('soil'))

        return world

    def __eq__(self, other):
        return (self.w == other.w and
                self.h == other.h and
                self.layer_height == other.layer_height and
                self.layer_temperature == other.layer_temperature and
                self.layer_wind == other.layer_wind and
                self.layer_atmosphere == other.layer_atmosphere and
                self.layer_wetness == other.layer_wetness and
                self.layer_vegetation == other.layer_vegetation and
                self.layer_soil == other.layer_soil)
