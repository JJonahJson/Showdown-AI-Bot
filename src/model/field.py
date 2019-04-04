from src.model.pokemon import Pokemon
from src.model.stats import StatsType

from enum import Enum, auto
from typing import Dict
from collections import OrderedDict

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

    def __init__(self):
        self.weather = Weather.Normal
        self.field = Field.Normal
        #TODO TERRAIN
        self.terrain = None
        self.activePokemonSide1 = {}
        self.activePokemonSide2 = {}
        self.inactivePokemonSide1 = {}
        self.inactivePokemonSide2 = {}
        self.teoreticalOrder = lambda active1,active2: sorted(active1+active2, key=lambda pokemon: pokemon.stats[StatsType.Speed])

    """Sets the leading pokemons
    """
    def setLeading(self, side1: Dict[Pokemon], side2:Dict[Pokemon]):
        self.activepokemonSide1 = side1
        self.activePokemonSide2 = side2

        for pokemon in self.teoreticalOrder(self.activePokemonSide1, self.activePokemonSide2):
            pokemon.ability.activateOnField(self)
            pass # TODO Activate SwitchIn-Ability in order to speed of pokemons

    """Sets the pokemon in the back
    """
    def setInactive(self, side1: Dict[Pokemon], side2: Dict[Pokemon]):
        self.inactivePokemonSide1 = side1
        self.inactivePokemonSide2 = side2
    
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

