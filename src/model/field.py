from src.model.stats import StatsType

from enum import Enum, auto
from typing import Dict

"""Enum for the possible weathers in game
"""
class Weather(Enum):
    Rain = auto()
    Sun = auto()
    Wind = auto()
    Hail = auto()
    Sandstorm = auto()
    Normal = auto()

"""Enum for the possible fields in game
"""
class Field(Enum):
    Electric = auto()
    Psychic = auto()
    Grass = auto()
    Misty = auto()
    Normal = auto()

"""Represents a battle field
"""
class BattleField():

    def __init__(self, active1,active2,inactive1,inactive2):
        self.weather = Weather.Normal
        self.field = Field.Normal
        #TODO TERRAIN
        self.terrain = None
        self.inactivePokemonSide1 = inactive1
        self.inactivePokemonSide2 = inactive2
        self.activePokemonSide1 = active1
        self.activePokemonSide2 = active2
        self.teoreticalOrder = lambda active1,active2: sorted(list(active1)+list(active2), key=lambda pokemon: pokemon.stats[StatsType.Speed])

    
    """Method for switch in a pokemon
    """
    def switchPokemon(self, player:int, indexIn:int, indexOut:int):
        if player == 1:
            # Reset Buffs
            for statType in StatsType:
                self.activePokemonSide1[indexOut].stats.mulStats[statType] = 0
            self.activePokemonSide1[indexOut], self.inactivePokemonSide1[indexIn] = self.inactivePokemonSide1[indexIn], self.activePokemonSide1[indexOut]
        else:
            for statType in StatsType:
                self.activePokemonSide1[indexOut].stats.mulStats[statType] = 0
            self.activePokemonSide2[indexOut], self.inactivePokemonSide2[indexIn] = self.inactivePokemonSide2[indexIn], self.activePokemonSide2[indexOut]

    """Method to execute a move
    """
    def doMove(self, player:int, pkmnCIndex:int, moveIndex:int, pkmnTIndex:int):
        if player == 1:
            self.activePokemonSide1[pkmnCIndex].doMove(moveIndex, self.activePokemonSide2, pkmnTIndex, self.weather)
        else:
            self.activePokemonSide2[pkmnCIndex].doMove(moveIndex, self.activePokemonSide1, pkmnTIndex, self.weather)

