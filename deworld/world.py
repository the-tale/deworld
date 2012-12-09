# coding: utf-8

from deworld import layers

class WorldException(Exception): pass

class World(object):

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.power_points = {}

        self.layer_height = layers.HeightLayer(world=self, w=self.w, h=self.h)
        self.layer_temperature = layers.TemperatureLayer(world=self, w=self.w, h=self.h)
        self.layer_wind = layers.WindLayer(world=self, w=self.w, h=self.h)
        self.layer_atmosphere = layers.AtmosphereLayer(world=self, w=self.w, h=self.h)
        self.layer_wetness = layers.WetnessLayer(world=self, w=self.w, h=self.h)

    def add_power_point(self, power_point):
        if power_point.name in self.power_points:
            raise WorldException('try to add duplicate power point "%s"' % power_point.name)
        self.power_points[power_point.name] = power_point


    def do_step(self):

        for power_point in self.power_points.values():
            power_point.update_world(self)

        self.layer_height.sync()
        self.layer_temperature.sync()
        self.layer_wind.sync()
        self.layer_wetness.sync()
        self.layer_atmosphere.sync()

        self.layer_height.apply()
        self.layer_temperature.apply()
        self.layer_wind.apply()
        self.layer_wetness.apply()
        self.layer_atmosphere.apply()
