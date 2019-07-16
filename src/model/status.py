from src.model.pokemontype import PokemonType
from src.model.stats import StatsType
from enum import Enum, auto


class StatusType(Enum):
    """Class that represents all possible statuses of a pokemon"""
    Normal = auto(),
    Fainted = auto(),
    Poisoned = auto(),
    BPoisoned = auto(),
    Burned = auto(),
    Paralyzed = auto(),
    Frozen = auto(),
    Asleep = auto(),
    Infatuated = auto(),
    Confused = auto(),
    Trapped = auto(),
    Protected = auto(),
    Endure = auto(),
    Flinched = auto()


non_volatile = {
    StatusType.Normal: False,
    StatusType.Fainted: True,
    StatusType.Poisoned: True,
    StatusType.BPoisoned: True,
    StatusType.Burned: True,
    StatusType.Paralyzed: True,
    StatusType.Frozen: True,
    StatusType.Asleep: True,

    StatusType.Infatuated: False,
    StatusType.Flinched: False,
    StatusType.Confused: False,
    StatusType.Protected: False,
    StatusType.Trapped: False,
    StatusType.Endure: False,
}

immune = {
    StatusType.Poisoned: [PokemonType.Poison, PokemonType.Steel],
    StatusType.BPoisoned: [PokemonType.Poison, PokemonType.Steel],
    StatusType.Paralyzed: [PokemonType.Electric],
    StatusType.Frozen: [PokemonType.Ice],
    StatusType.Burned: [PokemonType.Fire],
    StatusType.Normal: [],
    StatusType.Fainted: [],
    StatusType.Infatuated: [],
    StatusType.Flinched: [],
    StatusType.Confused: [],
    StatusType.Protected: [],
    StatusType.Trapped: [],
    StatusType.Endure: [],
    StatusType.Asleep: []
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
        for pkmn_type in pokemon.types:
            if pkmn_type in immune[status] or pokemon.non_volatile_status is not StatusType.Normal:
                return False
        pokemon.non_volatile_status.type = status
        return True

    @staticmethod
    def add_volatile_status(status: StatusType, pokemon):
        """Method which adds a volatile status to pokemon's volatile status list"""
        if non_volatile[status]:
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
    def add_output_effect(pokemon, value: float):
        """Method which applies changes to the damage output multiplier"""
        pokemon.damage_output_multiplier *= value

    @staticmethod
    def remove_output_effect(pokemon, value: float):
        """Method which removes changes to the damage output multiplier	"""
        pokemon.damage_output_multiplier /= value

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
        pokemon.stats.damage += pokemon.stats.base_stats[StatsType.HP] * percentage
