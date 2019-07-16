from src.model.field import Weather, Field
from src.model.moves.secondaryeffect import SecondaryEffect
from src.model.field import BattleField
from src.model.stats import Stats

from abc import ABC, abstractmethod
from enum import Enum, auto


class ActCondition(Enum):
    HPFULL = auto()
    STAB = auto()
    ONSWITCHIN = auto()
    ONSWITCHOUT = auto()


class Ability(ABC):
    """
    Generic Ability
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def activate(self, field, side: int):
        pass


class DebuffEnemyAbility(Ability):
    """Ability that debuffs a stat of the enemy
    """

    def __init__(self, name: str, secondary_effect: SecondaryEffect):
        super().__init__(name)
        self.secondary_effect = secondary_effect

    def activate(self, field: BattleField, side: int):
        if side == 1:
            for pokemon in field.active_pokemon_side2.items():
                pokemon.stats.mul_stats[self.secondary_effect.stat] += self.secondary_effect.value
        else:
            for pokemon in field.active_pokemon_side1.items():
                pokemon.stats.mul_stats[self.secondary_effect.stat] += self.secondary_effect.value


class WeatherAbility(Ability):
    """
    Ability that affects the current weather
    """

    def __init__(self, name: str, weather: Weather):
        super().__init__(name)
        self.weather = weather

    def activate(self, field: BattleField, side: int):
        field.weather = self.weather


class FieldAbility(Ability):
    """
    Ability that affects the current field.
    """

    def __init__(self, name: str, field_type: Field):
        self.name = name
        self.field = field_type

    def activate(self, field: BattleField, side: int):
        field.field = self.field
