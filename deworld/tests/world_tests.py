# coding: utf-8

from unittest import TestCase

from deworld.world import World
from deworld.configs import BaseConfig


class WorldTests(TestCase):

    W = 100
    H = 100

    def setUp(self):

        self.world = World(w=self.W, h=self.H, config=BaseConfig)
        self.layer = self.world.layer_vegetation

    def test_serialization(self):

        self.world.layer_height.data[5][5] = 1
        self.world.layer_temperature.data[5][5] = 2
        self.world.layer_wind.data[5][5] = 3
        self.world.layer_atmosphere.data[5][5] = 4
        self.world.layer_wetness.data[5][5] = 5
        self.world.layer_vegetation.data[5][5] = 6

        self.assertEqual(self.world, World.deserialize(config=BaseConfig, data=self.world.serialize()))
