from enum import Enum, auto


class SpeedCriterion(Enum):
    Normal = False
    TrickRoom = True


class Weather(Enum):
    """Enum for the possible weathers in game"""
    Raindance = auto()
    Sunnyday = auto()
    Wind = auto()
    Hail = auto()
    Sandstorm = auto()
    Normal = auto()

    # TODO: Primordial and desolate multipliers needs to be reworked


class Field(Enum):
    """Enum for the possible fields in game"""
    Electric = auto()
    Psychic = auto()
    Grass = auto()
    Misty = auto()
    Normal = auto()


