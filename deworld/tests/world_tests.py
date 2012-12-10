# coding: utf-8

from unittest import TestCase

from deworld.world import World
from deworld.configs import BaseConfig
from deworld.layers.atmosphere_layer import AtmospherePoint


class WorldTests(TestCase):

    W = 10
    H = 10

    def setUp(self):

        self.world = World(w=self.W, h=self.H, config=BaseConfig)
        self.layer = self.world.layer_vegetation

    def test_simple_step(self):
        self.world.do_step()

    def test_serialization(self):

        self.world.layer_height.data[5][5] = 1
        self.world.layer_temperature.data[5][5] = 2
        self.world.layer_wind.data[5][5] = (3.0, 3.0)
        self.world.layer_atmosphere.data[5][5] = AtmospherePoint(wind=(3.0, 3.0), temperature=-1, wetness=0.3)
        self.world.layer_wetness.data[5][5] = 5
        self.world.layer_vegetation.data[5][5] = 6

        self.assertEqual(self.world, World.deserialize(config=BaseConfig, data=self.world.serialize()))
        self.world.do_step()
