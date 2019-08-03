from typing import Dict

from model.item import Item
from model.stats_type import StatsType
from model.status import StatusType, Status


class Pokemon:
    """
    This class represents a Pokémon.
    name (str) = pokemon's name
    types (list) = pokemon's types (or type)
    gender( str) = pokemon's gender (male, female or neutral)
    stats (Stats) = actual pokemon's statistics
    abilities (list) = list of possible pokemon's abilities
    weight (float) = pokemon's weight which may influence some moves power
    nonVolatileStatus(StatusType) = pokemon's status (poisoned, fainted, ecc.)
    volatileStatus(list) = pokemon's list of volatile Status (confused, attracted, ecc.)
    item(Item) = pokemon's held item
    level(int) = pokemon's level (from 1 to 100)
    moves(list) = pokemon's moves

    """

    def __init__(self, name: str, types: list, gender: str, stats, moves: Dict, abilities: list, weight: float,
                 non_volatile_status, volatile_status: list, item: Item, level: int, possible_moves={}):
        self.name = name
        self.types = types
        self.gender = gender
        self.stats = stats
        self.abilities = abilities
        self.weight = weight
        self.non_volatile_status = non_volatile_status
        self.volatile_status = volatile_status
        self.item = item
        self.level = level
        self.moves = moves
        self.damage_output_multiplier = 1
        self.damage_input_multiplier = 1
        self.bad_poison_turn = 0
        self.blocked = False
        self.can_mega = False
        self.possible_moves = possible_moves

    def get_usable_moves(self):
        """Methods that returns all usable moves"""
        return {key: self.moves[key] for key in self.moves if self.moves[key].is_usable and self.moves[key].pp != 0}

    def use_move(self, move_index: int, target, weather, field):
        """Methods that apply a move"""
        if move_index < 5:
            self.moves[move_index].invoke_move(self, target, weather, field)
            if target.stats.get_actual_hp() <= 0:
                Status.apply_non_volatile_status(StatusType.Fnt, target)
        else:
            self.possible_moves[move_index].invoke_move(self, target, weather, field)
            if target.stats.get_actual_hp() <= 0:
                Status.apply_non_volatile_status(StatusType.Fnt, target)

    def __repr__(self):
        return self.name

    def to_string(self):
        """Method used to pretty print a pokemon
        :return: string
        """
        return "BOT POKEMON:\n{}, L{}, {}\nHP:{} ATK:{} DEF:{} SPA:{} SPD:{} SPE:{}\nMOVES:{}".format(
            self.name,
            str(self.level),
            self.non_volatile_status,
            self.stats.get_actual_hp(),
            self.stats.get_actual(
                StatsType.Atk),
            self.stats.get_actual(
                StatsType.Def),
            self.stats.get_actual(
                StatsType.Spa),
            self.stats.get_actual(
                StatsType.Spd),
            self.stats.get_actual(
                StatsType.Spe),
            list(map(lambda x: x[1],
                     self.moves.items())))

    def oppo_to_string(self):
        return "OPPONENT:\n{}, L{}, {}\nHP:{} ATK:{} DEF:{} SPA:{} SPD:{} SPE:{}\nMOVES:{}\nPOSSIBLE MOVES:{}".format(
            self.name,
            str(self.level),
            self.non_volatile_status,
            self.stats.get_actual_hp(),
            self.stats.get_actual(
                StatsType.Atk),
            self.stats.get_actual(
                StatsType.Def),
            self.stats.get_actual(
                StatsType.Spa),
            self.stats.get_actual(
                StatsType.Spd),
            self.stats.get_actual(
                StatsType.Spe),
            list(map(lambda x: x[1], self.moves.items())),
            list(map(lambda x: x[1], self.possible_moves.items())))

    def deepcopy(self):
        new_moves = {}
        for move in self.moves:
            new_moves[move] = self.moves[move].deepcopy()
        return Pokemon(self.name, self.types, self.gender, self.stats.deepcopy(), new_moves, self.abilities,
                       self.weight,
                       self.non_volatile_status, self.volatile_status, self.item, self.level, self.possible_moves)

    def __eq__(self, other_pokemon):
        return self.name == other_pokemon.name
