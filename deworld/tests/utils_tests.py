# coding: utf-8

from unittest import TestCase

from deworld.utils import E, prepair_to_approximation, resize2d, shift2d

class UtilsTests(TestCase):

    def setUp(self):
        pass

    def test_prepair_to_approximation(self):
        powers = prepair_to_approximation([(1, 'a'), (3, 'b'), (10, 'c')])
        Q = 3.0/43
        self.assertEqual(['a', 'b', 'c'], [p[1] for p in powers])
        self.assertTrue(-E < powers[0][0] - Q*10 < E)
        self.assertTrue(-E < powers[1][0] - Q*10/3 < E)
        self.assertTrue(-E < powers[2][0] - Q < E)

    def test_prepair_to_approximation_with_0_distance(self):
        powers = prepair_to_approximation([(1, 'a'), (0, 'b'), (10, 'c')])
        self.assertEqual(powers, [(1, 'b')])

    def test_prepair_to_approximation_with_no_points(self):
        powers = prepair_to_approximation([], default='c')
        self.assertEqual(powers, [(1, 'c')])

    def test_resize2d_increase(self):
        array = [[1, 2 ,3],
                 [4, 5, 6]]
        self.assertEqual(resize2d(array, 5, 6), [[1, 2, 3, 3, 3],
                                                 [4, 5, 6, 6, 6],
                                                 [4, 5, 6, 6, 6],
                                                 [4, 5, 6, 6, 6],
                                                 [4, 5, 6, 6, 6],
                                                 [4, 5, 6, 6, 6]])

    def test_resize2d_when_x_not_chaged(self):
        array = [[1, 2 ,3],
                 [4, 5, 6]]
        self.assertEqual(resize2d(array, 3, 6), [[1, 2, 3],
                                                 [4, 5, 6],
                                                 [4, 5, 6],
                                                 [4, 5, 6],
                                                 [4, 5, 6],
                                                 [4, 5, 6]])

    def test_resize2d_reduce(self):
        array = [[1, 2, 3, 3, 3],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6]]
        self.assertEqual(resize2d(array, 3, 2), [[1, 2 ,3],
                                                 [4, 5, 6]])

    def test_resize2d_when_y_not_changed(self):
        array = [[1, 2, 3, 3, 3],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6],
                 [4, 5, 6, 6, 6]]
        self.assertEqual(resize2d(array, 3, 6), [[1, 2, 3],
                                                 [4, 5, 6],
                                                 [4, 5, 6],
                                                 [4, 5, 6],
                                                 [4, 5, 6],
                                                 [4, 5, 6]])

    def test_shift2d(self):
        array = [[1, 2, 3, 4, 5],
                 [2, 3, 4, 5, 6],
                 [3, 4, 5, 6, 7],
                 [4, 5, 6, 7, 8],
                 [5, 6, 7, 8, 9],
                 [6, 7, 8, 9, 0]]
        self.assertEqual(shift2d(array, dx=3, dy=2), [[7, 8, 9, 5, 6],
                                                      [8, 9, 0, 6, 7],
                                                      [3, 4, 5, 1, 2],
                                                      [4, 5, 6, 2, 3],
                                                      [5, 6, 7, 3, 4],
                                                      [6, 7, 8, 4, 5]])

    def test_shift2d_no_shift(self):
        array = [[1, 2, 3, 4, 5],
                 [2, 3, 4, 5, 6],
                 [3, 4, 5, 6, 7],
                 [4, 5, 6, 7, 8],
                 [5, 6, 7, 8, 9],
                 [6, 7, 8, 9, 0]]
        self.assertEqual(shift2d(array, dx=0, dy=0), array)
