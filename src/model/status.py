from enum import Enum, auto

from src.model.pokemontype import PokemonType
from src.model.stats import StatsType


class StatusType(Enum):
    """Class that represents all possible statuses of a pokemon"""
    Normal = auto(),
    Fainted = auto(),
    Psn = auto(),
    Tox = auto(),
    Brn = auto(),
    Par = auto(),
    Frz = auto(),
    Slp = auto(),
    Attract = auto(),
    Confusion = auto(),
    Trapped = auto(),
    Protect = auto(),
    Endure = auto(),
    Flinch = auto()


non_volatile = {
    StatusType.Normal: False,
    StatusType.Fainted: True,
    StatusType.Psn: True,
    StatusType.Tox: True,
    StatusType.Brn: True,
    StatusType.Par: True,
    StatusType.Frz: True,
    StatusType.Slp: True,

    StatusType.Attract: False,
    StatusType.Flinch: False,
    StatusType.Confusion: False,
    StatusType.Protect: False,
    StatusType.Trapped: False

}

immune = {
    StatusType.Psn: [PokemonType.Poison, PokemonType.Steel],
    StatusType.Tox: [PokemonType.Poison, PokemonType.Steel],
    StatusType.Par: [PokemonType.Electric],
    StatusType.Frz: [PokemonType.Ice],
    StatusType.Brn: [PokemonType.Fire],
    StatusType.Normal: [],
    StatusType.Fainted: [],
    StatusType.Attract: [],
    StatusType.Flinch: [],
    StatusType.Confusion: [],
    StatusType.Protect: [],
    StatusType.Trapped: [],
    StatusType.Endure: [],
    StatusType.Slp: []
}


class Status:
    """Utility class with static methods which modify status and relative stats"""

    @staticmethod
    def apply_non_volatile_status(status: StatusType, pokemon) -> bool:
        """
        Method which applies a non volatile status, used also to specify when fainted
        :param status:
        :param pokemon:
        :return: True if succeed, False instead
        """
        if not non_volatile[status]:
            return False
        for pkmn_type in pokemon.types:
            if pkmn_type in immune[status] or (pokemon.non_volatile_status is not StatusType.Normal and
                                               pokemon.non_volatile_status):
                return False
        pokemon.non_volatile_status = status
        if status in [StatusType.Psn, StatusType.Tox, StatusType.Brn]:
            return True
        if Status.apply_status_effect[status](pokemon):
            return True
        else:
            return False

    @staticmethod
    def remove_non_volatile_status(target):
        if target.non_volatile_status != StatusType.Normal:

            if target.non_volatile_status == StatusType.Fainted:
                return False

            if target.non_volatile_status in [StatusType.Slp, StatusType.Frz]:
                target.blocked = False

            if target.non_volatile_status == StatusType.Par:
                Status.remove_volatile_stat_mod(target, StatsType.Spe, 0.5)

            if target.non_volatile_status == StatusType.Tox:
                target.bad_poison_turn = 0

            target.non_volatile_status = StatusType.Normal
            return True
        else:
            return False

    @staticmethod
    def add_volatile_status(status: StatusType, pokemon):
        """Method which adds a volatile status to pokemon's volatile status list"""
        if non_volatile[status]:
            return False
        if status in pokemon.volatile_status:
            return False

        pokemon.volatile_status.append(status)
        return True

    @staticmethod
    def remove_volatile_status(status: StatusType, pokemon):
        """Method which removes a volatile status to pokemon's volatile status list"""
        try:
            pokemon.volatile_status.remove(status)
        except ValueError:
            pass

    @staticmethod
    def add_volatile_stat_mod(pokemon, stat_type: StatsType, value: float):
        """Method which adds changes to the specified volatile stat"""
        pokemon.stats.volatile_mul[stat_type] *= value

    @staticmethod
    def remove_volatile_stat_mod(pokemon, stat_type: StatsType, value: float):
        """Method which removes changes to the specified volatile stat"""
        pokemon.stats.volatile_mul[stat_type] /= value

    @staticmethod
    def decrease_hp(pokemon, percentage: float):
        """Method which decreases pokemon's hp based on a specified percentage"""
        pokemon.stats.damage += pokemon.stats.real_stats[StatsType.HP] * percentage

    @staticmethod
    def apply_infatuation(target, caster):
        if target.gender == caster.gender or target.gender == "Genderless":
            return False
        if Status.add_volatile_status(StatusType.Attract, target):
            return True

        return False

    @staticmethod
    def apply_paralysis_effect(target):
        if target.non_volatile_status is not StatusType.Par:
            return False
        else:
            Status.add_volatile_stat_mod(target, StatsType.Spe, 0.5)
            return True

    @staticmethod
    def apply_poisoning_effect(target):
        if target.non_volatile_status != StatusType.Psn:
            return False
        else:
            Status.decrease_hp(target, 0.125)
            return True

    @staticmethod
    def apply_bad_poisoning_effect(target):
        if target.non_volatile_status != StatusType.Tox:
            return False
        else:
            target.bad_poison_turn += 1
            Status.decrease_hp(target, target.bad_poison_heard / 16.0)
            return True

    @staticmethod
    def apply_burning_effect(target):
        if target.non_volatile_status != StatusType.Brn:
            return False
        else:
            Status.decrease_hp(target, 0.0625)
            return True

    @staticmethod
    def apply_frozen_effect(target):
        if target.non_volatile_status != StatusType.Frz:
            return False
        else:
            target.blocked = True
            return True

    @staticmethod
    def apply_sleep_effect(target):
        if target.non_volatile_status != StatusType.Slp:
            return False
        else:
            target.blocked = True
            return True

    @staticmethod
    def apply_fainted_effect(target):
        if target.non_volatile_status != StatusType.Fainted:
            return False
        else:
            target.stats.damage = target.stats.real_stats[StatsType.HP]


Status.apply_status_effect = {
    StatusType.Par: Status.apply_paralysis_effect,
    StatusType.Frz: Status.apply_frozen_effect,
    StatusType.Slp: Status.apply_sleep_effect,
    StatusType.Fainted: Status.apply_fainted_effect
}
