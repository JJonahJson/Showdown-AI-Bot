from src.model.stats import StatsType
from enum import Enum, auto


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

    def __init__(self, active1, active2, inactive1, inactive2):
        self.weather = Weather.Normal
        self.field = Field.Normal
        self.speedControl = SpeedCriterion.Normal
        self.inactivePokemonSide1 = inactive1
        self.inactivePokemonSide2 = inactive2
        self.activePokemonSide1 = active1
        self.activePokemonSide2 = active2
    
    def switch_pokemon(self, player: int, index_in: int, index_out: int):
        """Method for switch in a pokemon"""
        if player == 1:
            # Reset Buffs
            for statType in StatsType:
                self.activePokemonSide1[index_out].stats.mulStats[statType] = 0
            self.activePokemonSide1[index_out], self.inactivePokemonSide1[index_in] = self.inactivePokemonSide1[index_in], self.activePokemonSide1[index_out]
        else:
            for statType in StatsType:
                self.activePokemonSide1[index_out].stats.mulStats[statType] = 0
            self.activePokemonSide2[index_out], self.inactivePokemonSide2[index_in] = self.inactivePokemonSide2[index_in], self.activePokemonSide2[index_out]

    def do_move(self, player:int, pkmn_ci_ndex: int, move_index: int, pkmn_ti_ndex: int):
        """Method to execute a move"""
        if player == 1:
            self.activePokemonSide1[pkmn_ci_ndex].do_move(move_index, self.activePokemonSide2, pkmn_ti_ndex, self.weather)
        else:
            self.activePokemonSide2[pkmn_ci_ndex].do_move(move_index, self.activePokemonSide1, pkmn_ti_ndex, self.weather)

