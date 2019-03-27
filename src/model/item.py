from abc import ABC
from pokemon import Pokemon
from stats import StatsType
from pokemontype import PokemonType

class Item(ABC):

    def __init__(self, name):
        self.name = name

    
    def effect(self, pokemon:Pokemon):
        pass

    def removeEffect(self, pokemon:Pokemon):
        pass

class StatsItem(Item):

    def __init__(self, name, statsType:StatsType, value:int):
        Item.__init__(self, name)
        self.statsType = statsType
        self.value = value
    

    def effect(self, pokemon:Pokemon):
        pokemon.stats.addVolitileMul(self.statsType, self.value)
    
    def removeEffect(self, pokemon:Pokemon):
        pokemon.stats.removeVolitileMul(self.statsType, self.value)


class MoveItem(Item):
    
    def __init__(self, name, moveType:PokemonType, value:float):
        Item.__init__(self, name)
        self.moveType = moveType
        self.value = value
    
    def effect(self, pokemon:Pokemon):
        for move in pokemon.moves:
            if move.moveType is self.moveType:
                move.moveType.addPowerMultiply(self.value)
    
    def removeEffect(self, pokemon:Pokemon):
        for move in pokemon.moves:
            if move.moveType is self.moveType:
                move.moveType.removePowerMultiply(self.value)