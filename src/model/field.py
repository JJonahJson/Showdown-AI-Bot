from enum import Enum, auto

"""Enum for the possible weathers in game
"""
class Weather(Enum):
    Rain = auto()
    Sun = auto()
    Wind = auto()
    Hail = auto()
    Sandstorm = auto()
    Normal = auto()

"""Enum for the possible fields in game
"""
class Field(Enum):
    Electric = auto()
    Psychic = auto()
    Grass = auto()
    Misty = auto()
    Normal = auto()
