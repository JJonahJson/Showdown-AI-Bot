from src.model.stats import StatsType
from abc import ABC, abstractmethod

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
    def addEffect(self, pokemon):
        pass

    """Abstract method used to remove the effect of the item
    """
    @abstractmethod
    def removeEffect(self, pokemon):
        pass

    """Abstract method for locking a pokemon on a move
    """
    @abstractmethod
    def addLock(self, pokemon, move):
        pass

    """Abstract method for removing a lock from pokemon's moves
    """
    @abstractmethod
    def removeLock(self, pokemon, move):
        pass

    """Abstract method for the berry item
    """
    @abstractmethod
    def activate(self, pokemon):
        pass


"""Class used to represent an item that affect the stats of a pokemon
    Args:
    name (str): name of the item
    statsType (StatsType): the stat that it affects
    value (float): Multiplier of the stat
"""
class StatsItem(Item):

    def __init__(self, name, statsType, value:float):
        super().__init__(self, name)
        self.statsType = statsType
        self.value = value
    
    def addEffect(self, pokemon):
        pokemon.stats.addVolitileMul(self.statsType, self.value)
    
    def removeEffect(self, pokemon):
        pokemon.stats.removeVolitileMul(self.statsType, self.value)

"""Class used to represent items that affect a particular move type of a pokemon
    Args:
    name (str): name of the item
    moveType (PokemonType): Type of the move.
    value (float): Multiplier of the move

"""
class MoveItem(Item):
    
    def __init__(self, name, moveType, value:float):
        super().__init__(self, name)
        self.moveType = moveType
        self.value = value
    
    def addEffect(self, pokemon):
        for move in pokemon.moves:
            if move.moveType is self.moveType:
                move.moveType.addPowerMultiply(self.value)
    
    def removeEffect(self, pokemon):
        for move in pokemon.moves:
            if move.moveType is self.moveType:
                move.moveType.removePowerMultiply(self.value)

"""Class that represents an item that modifies the total output damage of a pokemon
    Args:
    name (str): name of the item
    value (float): multiplier of the damname (str): name of the itemage
"""
class DamageItem(Item):

    def __init__(self, name, value:float):
        super().__init__(self, name)
        self.value = value

    def addEffect(self, pokemon):
        pokemon.damageOutputMultiplier = pokemon.damageOutputMultiplier * self.value

    def removeEffect(self, pokemon):
        pokemon.damageOutputMultiplier = pokemon.damageOutputMultiplier * self.value

"""Class that represents a choice item
    Args:
    name (str): name of the item
    statsType (StatsType): the stat that it affects
    value (float): Multiplier of the stat
"""
class ChoiceItem(StatsItem):

    def __init__(self, name, stats, value:float):
        super().__init__(name, stats, value)
    


    def addLock(self, pokemon, move):
        for toLock in pokemon.moves:
            if toLock != move:
                toLock.isUsable = False
    


    def removeLock(self, pokemon, move):
        for toLock in pokemon.moves:
            toLock.isUsable = True

"""Class that represents a berry that heals when the hp go beyond a threshold
"""
class HealingBerry(Item):

    """Args:
        name (str): name of the berry
        threshold(int): % of the hp that activate the berry
        value(int): % of the base health to restore
    """
    def __init__(self, name:str, threshold:int, value:int):
        super().__init__(name)
        self.threshold = threshold
        self.value = value

    def activate(self, pokemon):
        # If under the threshold then activate
        if pokemon.stats.getActualHP() <= (pokemon.stats.baseStats[StatsType.HP] * (self.threshold / 100)):
            pokemon.stats.increaseHP(pokemon.stats.baseStats[StatsType.HP] * (self.value / 100))
            
