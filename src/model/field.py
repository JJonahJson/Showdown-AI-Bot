from abc import ABC, abstractmethod
from enum import Enum, auto

from src.model.pokemon import Pokemon


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


class BattleField(ABC):
    """BattleField superclass"""

    def __init__(self):
        self.weather = Weather.Normal
        self.field = Field.Normal
        self.speed_control = SpeedCriterion.Normal

    @abstractmethod
    def switch_pokemon(self, player: int, pokemon_in: int, pokemon_out: int):
        pass

    @abstractmethod
    def do_move(self, player: int, pokemon_caster: int, move_index: int, pokemon_target: int):
        pass


class BattleFieldSingle(BattleField):
    """Represents a battle field for a battle in single"""

    def __init__(self, active_pokemon_bot: Pokemon, active_pokemon_oppo: Pokemon, bench_bot: list, bench_oppo: list):
        """ Constructor method
        :param active_pokemon_bot: active pokemon of the bot
        :param active_pokemon_oppo: active pokemon of the opponenent
        :param bench_bot: list of pokemons in the bench
        :param bench_oppo: list of pokemons in the bench
        """
        super().__init__()
        self.active_pokemon_bot = active_pokemon_bot
        self.active_pokemon_oppo = active_pokemon_oppo
        self.bench_bot = bench_bot
        self.bench_oppo = bench_oppo

    def do_move(self, player: int, pokemon_caster: int, move_index: int, pokemon_target):
        """Apply move to the target
        :param player: player id
        :param pokemon_caster:
        :param move_index: Index of the move
        :param pokemon_target: Target
        :return:
        """
        if player == 1:
            self.active_pokemon_bot.use_move(move_index, self.active_pokemon_oppo,
                                             self.weather, self.field)
        else:
            self.active_pokemon_oppo.use_move(move_index, self.active_pokemon_bot,
                                              self.weather, self.field)

    def switch_pokemon(self, player: int, pokemon_in: int, pokemon_out: int):
        """Switch pokemon
        :param player:
        :param pokemon_in: Not used
        :param pokemon_out: Index of the pokemon to remove
        :return:
        """
        if player == 1:
            to_replace = self.active_pokemon_bot
            self.active_pokemon_bot = self.bench_bot[pokemon_in - 1]
            self.bench_bot[pokemon_in - 1] = to_replace
        else:
            to_replace = self.active_pokemon_oppo
            self.active_pokemon_oppo = self.bench_oppo[pokemon_in - 1]
            self.bench_oppo[pokemon_in - 1] = to_replace
