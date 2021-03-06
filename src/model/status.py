from model.status_type import StatusType

from model.pokemon_type import PokemonType
from model.stats_type import StatsType


non_volatile = {
    StatusType.Normal: False,
    StatusType.Fnt: True,
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
    StatusType.Trapped: False,
    StatusType.Endure: False,
    StatusType.Substitute: False,
    StatusType.Taunt: False,
    StatusType.Aquaring: False,
    StatusType.Autotomize: False,
    StatusType.Banefulbunker: False,
    StatusType.Bide: False,
    StatusType.Partiallytrapped: False,
    StatusType.Charge: False,
    StatusType.Curse: False,
    StatusType.Defensecurl: False,
    StatusType.Destinybond: False,
    StatusType.Disable: False,
    StatusType.Electrify: False,
    StatusType.Embargo: False,
    StatusType.Encore: False,
    StatusType.Focusenergy: False,
    StatusType.Followme: False,
    StatusType.Foresight: False,
    StatusType.Gastroacid: False,
    StatusType.Grudge: False,
    StatusType.Healblock: False,
    StatusType.Helpinghand: False,
    StatusType.Imprison: False,
    StatusType.Ingrain: False,
    StatusType.Kingsshield: False,
    StatusType.Laserfocus: False,
    StatusType.Leechseed: False,
    StatusType.Magiccoat: False,
    StatusType.Magnetrise: False,
    StatusType.Minimize: False,
    StatusType.Miracleeye: False,
    StatusType.Nightmare: False,
    StatusType.Powder: False,
    StatusType.Powertrick: False,
    StatusType.Ragepowder: False,
    StatusType.Smackdown: False,
    StatusType.Snatch: False,
    StatusType.Spikyshield: False,
    StatusType.Spotlight: False,
    StatusType.Stockpile: False,
    StatusType.Telekinesis: False,
    StatusType.Throatchop: False,
    StatusType.Torment: False,
    StatusType.Yawn: False

}

immune = {
    StatusType.Psn: [PokemonType.Poison, PokemonType.Steel],
    StatusType.Tox: [PokemonType.Poison, PokemonType.Steel],
    StatusType.Par: [PokemonType.Electric],
    StatusType.Frz: [PokemonType.Ice],
    StatusType.Brn: [PokemonType.Fire],
    StatusType.Slp: [],
    StatusType.Normal: [],
    StatusType.Fnt: []
}


class Status:
    """Utility class with static methods which modify status and relative stats"""

    @staticmethod
    def apply_non_volatile_status(status, pokemon) -> bool:
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
                                               pokemon.non_volatile_status and status is not StatusType.Fnt):
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

            if target.non_volatile_status == StatusType.Fnt:
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
    def add_volatile_status(status, pokemon):
        """Method which adds a volatile status to pokemon's volatile status list"""
        if non_volatile[status]:
            return False
        if status in pokemon.volatile_status:
            return False

        pokemon.volatile_status.append(status)
        return True

    @staticmethod
    def remove_volatile_status(status, pokemon):
        """Method which removes a volatile status to pokemon's volatile status list"""
        try:
            pokemon.volatile_status.remove(status)
        except ValueError:
            pass

    @staticmethod
    def add_volatile_stat_mod(pokemon, stat_type, value: float):
        """Method which adds changes to the specified volatile stat"""
        pokemon.stats.volatile_mul[stat_type] *= value

    @staticmethod
    def remove_volatile_stat_mod(pokemon, stat_type, value: float):
        """Method which removes changes to the specified volatile stat"""
        pokemon.stats.volatile_mul[stat_type] /= value

    @staticmethod
    def decrease_hp(pokemon, percentage: float):
        """Method which decreases pokemon's hp based on a specified percentage"""
        pokemon.stats.damage += round(pokemon.stats.real_stats[StatsType.HP] * percentage)
        if pokemon.stats.damage >= pokemon.stats.real_stats[StatsType.HP]:
            Status.apply_non_volatile_status(StatusType.Fnt, pokemon)

    @staticmethod
    def apply_infatuation(target, caster):
        """Method which applies infatuation"""
        if target.gender == caster.gender or target.gender == "":
            return False
        if Status.add_volatile_status(StatusType.Attract, target):
            return True

        return False

    @staticmethod
    def apply_paralysis_effect(target):
        """Method which applies paralyze effect and halves the speed of the pokemon"""
        if target.non_volatile_status is not StatusType.Par:
            return False
        else:
            Status.add_volatile_stat_mod(target, StatsType.Spe, 0.5)
            return True

    @staticmethod
    def apply_poisoning_effect(target):
        """Method which applies poisoning effect and decreases hp by 12.5%"""
        if target.non_volatile_status != StatusType.Psn:
            return False
        else:
            Status.decrease_hp(target, 0.125)
            return True

    @staticmethod
    def apply_bad_poisoning_effect(target):
        """Method which applies bad poisoning of a pokemon and applyes the continuos and relentless damage"""
        if target.non_volatile_status != StatusType.Tox:
            return False
        else:
            target.bad_poison_turn += 1
            Status.decrease_hp(target, target.bad_poison_heard / 16.0)
            return True

    @staticmethod
    def apply_burning_effect(target):
        """Method which applies burn status and decrese hp of a pokemon by 6.25%"""
        if target.non_volatile_status != StatusType.Brn:
            return False
        else:
            Status.decrease_hp(target, 0.0625)
            return True

    @staticmethod
    def apply_frozen_effect(target):
        """Method that applies frozen status to a pokemon"""
        if target.non_volatile_status != StatusType.Frz:
            return False
        else:
            target.blocked = True
            return True

    @staticmethod
    def apply_sleep_effect(target):
        """Method that apply sleep effect to a pokemon"""
        if target.non_volatile_status != StatusType.Slp:
            return False
        else:
            target.blocked = True
            return True

    @staticmethod
    def apply_fainted_effect(target):
        """Method that applies fainted effect to a pokemon"""
        if target.non_volatile_status != StatusType.Fnt:
            return False
        else:
            target.stats.damage = target.stats.real_stats[StatsType.HP]


Status.apply_status_effect = {
    StatusType.Par: Status.apply_paralysis_effect,
    StatusType.Frz: Status.apply_frozen_effect,
    StatusType.Slp: Status.apply_sleep_effect,
    StatusType.Fnt: Status.apply_fainted_effect
}
