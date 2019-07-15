from abc import ABC, abstractmethod
from enum import Enum, auto
from random import random
from typing import Union

from src.model.damagecalculator import DamageCalculator
from src.model.pokemontype import PokemonType as pk


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
        moveName (str): The name of the move
        accuracy (int) or (bool): The accuracy of the move, if true the move is secured to hit.
        basePower (int): The base power of the move
        category (str): Physical if the move is a physical move or special if is a special one
        pp (int): Power points of a move
        priority (int): The level of move's priority
        isZ (bool): If the move is Z
        critRatio (int): Critical ratio of the move
        target (str): Which targets are possible by the move
        moveType (PokemonType): Type of the move
        onUser (SecondaryEffect): SecondaryEffect of the move
        onTarget (SecondaryEffect): SecondaryEffect of the move
        powerMultiply (int): Used for the items that enhance the damage of a move
        isLocked (boolean): if the move is locked or not

    """

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category: MoveCategory, pp: int, priority: int,
                 isZ: bool, critRatio: int, move_type,
                 scale_with, on_user,
                 on_target, defends_on):

        self.moveName = move_name
        self.accuracy = accuracy
        self.basePower = base_power
        self.category = category
        self.scaleWith = scale_with
        self.pp = pp
        self.priority = priority
        self.isZ = isZ
        self.critRatio = critRatio
        self.moveType = move_type
        self.onUser = on_user
        self.onTarget = on_target
        self.moveStatus = MoveStatus.Available
        self.powerMultiply = 1
        self.isUsable = True
        self.defends_on = defends_on

    @abstractmethod
    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        """
        Args:
        casterPokemon(Pokemon): the pokemon that does the move
        targetPokemon(Pokemon): the pokemon hit by the move

        """
        pass

    def __lt__(self, otherMove):
        return self.priority > otherMove.priority

    def calculateBasePower(self):
        return self.basePower * self.powerMultiply

    def addPowerMultiply(self, value: float):
        self.powerMultiply = self.powerMultiply * value

    def removePowerMultiply(self, value: float):
        self.powerMultiply = self.powerMultiply / value


class SingleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with only one target.

    """

    def __init__(self, move_name, accuracy: int,
                 base_power: int, category: MoveCategory, pp: int, priority: int,
                 is_z, crit_ratio: int, move_type: pk,
                 scale_with: object, on_user: object,
                 on_target: object, defends_on: object = None) -> object:

        super().__init__(move_name, accuracy,
                         base_power, category, pp, priority,
                         is_z, crit_ratio, move_type, scale_with,
                         on_user, on_target, defends_on)

    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, target_pokemon)
        target_pokemon.stats.decrease_hp(damage)
        self.pp -= 1

        if self.onUser:
            caster_pokemon.stats.modify(self.onUser.stat, self.onUser.value)

        if self.onTarget:
            target_pokemon.stats.modify(self.onTarget.stat, self.onTarget.value)


class MultipleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with multiple targets.

    """

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category: MoveCategory, pp: int, priority: int,
                 isZ: bool, critRatio: int, move_type,
                 scale_with, on_user,
                 on_target, defends_on=None):

        super().__init__(move_name, accuracy,
                         base_power, category, pp, priority,
                         isZ, critRatio, move_type, scale_with,
                         on_user, on_target, defends_on)

    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        for targetPokemon in target_pokemon.items():
            self.pp -= 1
            damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, targetPokemon)
            targetPokemon.stats.decrease_hp(damage)

            if self.onUser:
                caster_pokemon.stats.modify(self.onUser.stat, self.onUser.value)

            if self.onTarget:
                targetPokemon.stats.modify(self.onTarget.stat, self.onTarget.value)


class StatusMove(SingleMove):

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category: str, pp: int, priority: int,
                 is_z: bool, crit_ratio: int, move_type,
                 scale_with, on_user, on_target, status, defends_on=None):
        super().__init__(self, move_name, accuracy,
                         base_power, category, pp, priority,
                         is_z, crit_ratio, move_type, scale_with,
                         on_user, on_target, defends_on)
        self.status = status

    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        self.pp -= 1
        damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, target_pokemon)
        target_pokemon.stats.decrease_hp(damage)

        if random() <= self.accuracy:
            target_pokemon.apply_status(self.status)


class MoveFactory:
    """Factory for the Move class hierarchy."""
    subclasses = {
        'single'  : SingleMove,
        'multiple': MultipleMove
    }

    @staticmethod
    def create_move(target: str, move_name: str, accuracy: int, base_power: int, category: str, pp: int, priority: int,
                    isZ: bool, crit_ratio: int, move_type, scale_with, on_user, on_target, defends_on=None) -> Union[
        SingleMove, MultipleMove]:
        return MoveFactory.subclasses[target](move_name,
                                              accuracy, base_power, category,
                                              pp, priority, isZ, crit_ratio, move_type, scale_with,
                                              on_user, on_target, defends_on)
