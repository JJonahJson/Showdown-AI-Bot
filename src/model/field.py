from src.model.stats import StatsType

from enum import Enum, auto
from typing import Dict

class Weather(Enum):
    """Enum for the possible weathers in game"""
    Rain = auto()
    Sun = auto()
    Wind = auto()
    Hail = auto()
    Sandstorm = auto()
    Normal = auto()

class Field(Enum):
    """Enum for the possible fields in game"""
    Electric = auto()
    Psychic = auto()
    Grass = auto()
    Misty = auto()
    Normal = auto()

class SpeedCriterion(Enum):
    Normal = False
    TrickRoom = True

class BattleField():
    """Represents a battle field"""

    def __init__(self, active1,active2,inactive1,inactive2):
        self.weather = Weather.Normal
        self.field = Field.Normal
        self.speedControl = SpeedCriterion.Normal
        self.inactivePokemonSide1 = inactive1
        self.inactivePokemonSide2 = inactive2
        self.activePokemonSide1 = active1
        self.activePokemonSide2 = active2
    
    def switchPokemon(self, player:int, indexIn:int, indexOut:int):
        """Method for switch in a pokemon"""
        if player == 1:
            # Reset Buffs
            for statType in StatsType:
                self.activePokemonSide1[indexOut].stats.mulStats[statType] = 0
            self.activePokemonSide1[indexOut], self.inactivePokemonSide1[indexIn] = self.inactivePokemonSide1[indexIn], self.activePokemonSide1[indexOut]
        else:
            for statType in StatsType:
                self.activePokemonSide1[indexOut].stats.mulStats[statType] = 0
            self.activePokemonSide2[indexOut], self.inactivePokemonSide2[indexIn] = self.inactivePokemonSide2[indexIn], self.activePokemonSide2[indexOut]

    def doMove(self, player:int, pkmnCIndex:int, moveIndex:int, pkmnTIndex:int):
        """Method to execute a move"""
        if player == 1:
            self.activePokemonSide1[pkmnCIndex].doMove(moveIndex, self.activePokemonSide2, pkmnTIndex, self.weather)
        else:
            self.activePokemonSide2[pkmnCIndex].doMove(moveIndex, self.activePokemonSide1, pkmnTIndex, self.weather)

