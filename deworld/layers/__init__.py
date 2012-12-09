# coding: utf-8

from deworld.layers.base_layer import BaseLayer
from deworld.layers.height_layer import HeightLayer
from deworld.layers.temperature_layer import TemperatureLayer
from deworld.layers.wind_layer import WindLayer
from deworld.layers.wetness_layer import WetnessLayer
from deworld.layers.atmosphere_layer import AtmosphereLayer


class LAYER_TYPE:
    HEIGHT = 0
    TEMPERATURE = 1
    WIND = 2
    WETNESS = 3
    ATMOSPHERE = 4

__all__ = [LAYER_TYPE, BaseLayer, HeightLayer, TemperatureLayer, WindLayer, WetnessLayer, AtmosphereLayer]
