from abc import ABC, abstractmethod

from model.pokemon import Pokemon
from model.stats_type import StatsType
from model.status import Status
from model.status_type import StatusType
from model.field_type import Field, Weather, SpeedCriterion


class BattleField(ABC):
    """BattleField superclass"""

    def __init__(self):
        self.weather = Weather.Normal
        self.field = Field.Normal
        self.speed_control = SpeedCriterion.Normal
        self.player_id = ""

    @abstractmethod
    def switch_pokemon(self, player: int, pokemon_in: int):
        pass

    @abstractmethod
    def update_buff(self, side, qta, level):
        pass

    @abstractmethod
    def update_turn(self):
        pass

    @abstractmethod
    def update_status(self, side, status=""):
        pass

    @abstractmethod
    def update_weather(self, weather):
        pass

    @abstractmethod
    def do_move(self, player: int, pokemon_caster: int, move_index: int, pokemon_target: int):
        pass

    @abstractmethod
    def update_field(self, terrain):
        pass

    @abstractmethod
    def update_damage(self, side, damage):
        pass

    @abstractmethod
    def get_pokemon_index_by_name(self, side, pkmn_name):
        pass


class BattleFieldSingle(BattleField):
    """Represents a battle field for a battle in single"""

    def __init__(self, active_pokemon_bot: Pokemon, active_pokemon_oppo: Pokemon, bench_bot: dict, bench_oppo: dict):
        """ Constructor method
        :param active_pokemon_bot: active pokemon of the bot
        :param active_pokemon_oppo: active pokemon of the opponenent
        :param bench_bot: list of pokemons in the bench
        :param bench_oppo: list of pokemons in the bench
        """
        super().__init__()
        self.active_pokemon_bot = active_pokemon_bot
        self.active_pokemon_oppo = active_pokemon_oppo
        self.all_pkmns_bot = bench_bot
        self.room_name = ""
        self.turn_number = 0
        self.all_pkmns_oppo = bench_oppo
        self.active_selector_side = {1: self.active_pokemon_bot, 2: self.active_pokemon_oppo}
        self.bench_selector_side = {1: self.all_pkmns_bot, 2: self.all_pkmns_oppo}

    def update_turn(self, value=2):
        self.turn_number += value
        print(self.turn_number)

    def get_pokemon_index_by_name(self, side, pkmn_name):
        for item in self.bench_selector_side[side]:
            if pkmn_name in self.bench_selector_side[side][item].name:
                return item

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

    def switch_pokemon(self, player: int, pokemon_in: int):
        """Switch pokemon
        :param player:
        :param pokemon_in:
        :return:
        """
        active_index = self.get_pokemon_index_by_name(player, self.active_selector_side[player].name)
        if player == 1:
            to_replace = self.active_pokemon_bot
            self.active_pokemon_bot = self.all_pkmns_bot[pokemon_in]
            self.all_pkmns_bot[active_index] = self.all_pkmns_bot[pokemon_in]
            self.all_pkmns_bot[pokemon_in] = to_replace
            self.active_selector_side[1] = self.active_pokemon_bot

        else:
            to_replace = self.active_pokemon_oppo
            self.active_pokemon_oppo = self.all_pkmns_oppo[pokemon_in]
            self.all_pkmns_oppo[active_index] = self.all_pkmns_oppo[pokemon_in]
            self.all_pkmns_oppo[pokemon_in] = to_replace
            self.active_selector_side[2] = self.active_pokemon_oppo

    def update_status(self, side, status=""):
        # TODO fix after merge, rename enum
        """Update the status of a pokemon
        :param side:
        :param status:
        :return:
        """
        if status == "":
            Status.remove_non_volatile_status(self.active_selector_side[side])
        else:
            Status.apply_non_volatile_status(StatusType[status.capitalize()], self.active_selector_side[side])

    def update_buff(self, side, stat, level):
        """Update the stats multiplier
        :param side: 1 or 2 1 for the bot side and 2 for the opponent side
        :param stat: StatsType that means the stats that has been buffed or debuffed
        :param level: the quantity of the buff/debuff
        :return:
        """
        self.active_selector_side[side].stats.modify(StatsType[stat.capitalize()], level)

    def update_weather(self, weather):
        """Updates the weather
        :param weather: The weather to be set
        :return:
        """
        self.weather = Weather[weather.capitalize()]

    def update_field(self, terrain):
        """Updates the field
        :param terrain: The terrain to be set
        :return:
        """
        self.field = terrain

    def update_damage(self, side, remaining_hp):
        """Updates the damage
        :param side: 1 or 2. 1 if it's the bot side, 2 if it's the oppo side
        :param remaining_hp: The remaining hp
        :return:
        """
        if side == 1:
            self.active_selector_side[side].stats.decrease_hp(remaining_hp)
        else:
            self.active_selector_side[side].stats.decrease_hp(int(remaining_hp / 100 * self.active_selector_side[
                side].stats.real_stats[StatsType.HP]))

    def update_heal(self, side, heal):
        """Heals a unit
        :param side: 1 or 2
        :param heal: The % of healing
        :return:
        """
        self.active_selector_side[side].stats.increase_hp(heal)
