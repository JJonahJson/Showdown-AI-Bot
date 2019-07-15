from src.model.damagecalculator import DamageCalculator
from abc import ABC, abstractmethod
from typing import Union
from enum import Enum, auto
from random import random


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

    def __init__(self, moveName:str, accuracy:int,
                 basePower:int, category, pp:int, priority:int,
                 isZ:bool, critRatio:int, moveType,
                 moveCategory, scaleWith, onUser,
                 onTarget, defendsOn=None):

        self.moveName = moveName
        self.accuracy = accuracy
        self.basePower = basePower
        self.category = category
        self.scaleWith = scaleWith
        self.pp = pp
        self.priority = priority
        self.isZ = isZ
        self.critRatio = critRatio
        self.moveType = moveType
        self.onUser = onUser
        self.onTarget = onTarget
        self.moveStatus = MoveStatus.Available
        self.powerMultiply = 1
        self.isUsable = True

        if defendsOn :
            self.defendsOn = self.scaleWith
        else:
            self.defendsOn = defendsOn

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

    def addPowerMultiply(self, value:float):
        self.powerMultiply = self.powerMultiply * value

    def removePowerMultiply(self, value:float):
        self.powerMultiply = self.powerMultiply / value


class SingleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with only one target.

    """

    def __init__(self, moveName:str, accuracy:int,
                 basePower:int, category:str, pp:int, priority:int,
                 isZ:bool, critRatio:int, moveType,
                 scaleWith, onUser,
                 onTarget, defendsOn=None):

        super().__init__(self, moveName, accuracy,
                         basePower, category, pp, priority,
                         isZ, critRatio, moveType, scaleWith,
                         onUser, onTarget, defendsOn)

    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, target_pokemon)
        target_pokemon.stats.decrease_hp(damage)

        if self.onUser:
            caster_pokemon.stats.modify(self.onUser.stat, self.onUser.value)

        if self.onTarget:
            target_pokemon.stats.modify(self.onTarget.stat, self.onTarget.value)


class MultipleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with multiple targets.

    """

    def __init__(self, moveName:str, accuracy:int,
                 basePower:int, category:str, pp:int, priority:int,
                 isZ:bool, critRatio:int, moveType,
                 scaleWith, onUser,
                 onTarget, defendsOn=None):

        super().__init__(self, moveName, accuracy,
                         basePower, category, pp, priority,
                         isZ, critRatio, moveType, scaleWith,
                         onUser, onTarget, defendsOn)

    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        for targetPokemon in target_pokemon.items():
            damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, targetPokemon)
            targetPokemon.stats.decrease_hp(damage)

            if self.onUser:
                caster_pokemon.stats.modify(self.onUser.stat, self.onUser.value)

            if self.onTarget:
                targetPokemon.stats.modify(self.onTarget.stat, self.onTarget.value)


class StatusMove(SingleMove):

    def __init__(self, moveName:str, accuracy:int,
                 basePower:int, category:str, pp:int, priority:int,
                 isZ:bool, critRatio:int, moveType,
                 scaleWith, onUser, onTarget, status,defendsOn=None):

        super().__init__(self, moveName, accuracy,
                         basePower, category, pp, priority,
                         isZ, critRatio, moveType, scaleWith,
                         onUser, onTarget, defendsOn)
        self.status = status

    def invokeMove(self, caster_pokemon, target_pokemon, weather, field):
        damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, target_pokemon)
        target_pokemon.stats.decrease_hp(damage)

        if random() <= self.accuracy:
            target_pokemon.apply_status(self.status)



class MoveFactory:
    """Factory for the Move class hierarchy."""
    subclasses = {
        'single': SingleMove,
        'multiple': MultipleMove
    }

    @staticmethod
    def CreateMove(target:str,self, moveName:str, accuracy:int,
                   basePower:int, category:str, pp:int, priority:int,
                   isZ:bool, critRatio:int, moveType,
                   scaleWith, onUser,
                   onTarget, defendsOn=None) -> Union[SingleMove, MultipleMove]:

        return MoveFactory.subclasses[target](moveName,
                                              accuracy, basePower, category,
                                              pp, priority, isZ, critRatio, moveType, scaleWith,
                                              onUser, onTarget, defendsOn)
