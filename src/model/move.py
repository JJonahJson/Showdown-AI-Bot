import copy
import random
from abc import ABC, abstractmethod

from model.damage_calculator import DamageCalculator
from model.move_type import MoveStatus
from model.status import Status


class Move(ABC):
    """
    This class represents a move of a pokemon
    Args:
        move_name (str): The name of the move
        accuracy (int) or (bool): The accuracy of the move, if true the move is secured to hit.
        base_power (int): The base power of the move
        category (str): Physical if the move is a physical move or special if is a special one
        pp (int): Power points of a move
        priority (int): The level of move's priority
        is_Z (bool): If the move is Z
        crit_ratio (int): Critical ratio of the move
        target (str): Which targets are possible by the move
        move_type (PokemonType): Type of the move
        on_user_stats: stat of the user modified by the move
        on_target_stats: stat of the opponent modified by the move
        power_multiply (int): Used for the items that enhance the damage of a move
        is_locked (boolean): if the move is locked or not
        chance: probability that the change of the stat or of the status occurs
        volatile_status: volatile_status added by the move
        non_volatile_status: non_volatile_status added by the move
        is_usable = a move is not usable if the pp are over or the move is blocked
        #TODO forse bisogna aggiungere una distinzione tra status on user e on target

    """

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category, pp: int, priority: int,
                 is_Z: bool, crit_ratio: int, move_type, scale_with, on_user_stats,
                 on_target_stats, defends_on, chance: int, volatile_status, non_volatile_status):

        self.move_name = move_name
        self.accuracy = accuracy
        self.base_power = base_power
        self.category = category
        self.scale_with = scale_with
        self.pp = pp
        self.priority = priority
        self.is_Z = is_Z
        self.crit_ratio = crit_ratio
        self.move_type = move_type
        self.on_user_stats = on_user_stats
        self.on_target_stats = on_target_stats
        self.moveStatus = MoveStatus.Available
        self.power_multiply = 1
        self.is_usable = True
        self.is_locked = False

        if defends_on:
            self.defends_on = self.scale_with
        else:
            self.defends_on = defends_on

        self.chance = chance
        self.volatile_status = volatile_status
        self.non_volatile_status = non_volatile_status

    @abstractmethod
    def invoke_move(self, caster_pokemon, target_pokemon, weather, field):
        """
        Args:
        caster_pokemon(Pokemon): the pokemon that does the move
        targetPokemon(Pokemon): the pokemon hit by the move

        """
        pass

    def calculate_base_power(self, types):
        stab = 1
        if self.move_type in types:
            stab = 1.5
        return self.base_power * stab

    def __lt__(self, other_move):
        return self.priority > other_move.priority

    def __eq__(self, other_move):
        return self.move_name.lower().replace(" ", "").replace("'", "") == other_move.move_name

    def add_power_multiply(self, value: float):
        self.power_multiply = self.power_multiply * value

    def remove_power_multiply(self, value: float):
        self.power_multiply = self.power_multiply / value

    def __repr__(self):
        return self.move_name


class SingleMove(Move):
    """
    Subclass of the Move class.
    It represents a move with only one target.

    """

    def __init__(self, move_name: str, accuracy: int,
                 base_power: int, category, pp: int, priority: int,
                 is_Z: bool, crit_ratio: int, move_type,
                 scale_with, on_user_stats,
                 on_target_stats, defends_on, chance: int, volatile_status, non_volatile_status):

        super().__init__(move_name, accuracy,
                         base_power, category, pp, priority,
                         is_Z, crit_ratio, move_type, scale_with,
                         on_user_stats, on_target_stats, defends_on, chance, volatile_status, non_volatile_status)

    def invoke_move(self, caster_pokemon, target_pokemon, weather, field):
        damage = DamageCalculator.calculate(weather, field, caster_pokemon, self, target_pokemon)
        target_pokemon.stats.decrease_hp(target_pokemon.stats.get_actual_hp()-damage)
        self.pp -= 1

        if random.randint(0, 100) <= self.chance:

            for tupla in self.on_user_stats:
                caster_pokemon.stats.modify(tupla[0], tupla[1])

            for tupla in self.on_target_stats:
                target_pokemon.stats.modify(tupla[0], tupla[1])
            if self.volatile_status:
                if self.volatile_status[1]:
                    if self.volatile_status[0] == 'self':
                        Status.add_volatile_status(self.volatile_status[1], caster_pokemon)
                    else:
                        Status.add_volatile_status(self.volatile_status[1], target_pokemon)

            if self.non_volatile_status:
                if self.non_volatile_status[1]:
                    if self.non_volatile_status[0] == 'self':
                        Status.apply_non_volatile_status(self.non_volatile_status[1], caster_pokemon)
                    else:
                        Status.apply_non_volatile_status(self.non_volatile_status[1], target_pokemon)

    def deepcopy(self):
        return SingleMove(self.move_name, self.accuracy, self.base_power, self.category, self.pp, self.priority,
                          self.is_Z, self.crit_ratio, self.move_type, self.scale_with, copy.deepcopy(
                self.on_user_stats), copy.deepcopy(self.on_target_stats), self.defends_on, self.chance,
                          self.volatile_status, self.non_volatile_status)
