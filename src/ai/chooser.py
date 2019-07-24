from src.model.field import BattleFieldSingle, Weather
from src.model.damagecalculator import DamageCalculator, TypeMultiplier
from src.model.status import StatusType
from src.model.stats import StatsType


class Chooser:

    @staticmethod
    def choose_move(field: BattleFieldSingle):
        # determine if the opponent is faster
        opponent_faster = False
        if field.active_pokemon_bot.stats.real_stats[StatsType.Spe] < field.active_pokemon_oppo.stats.real_stats[
            StatsType.Spe]:
            opponent_faster = True

        # determine the index of the move with more damage inflicted to the opponent
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = {}
        for index_move in moves:
            damage[index_move] = DamageCalculator.calculate(field.weather, field.field, field.active_pokemon_bot,
                                                            moves[index_move], field.active_pokemon_oppo)

        max_damage_move_index = max(damage.keys(), key=lambda x: damage[x])

        # determine when is better to use protect
        if (field.active_pokemon_oppo.non_volatile_status in [StatusType.Brn, StatusType.Psn, StatusType.Tox]) or (
                StatusType.Confusion in field.active_pokemon_oppo.volatile_status) or (
                field.weather in [Weather.Hail, Weather.Sandstorm]):
            opponent_moves = field.active_pokemon_oppo.get_usable_moves()
            opponent_damage = []
            for index_move in opponent_moves:
                damage.append(DamageCalculator.calculate(field.weather, field.field, field.active_pokemon_oppo,
                                                         opponent_moves[index_move], field.active_pokemon_bot))

        return max_damage_move_index

    @staticmethod
    def choose_switch(field: BattleFieldSingle):
        bot_team = field.all_pkmns_bot
        valid_switch = {}
        for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                field.active_pokemon_bot.name != x[1].name,
                                      bot_team.items())):
            # TODO Convert to dict
            valid_switch[index_pkmn] = 0
            for pkmn_type in bot_team[index_pkmn].types:
                for pkmn_type_oppo in field.active_pokemon_oppo.types:
                    if pkmn_type in TypeMultiplier.weakTo[pkmn_type_oppo]:
                        valid_switch[index_pkmn] += 1

                    if pkmn_type_oppo in TypeMultiplier.weakTo[pkmn_type]:
                        valid_switch[index_pkmn] -= 1

                    if pkmn_type in TypeMultiplier.resistsTo[pkmn_type_oppo]:
                        valid_switch[index_pkmn] -= 1

                    if pkmn_type_oppo in TypeMultiplier.resistsTo[pkmn_type]:
                        valid_switch[index_pkmn] += 1

                    if pkmn_type_oppo in TypeMultiplier.immuneTo[pkmn_type]:
                        valid_switch[index_pkmn] += 2

                    if pkmn_type in TypeMultiplier.immuneTo[pkmn_type_oppo]:
                        valid_switch[index_pkmn] -= 2

        choosen_switch_index = max(valid_switch.keys(), key=lambda x: valid_switch[x])
        return choosen_switch_index
