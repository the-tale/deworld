# coding: utf-8

from deworld.layers.base_layer import BaseLayer
from deworld.layers.height_layer import HeightLayer
from deworld.layers.temperature_layer import TemperatureLayer
from deworld.layers.wind_layer import WindLayer

class LAYER_TYPE:
    HEIGHT = 0
    TEMPERATURE = 1
    WIND = 2

__all__ = [LAYER_TYPE, BaseLayer, HeightLayer, TemperatureLayer, WindLayer]
