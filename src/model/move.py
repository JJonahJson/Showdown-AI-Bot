from src.model.damagecalculator import DamageCalculator
from src.model.status import Status
from abc import ABC, abstractmethod
from enum import Enum, auto
import random


class MoveCategory(Enum):
    Status = auto()
    Damage = auto()


class MoveStatus(Enum):
    Locked = auto()
    Available = auto()


class Move(ABC):
    """
    This class represents a move of a pokemon
    Args:
        move_name (str): The name of the move
        accuracy (int) or (bool): The accuracy of the move, if true the move is secured to hit.
        base_power (int): The base power of the move
        category (str): Physical if the move is a physical move or special if is a special one
        pp (int): Power points of a move
        priority (int): The level of move's priority
        is_Z (bool): If the move is Z
        crit_ratio (int): Critical ratio of the move
        target (str): Which targets are possible by the move
        move_type (PokemonType): Type of the move
        on_user (SecondaryEffect): SecondaryEffect of the move
        on_target (SecondaryEffect): SecondaryEffect of the move
        power_multiply (int): Used for the items that enhance the damage of a move
        is_locked (boolean): if the move is locked or not

    """

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category, pp: int, priority: int,
                 is_Z: bool, crit_ratio: int, move_type, scale_with, on_user_stats,
                 on_target_stats, defends_on, chance: int, volatile_status, non_volatile_status):

        self.move_name = move_name
        self.accuracy = accuracy
        self.base_power = base_power
        self.category = category
        self.scale_with = scale_with
        self.pp = pp
        self.priority = priority
        self.is_Z = is_Z
        self.crit_ratio = crit_ratio
        self.move_type = move_type
        self.on_user_stats = on_user_stats
        self.on_target_stats = on_target_stats
        self.moveStatus = MoveStatus.Available
        self.power_multiply = 1
        self.isUsable = True

        if defends_on:
            self.defends_on = self.scale_with
        else:
            self.defends_on = defends_on

        self.chance = chance
        self.volatile_status = volatile_status
        self.non_volatile_status = non_volatile_status


    @abstractmethod
    def invoke_move(self, caster_pokemon, target_pokemon, weather, field):
        """
        Args:
        caster_pokemon(Pokemon): the pokemon that does the move
        targetPokemon(Pokemon): the pokemon hit by the move

        """
        pass

    def calculate_base_power(self, types):
        stab = 1
        if self.move.move_type in types:
            stab = 1.5
        return self.move.base_power*stab


    def __lt__(self, other_move):
        return self.priority > other_move.priority

    def calculate_base_power(self):
        return self.base_power * self.power_multiply

    def add_power_multiply(self, value: float):
        self.power_multiply = self.power_multiply * value

    def remove_power_multiply(self, value: float):
        self.power_multiply = self.power_multiply / value


class SingleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with only one target.

    """

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category: str, pp: int, priority: int,
                 is_Z: bool, crit_ratio: int, move_type,
                 scale_with, on_user,
                 on_target, defends_on, chance: int, volatile_status, non_volatile_status):

        super().__init__(move_name, accuracy,
                         base_power, category, pp, priority,
                         is_Z, crit_ratio, move_type, scale_with,
                         on_user, on_target, defends_on, chance, volatile_status, non_volatile_status)

    def invoke_move(self, caster_pokemon, target_pokemon, weather, field):
        damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, target_pokemon)
        target_pokemon.stats.decrease_hp(damage)
        self.pp -= 1

        if random.randint(0,100) <= self.chance:

            for tupla in self.on_user_stats:
                caster_pokemon.stats.modify(tupla[0], tupla[1])

            for tupla in self.on_target_stats:
                target_pokemon.stats.modify(tupla[0], tupla[1])

            if self.volatile_status[1]:
                if self.volatile_status[0] == 'self':
                    Status.add_volatile_status(self.volatile_status[1], caster_pokemon)
                else:
                    Status.add_volatile_status(self.volatile_status[1], target_pokemon)

            if self.non_volatile_status[1]:
                if self.non_volatile_status[0] == 'self':
                    Status.apply_non_volatile_status(self.non_volatile_status[1], caster_pokemon)
                else:
                    Status.apply_non_volatile_status(self.non_volatile_status[1], target_pokemon)



