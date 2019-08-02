from enum import Enum, auto


class StatsType(Enum):
    """Enum class which contains stats' types"""
    HP = auto()
    Atk = auto()
    Def = auto()
    Spa = auto()
    Spd = auto()
    Spe = auto()
    Accuracy = auto()
    Evasion = auto()