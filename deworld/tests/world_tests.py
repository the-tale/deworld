# coding: utf-8
import random

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

    def test_resize_increase(self):
        self.world.do_step()
        self.world.resize(self.world.w+2, self.world.h+3)
        self.world.do_step()

    def test_resize_decrease(self):
        self.world.do_step()
        self.world.resize(self.world.w-2, self.world.h-3)
        self.world.do_step()

    def test_serialization(self):

        self.world.layer_height.data[5][5] = 1
        self.world.layer_temperature.data[5][5] = 2
        self.world.layer_wind.data[5][5] = (3.0, 3.0)
        self.world.layer_atmosphere.data[5][5] = AtmospherePoint(wind=(3.0, 3.0), temperature=-1, wetness=0.3)
        self.world.layer_wetness.data[5][5] = 5
        self.world.layer_vegetation.data[5][5] = 1

        self.assertEqual(self.world, World.deserialize(config=BaseConfig, data=self.world.serialize()))
        self.world.do_step()

    def test_cell_info_randomize_stability(self):
        cell = self.world.cell_info(5, 5)
        randomized_cell = cell.randomize(1, 0.5)

        for i in range(100):
            self.assertEqual(randomized_cell, cell.randomize(1, 0.5))


    def test_cell_info_randomize_random_state_restore(self):
        random.seed(1)

        test_list = [random.randint(-100, 100) for i in range(100)]

        random.seed(1)

        cell = self.world.cell_info(5, 5)

        cell.randomize(1, 0.5)

        self.assertEqual(test_list, [random.randint(-100, 100) for i in range(100)])
