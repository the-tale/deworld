# coding: utf-8

from unittest import TestCase, mock

from deworld.world import World
from deworld.utils import E
from deworld.configs import BaseConfig

class WindLayerTests(TestCase):

    W = 100
    H = 100

    def setUp(self):
        self.world = World(w=self.W, h=self.H, config=BaseConfig)
        self.layer = self.world.layer_wind

    def fill_layer_with(self, data, from_x, from_y, to_x, to_y, value):
        for y in range(from_y, to_y+1):
            for x in range(from_x, to_x+1):
                data[y][x] = value

    @mock.patch('deworld.layers.WindLayer.BORDER_SPEED', 1.0)
    def test_get_speeds_border(self):
        v_speed, h_speed = self.layer._get_speeds(from_x=-1, from_y=0, to_x=0, to_y=0)
        self.assertTrue(v_speed > 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=self.W, from_y=0, to_x=self.W-1, to_y=0)
        self.assertTrue(v_speed < 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=0, from_y=-1, to_x=0, to_y=0)
        self.assertTrue( -E < v_speed < E and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=0, from_y=self.H, to_x=0, to_y=self.H-1)
        self.assertTrue( -E < v_speed < E and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=-1, from_y=-1, to_x=0, to_y=0)
        self.assertTrue(v_speed > 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=self.W, from_y=-1, to_x=self.W-1, to_y=0)
        self.assertTrue(v_speed < 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=-1, from_y=self.H, to_x=0, to_y=self.H-1)
        self.assertTrue(v_speed > 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=self.W, from_y=self.H, to_x=self.W-1, to_y=self.H-1)
        self.assertTrue(v_speed < 0 and h_speed < 0)

    @mock.patch('deworld.layers.WindLayer.TEMPERATURE_SPEED', 1.0)
    def test_get_speed_temperature_to_heigh(self):
        self.world.layer_temperature.data[5][5] += 1

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=4, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=6, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed < 0)

    @mock.patch('deworld.layers.WindLayer.TEMPERATURE_SPEED', 1.0)
    def test_get_speed_temperature_to_low(self):
        self.world.layer_temperature.data[5][5] -= 1

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=4, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=6, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed > 0)

    @mock.patch('deworld.layers.WindLayer.HEIGHT_SPEED', 1.0)
    def test_get_speed_height_to_heigh(self):
        self.world.layer_height.data[5][5] += 1

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=4, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=6, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed > 0)

    @mock.patch('deworld.layers.WindLayer.HEIGHT_SPEED', 1.0)
    def test_get_speed_height_to_low(self):
        self.world.layer_height.data[5][5] -= 1

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=5, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and -E < h_speed < E)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=4, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=5, from_y=6, to_x=5, to_y=5)
        self.assertTrue( -E < v_speed < E and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=4, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed > 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=4, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed > 0 and h_speed < 0)

        v_speed, h_speed = self.layer._get_speeds(from_x=6, from_y=6, to_x=5, to_y=5)
        self.assertTrue(v_speed < 0 and h_speed < 0)
