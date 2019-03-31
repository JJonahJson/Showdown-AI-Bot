from abc import ABC, abstractmethod
from pokemon import Pokemon
from stats import StatsType
from pokemontype import PokemonType

"""Abstract class that represents a generic item in game.
    Args:
    name (str): Name of the item
"""
class Item(ABC):

    def __init__(self, name):
        self.name = name
  
    """Abstract method used to implement the effect of the item
    """
    @abstractmethod
    def addEffect(self, pokemon:Pokemon):
        pass

    """Abstract method used to remove the effect of the item
    """
    @abstractmethod
    def removeEffect(self, pokemon:Pokemon):
        pass

"""Class used to represent an item that affect the stats of a pokemon
    Args:
    name (str): name of the item
    statsType (StatsType): the stat that it affects
    value (float): Multiplier of the stat
"""
class StatsItem(Item):

    def __init__(self, name, statsType:StatsType, value:float):
        Item.__init__(self, name)
        self.statsType = statsType
        self.value = value
    
    def addEffect(self, pokemon:Pokemon):
        pokemon.stats.addVolitileMul(self.statsType, self.value)
    
    def removeEffect(self, pokemon:Pokemon):
        pokemon.stats.removeVolitileMul(self.statsType, self.value)

"""Class used to represent items that affect a particular move type of a pokemon
    Args:
    name (str): name of the item
    moveType (PokemonType): Type of the move.
    value (float): Multiplier of the move

"""
class MoveItem(Item):
    
    def __init__(self, name, moveType:PokemonType, value:float):
        Item.__init__(self, name)
        self.moveType = moveType
        self.value = value
    
    def addEffect(self, pokemon:Pokemon):
        for move in pokemon.moves:
            if move.moveType is self.moveType:
                move.moveType.addPowerMultiply(self.value)
    
    def removeEffect(self, pokemon:Pokemon):
        for move in pokemon.moves:
            if move.moveType is self.moveType:
                move.moveType.removePowerMultiply(self.value)

""" Class that represents an item that modifies the total output damage of a pokemon
    Args:
    name (str): name of the item
    value (float): multiplier of the damname (str): name of the itemage
"""
class DamageItem(Item):

    def __init__(self, name, value:float):
        Item.__init__(self, name)
        self.value = value

    def addEffect(self, pokemon:Pokemon):
        pokemon.damageOutputMultiplier = pokemon.damageOutputMultiplier * self.value

    def removeEffect(self, pokemon:Pokemon):
        pokemon.damageOutputMultiplier = pokemon.damageOutputMultiplier * self.value
