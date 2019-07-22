from typing import Dict
from model.stats import StatsType, Stats
from model.status import StatusType, Status
from model.item import Item


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

    def __init__(self, name: str, types: list, gender: str, stats: Stats, moves: Dict, abilities: list, weight: float,
                 non_volatile_status: StatusType, volatile_status: list, item: Item, level: int):
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

    def get_usable_moves(self):
        """Methods that returns all usable moves"""
        return {key: value for key, value in self.moves if value.isUsable()}

    def use_move(self, move_index: int, target, weather, field):
        """Methods that apply a move"""
        self.moves[move_index].invoke_move(self, target, weather, field)
        if target.stats.get_actual_hp() <= 0:
            Status.apply_non_volatile_status(target, StatusType.Fnt)

    def __repr__(self):
        return self.name

    def __lt__(self, other_pokemon):
        """More speed"""
        return self.stats[StatsType.Spe] > other_pokemon.stats[StatsType.Spe]

    def __eq__(self, other_pokemon):
        return self.name == other_pokemon.name
