# coding: utf-8

# hight colors from:
# http://en.wikipedia.org/wiki/Wikipedia:Graphics_Lab/Resources/QGIS/Create_a_topographic_background
# http://en.wikipedia.org/wiki/Wikipedia:WikiProject_Maps/Conventions/Topographic_maps
# http://en.wikipedia.org/wiki/Wikipedia:WikiProject_Maps/Conventions

import math
import collections

class Color(collections.namedtuple('BaseColor', ['red', 'green', 'blue'])):

    @property
    def rgb(self): return (self.red, self.green, self.blue)


class HeightColorMap(object):

    HIGH_COLORS = list(reversed([ Color(red=245, green=244, blue=242),
                                  Color(red=224, green=222, blue=216),
                                  Color(red=202, green=195, blue=184),
                                  Color(red=186, green=174, blue=154),
                                  Color(red=172, green=154, blue=124),
                                  Color(red=170, green=135, blue=83),
                                  Color(red=185, green=152, blue=90),
                                  Color(red=195, green=167, blue=107),
                                  Color(red=202, green=185, blue=130),
                                  Color(red=211, green=202, blue=157),
                                  Color(red=222, green=214, blue=163),
                                  Color(red=232, green=225, blue=182),
                                  Color(red=239, green=235, blue=192),
                                  Color(red=225, green=228, blue=181),
                                  Color(red=209, green=215, blue=171),
                                  Color(red=189, green=204, blue=150),
                                  Color(red=168, green=198, blue=143),
                                  Color(red=148, green=191, blue=139),
                                  Color(red=172, green=208, blue=165),
                                  ]))

    LOW_COLORS = [ Color(red=216, green=242, blue=254),
                   Color(red=198, green=236, blue=255),
                   Color(red=185, green=227, blue=255),
                   Color(red=172, green=219, blue=251),
                   Color(red=161, green=210, blue=247),
                   Color(red=150, green=201, blue=240),
                   Color(red=141, green=193, blue=234),
                   Color(red=132, green=185, blue=227),
                   Color(red=121, green=178, blue=222),
                   Color(red=113, green=171, blue=216)]

    @classmethod
    def _get_color(cls, colors, norm):
        return colors[min(len(colors)-1, int(math.floor(len(colors)*norm)))]

    @classmethod
    def _get_color_interpolated(cls, colors, norm):
        c1 =  colors[min(len(colors)-1, int(math.floor(len(colors)*norm)))]
        c2 =  colors[min(len(colors)-1, int(math.ceil(len(colors)*norm)))]
        return Color(red=(c1.red+c2.red)/2,
                     green=(c1.green+c2.green)/2,
                     blue=(c1.blue+c2.blue)/2)

    @classmethod
    def get_color(cls, height, discret=True):

        if discret:
            if height >= 0:
                return cls._get_color(cls.HIGH_COLORS, height)
            else:
                return cls._get_color(cls.LOW_COLORS, -height)
        else:
            if height >= 0:
                return cls._get_color_interpolated(cls.HIGH_COLORS, height)
            else:
                return cls._get_color_interpolated(cls.LOW_COLORS, -height)


class GrayColorMap(object):

    @classmethod
    def get_color(cls, height, discret=True):
        return Color(int(255*height), int(255*height), int(255*height))


class RGBColorMap(object):

    @classmethod
    def get_color(cls, r, g, b, discret=True):
        return Color(int(255*r), int(255*g), int(255*b))
