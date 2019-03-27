from enum import Enum, auto

class Weather(Enum):
    Rain = auto()
    Sun = auto()
    Wind = auto()
    Hail = auto()
    Sandstorm = auto()
    Normal = auto()

class Field(Enum):
    Electric = auto()
    Psychic = auto()
    Grass = auto()
    Misty = auto()
    Normal = auto()
