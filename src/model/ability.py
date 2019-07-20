from src.model.field import Weather, Field
from src.model.stats import StatsType
from src.model.field import BattleFieldSingle

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


class BuffUserAbility(Ability):
    """Ability that buffs a stat of the user
    """

    def __init__(self, name: str, stat: StatsType, value: int):
        super().__init__(name)
        self.stat = stat
        self.value = value

    def activate(self, field: BattleFieldSingle, side: int):
        field.active_selector_side[side].stats.volatile_mul[self.stat] *= self.value


class DebuffEnemyAbility(Ability):
    """Ability that debuffs a stat of the enemy
    """

    def __init__(self, name: str, stat: StatsType, value: int):
        super().__init__(name)
        self.stat = stat
        self.value = value

    def activate(self, field: BattleFieldSingle, side: int):
        field.active_selector_side[side].stats.mul_stats[self.stat] += self.value


class WeatherAbility(Ability):
    """
    Ability that affects the current weather
    """

    def __init__(self, name: str, weather: Weather):
        super().__init__(name)
        self.weather = weather

    def activate(self, field: BattleFieldSingle, side: int):
        field.weather = self.weather


class FieldAbility(Ability):
    """
    Ability that affects the current field.
    """

    def __init__(self, name: str, field_type: Field):
        self.name = name
        self.field_type = field_type

    def activate(self, field: BattleFieldSingle, side: int):
        field.field = self.field_type
