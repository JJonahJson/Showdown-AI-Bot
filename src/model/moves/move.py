from abc import ABC, abstractmethod
from moves.secondaryeffect import SecondaryEffect
from typing import Union
from enum import Enum, auto

from pokemon import Pokemon
from pokemontype import PokemonType
from stats import StatsType


class MoveCategory(Enum):
    Status = auto()
    Damage = auto()

class Move(ABC):
    """This class represents a move of a pokemon
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
    """
    
    def __init__(self, moveName:str, accuracy:int, 
        basePower:int, category:MoveCategory, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:PokemonType,
        moveCategory:Move, scaleWith:StatsType, onUser:SecondaryEffect,
        onTarget:SecondaryEffect, defendsOn:StatsType=None):

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
        self.powerMultiply = 1

        if defendsOn :
            self.defendsOn = self.scaleWith
        else:
            self.defendsOn = defendsOn
    
    """
    Args:
        casterPokemon(Pokemon): the pokemon that does the move
        targetPokemon(Pokemon): the pokemon hit by the move
    """
    @abstractmethod
    def invokeMove(self, casterPokemon: Pokemon, targetPokemon: Pokemon):
        pass

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
        isZ:bool, critRatio:int, moveType:PokemonType,
        scaleWith:StatsType, onUser:SecondaryEffect,
        onTarget:SecondaryEffect, defendsOn:StatsType=None):

        Move.__init__(self, moveName, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType, scaleWith,
        onUser, onTarget, defendsOn)

    
    def invokeMove(self, casterPokemon:Pokemon, targetPokemon:Pokemon):

        # TODO Insert the damage  calculation that the move does
        # TODO Implement the move, when the merging with the pokemon model is done
        if self.onUser:
            casterPokemon.stats.modify(self.onUser.stat, self.onUser.value)

        if self.onTarget:
            targetPokemon.stats.modify(self.onTarget.stat, self.onTarget.value)
        
       


class MultipleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with multiple targets.
    """

    def __init__(self, moveName:str, accuracy:int, 
        basePower:int, category:str, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:PokemonType,
        scaleWith:StatsType, onUser:SecondaryEffect,
        onTarget:SecondaryEffect, defendsOn:StatsType=None):

        Move.__init__(self, moveName, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType, scaleWith,
        onUser, onTarget, defendsOn)

    
    def invokeMove(self, targetPokemons, casterPokemons):
        # TODO Insert the damage calculation that the move does
        
        if self.onUser:
            for casterPokemon in casterPokemons:
                casterPokemon.stats.modify(self.onUser.stat, self.onUser.value)
        if self.onTarget:
            for targetPokemon in targetPokemons:
                targetPokemon.stats.modify(self.onTarget.stat, self.onTarget.value)


class MoveFactory:
    """Factory for the Move class hierarchy.
    """
    subclasses = {
        'single': SingleMove,
        'multiple': MultipleMove
    }

    @staticmethod
    def CreateMove(target:str,self, moveName:str, accuracy:int, 
        basePower:int, category:str, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:PokemonType,
        scaleWith:StatsType, onUser:SecondaryEffect,
        onTarget:SecondaryEffect, defendsOn:StatsType=None) -> Union[SingleMove, MultipleMove]:

        return MoveFactory.subclasses[target](moveName, 
        accuracy, basePower, category,
        pp, priority,isZ, critRatio, moveType, scaleWith,
        onUser, onTarget, defendsOn)
