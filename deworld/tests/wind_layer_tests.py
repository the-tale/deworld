# coding: utf-8

from unittest import TestCase

from deworld.world import World


class WindLayerTests(TestCase):

    W = 100
    H = 100

    def setUp(self):

        self.world = World(self.W, self.H)
        self.layer = self.world.layer_wind


    # def test_modify_speed_zero(self):
    #     self.assertEqual(self.layer._modify_speed(speed=0, temp_delta=0, height_delta=0, distance=0, direction=1), 0)
    #     self.assertEqual(self.layer._modify_speed(speed=0, temp_delta=0, height_delta=0, distance=0, direction=-1), 0)

    # def test_modify_speed_temp(self):
    #     self.assertTrue(self.layer._modify_speed(speed=0, temp_delta=10, height_delta=0, distance=0, direction=1) > 0 )
    #     self.assertTrue(self.layer._modify_speed(speed=0, temp_delta=10, height_delta=0, distance=0, direction=-1) < 0 )
    #     self.assertTrue(self.layer._modify_speed(speed=0, temp_delta=-10, height_delta=0, distance=0, direction=1) > 0 )
    #     self.assertTrue(self.layer._modify_speed(speed=0, temp_delta=-10, height_delta=0, distance=0, direction=-1) < 0 )
