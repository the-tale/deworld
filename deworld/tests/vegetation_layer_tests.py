# coding: utf-8

from unittest import TestCase, mock

from deworld.world import World
from deworld.layers import VEGETATION_TYPE
from deworld.configs import BaseConfig


class VegetationLayerTests(TestCase):

    W = 100
    H = 100

    def setUp(self):

        self.world = World(w=self.W, h=self.H, config=BaseConfig)
        self.layer = self.world.layer_vegetation


    def test_border_right_power_no_border(self):
        self.assertEqual(self.layer._border_right_power(1.0, 50, 60, 70), 1.0)

    def test_border_right_power_abroad(self):
        self.assertEqual(self.layer._border_right_power(1.0, 80, 60, 70), 0.0)

    def test_border_right_power_between(self):
        self.assertEqual(self.layer._border_right_power(1.0, 65, 60, 70), 0.5)


    def test_border_left_power_abroad(self):
        self.assertEqual(self.layer._border_left_power(1.0, 50, 70, 60), 0.0)

    def test_border_left_power_no_border(self):
        self.assertEqual(self.layer._border_left_power(1.0, 80, 70, 60), 1.0)

    def test_border_left_power_between(self):
        self.assertEqual(self.layer._border_left_power(1.0, 65, 70, 60), 0.5)


    @mock.patch('deworld.layers.vegetation_layer.VegetationLayer.SPAWN_PROBABILITY', -1)
    def test_can_spawn_cannot(self):
        self.assertFalse(self.layer.can_spawn(5, 5, [VEGETATION_TYPE.FOREST]))

    @mock.patch('deworld.layers.vegetation_layer.VegetationLayer.SPAWN_PROBABILITY', -1)
    def test_can_spawn_can(self):
        self.assertFalse(self.layer.can_spawn(5, 5, [VEGETATION_TYPE.FOREST]))
        self.assertTrue(self.layer.can_spawn(5, 5, [VEGETATION_TYPE.DESERT]))
        self.assertTrue(self.layer.can_spawn(5, 5, [VEGETATION_TYPE.FOREST, VEGETATION_TYPE.DESERT]))

    @mock.patch('deworld.layers.vegetation_layer.VegetationLayer.SPAWN_PROBABILITY', 0.1)
    def test_can_spawn_with_probability(self):
        spawned = False
        for i in range(1000):
            spawned = spawned or self.layer.can_spawn(5, 5, [VEGETATION_TYPE.FOREST])

        self.assertTrue(spawned)
