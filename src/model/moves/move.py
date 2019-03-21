from abc import ABC, abstractmethod
from secondaryeffect import SecondaryEffect
from typing import Union

import sys
sys.path.append("..")

from pokemon import Pokemon


class Move(ABC):
    """This class represents a move of a pokemon
    Args:
        moveName (str): The name of the move
        accuracy (int) or (bool): The accuracy of the move, if true the move is secured to hit.
        basePower (int): The base power of the move
        category (str): Physical if the move is a physical move or special if is a special one
        pp (int): Power points of a move
        priority (int): The level of a priority of the move
        isZ (bool): If the move is Z
        critRatio (int): Critical ratio of the move
        target (str): Which targets are possble in the move
        moveType (str): Type of the move
        onUser (SecondaryEffect): SecondaryEffect of the move
        onTarget (SecondaryEffect): SecondaryEffect of the move
    """
    
    def __init__(self, moveName:str, accuracy:int, 
        basePower:int, category:str, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:str,
        onUser:SecondaryEffect, onTarget:SecondaryEffect):

        self.moveName = moveName
        self.accuracy = accuracy
        self.basePower = basePower
        self.category = category
        self.pp = pp
        self.priority = priority
        self.isZ = isZ
        self.critRatio = critRatio
        self.moveType = moveType
        self.onUser = onUser
        self.onTarget = onTarget
    
    """
    Args:
        casterPokemon(Pokemon): the pokemon that does the move
        targetPokemon(Pokemon): the pokemon who receives the move
    """
    @abstractmethod
    def invokeMove(self, casterPokemon: Pokemon, targetPokemon: Pokemon):
        pass


class SingleMove(Move):
    """Subclass of the Move class.
    It represents a move with only one target.
    """

    def __init__(self, moveName:str, accuracy:int, 
        basePower:int, category:str, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:str,
        onUser:SecondaryEffect, onTarget:SecondaryEffect):
        Move.__init__(self, moveName, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget)

    
    def invokeMove(self, casterPokemon:Pokemon, targetPokemon:Pokemon):

        # TODO Insert the damage the damage calculation that the move does
        # TODO Implement the move, when the merging with the pokemon model is done
        if self.onUser:
            casterPokemon.stats.modify(self.onUser.stat, self.onUser.value)

        if self.onTarget:
            targetPokemon.stats.modify(self.onTarget.stat, self.onTarget.value)
        
       


class MultipleMove(Move):
    """Subclass of the Move class.
    It represents a move with multiple targets.
    """

    def __init__(self, moveName:str, accuracy:int, 
        basePower:int, category:str, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:str,
        onUser:SecondaryEffect, onTarget:SecondaryEffect):
        Move.__init__(self, moveName, accuracy, 
        basePower, category, pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget)

    
    def invokeMove(self, targetPokemons, casterPokemons):
        # TODO Insert the damage the damage calculation that the move does
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
    def CreateMove(target:str, moveName:str, accuracy:int, 
        basePower:int, category:str, pp:int, priority:int,
        isZ:bool, critRatio:int, moveType:str,
        onUser:SecondaryEffect, onTarget:SecondaryEffect) -> Union[SingleMove, MultipleMove]:

        return MoveFactory.subclasses[target](moveName, 
        accuracy, basePower, category,
        pp, priority,
        isZ, critRatio, moveType,
        onUser, onTarget)
