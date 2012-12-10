# coding: utf-8


class BaseConfig:

    class LAYERS:

        class ATMOSPHERE:
            MAX_WIND_SPEED = 4 # in cells
            DELTA = 3

            WIND_AK = 0.95
            WIND_WK = 1 - WIND_AK

            WIND_FOREST_MULTIPLIER = 0.95

            TEMP_AK = 0.75
            TEMP_WK = 1 - TEMP_AK

            WET_AK = 0.75
            WET_WK = 1 - WET_AK

        class HEIGHT:
            STEP = 0.01

        class TEMPERATURE:
            pass

        class VEGETATION:
            HEIGHT_FOREST_BARIER_START = 0.4
            HEIGHT_FOREST_BARIER_END = 0.7
            HEIGHT_GRASS_BARIER_START = 0.6
            HEIGHT_GRASS_BARIER_END = 0.8

            TEMPERATURE_FOREST_BARIER_START = 0.8
            TEMPERATURE_FOREST_BARIER_END = 0.9
            TEMPERATURE_GRASS_BARIER_START = 0.85
            TEMPERATURE_GRASS_BARIER_END = 0.95

            WETNESS_FOREST_BARIER_START = 0.3
            WETNESS_FOREST_BARIER_END = 0.1
            WETNESS_GRASS_BARIER_START = 0.15
            WETNESS_GRASS_BARIER_END = 0.025

            FOREST_BORDER = 0.2
            GRASS_BORDER = 0.1

            SPAWN_PROBABILITY = 0.01

        class WETNESS:
            STEP = 0.01
            POWER_PER_HEIGHT = -0.25
            POWER_PER_TEMPERATURE = -0.15
            POWER_PER_ATMOSPHERE = 0.5

        class WIND:
            BORDER_SPEED = 0.05
            DELTA = 3
            TEMPERATURE_SPEED = 5.0 /13.0 # PER 100% difference
            HEIGHT_SPEED = 2.5 /13.0 # PER 100% difference
