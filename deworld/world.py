# coding: utf-8

from deworld import layers
from deworld.exceptions import DeworldException

class World(object):

    def __init__(self, w, h, config,
                 layer_height=None,
                 layer_temperature=None,
                 layer_wind=None,
                 layer_atmosphere=None,
                 layer_wetness=None,
                 layer_vegetation=None):
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

    def clear_power_points(self):
        self.power_points.clear()

    def add_power_point(self, power_point):
        if power_point.name in self.power_points:
            raise DeworldException('try to add duplicate power point "%s"' % power_point.name)
        self.power_points[power_point.name] = power_point

    def clear_biomes(self):
        del self.biomes[:]

    def add_biom(self, biom):
        for exists_biom in self.bioms:
            if exists_biom.id == biom.id:
                raise DeworldException('biom with id "%d" has already added to world' % biom.id)
        self.biomes.append(biom)

    def _select_biom(self, x, y):
        for biom in self.bioms:
            if biom.check(self, x, y):
                return biom

        raise DeworldException('can not find biom for coordinates (%d, %d). Last biom in bioms list always MUST accept any cell.' % (x, y))

    def get_biom_map(self):

        biom_map = []

        for y in xrange(self.h):
            row = []
            biom_map.append(row)
            for x in xrange(self.w):
                row.append(self._select_biom(x, y))

        return biom_map


    def do_step(self):

        for power_point in self.power_points.values():
            power_point.update_world(self)

        self.layer_height.sync()
        self.layer_temperature.sync()
        self.layer_wind.sync()
        self.layer_wetness.sync()
        self.layer_vegetation.sync()
        self.layer_atmosphere.sync()

        self.layer_height.apply()
        self.layer_temperature.apply()
        self.layer_wind.apply()
        self.layer_wetness.apply()
        self.layer_vegetation.apply()
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
                    layer_vegetation=data['layers']['vegetation'])

        return world

    def __eq__(self, other):
        return (self.w == other.w and
                self.h == other.h and
                self.layer_height == other.layer_height and
                self.layer_temperature == other.layer_temperature and
                self.layer_wind == other.layer_wind and
                self.layer_atmosphere == other.layer_atmosphere and
                self.layer_wetness == other.layer_wetness and
                self.layer_vegetation == other.layer_vegetation )
