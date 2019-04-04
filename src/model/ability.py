from src.model.stats import StatsType

from abc import ABC
from enum import Enum, auto

class ActCondition(Enum):
    HPFULL = auto()
    STAB = auto()
    ONSWITCHIN = auto()
    ONSWITCHOUT = auto()



class Activation():

    conditions = {
        ActCondition.HPFULL: (lambda pokemon: pokemon.stats.currentHp() == pokemon.stats.baseStats[StatsType.HP]),
        ActCondition.STAB: (lambda pokemon, move: move.moveType in pokemon.types) 
    }




class Ability(ABC):

    def __init__(self, name:str):
        self.name = name
