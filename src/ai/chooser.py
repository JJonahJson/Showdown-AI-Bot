from src.model.damagecalculator import DamageCalculator, TypeMultiplier
from src.model.field import BattleFieldSingle
from src.model.status import StatusType


class Chooser:

    @staticmethod
    def choose_move(field: BattleFieldSingle):
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = []
        for index_move in moves:
            damage.append(DamageCalculator.calculate(field.weather, field.field, field.active_pokemon_bot,
                                                     moves[index_move], field.active_pokemon_oppo))

        choosen_move_index = max(range(len(damage)), key=lambda x: damage[x])
        return choosen_move_index + 1

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

        choosen_switch_index = max(range(len(valid_switch)), key=lambda x: valid_switch[x])
        return choosen_switch_index + 1
