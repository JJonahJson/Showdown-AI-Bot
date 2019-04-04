from src.model.stats import StatsType
from src.model.field import Weather
from src.model.pokemon import Pokemon

from abc import ABC, abstractmethod
from enum import Enum, auto

class ActCondition(Enum):
    HPFULL = auto()
    STAB = auto()
    ONSWITCHIN = auto()
    ONSWITCHOUT = auto()


class Activation():

    conditions = {
        ActCondition.HPFULL: (lambda pokemon: pokemon.stats.currentHp() == pokemon.stats.baseStats[StatsType.HP]),
        ActCondition.STAB: (lambda pokemon, move: move.moveType in pokemon.types), 
    }

class Ability(ABC):

    def __init__(self, name:str):
        self.name = name

    @abstractmethod
    def activateOnField(self, field):
        pass

    @abstractmethod
    def activateOnPokemon(self, pokemon):
        pass

class WeatherAbility(Ability):

    def __init__(self, name:str, weather:Weather):
        super().__init__(name)
        self.weather = weather

    def activateOnField(self, field):
        # TODO add battlefield parameter
        if Activation.conditions[ActCondition.ONSWITCHIN]:
            pass # TODO Set Weather

class DamageReductionAbility(Ability):

    def __init__(self, name:str, condition:ActCondition,reduction:int):
        super().__init__(name)
        self.reduction = reduction
        self.condition = condition
    
    def activateOnPokemon(self, pokemon):
        if Activation.conditions[self.condition](pokemon):
            pokemon.damageInputMultiplier = (self.reduction / 100)
        else:
            pokemon.damageInputMultiplier = 1

                