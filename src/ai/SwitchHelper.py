from model.damage_calculator import DamageCalculator
from model.status_type import StatusType


def switch_help(field):
    bot_team = field.all_pkmns_bot
    valid_switch = {}
    for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                            field.active_pokemon_bot.name != x[1].name,
                                  bot_team.items())):

        valid_switch[index_pkmn] = 0
        for pkmn_type in bot_team[index_pkmn].types:
            for pkmn_type_oppo in field.active_pokemon_oppo.types:
                if DamageCalculator.weak_to(pkmn_type_oppo, pkmn_type):
                    valid_switch[index_pkmn] += 1 * 2

                if DamageCalculator.weak_to(pkmn_type, pkmn_type_oppo):
                    valid_switch[index_pkmn] -= 1 * 2

                if DamageCalculator.resists_to(pkmn_type_oppo, pkmn_type):
                    valid_switch[index_pkmn] -= 1 * 2

                if DamageCalculator.resists_to(pkmn_type, pkmn_type_oppo):
                    valid_switch[index_pkmn] += 1 * 2

                if DamageCalculator.immune_to(pkmn_type, pkmn_type_oppo):
                    valid_switch[index_pkmn] += 2 * 2

                if DamageCalculator.immune_to(pkmn_type_oppo, pkmn_type):
                    valid_switch[index_pkmn] -= 2 * 2

        for move_type in list(map(lambda x: x[1].move_type, bot_team[index_pkmn].moves.items())):
            for pkmn_type_oppo in field.active_pokemon_oppo.types:
                if DamageCalculator.resists_to(pkmn_type_oppo, move_type):
                    valid_switch[index_pkmn] -= 1

                if DamageCalculator.weak_to(pkmn_type_oppo, move_type):
                    valid_switch[index_pkmn] += 2

                if DamageCalculator.immune_to(pkmn_type_oppo, move_type):
                    valid_switch[index_pkmn] -= 1

    choosen_switch_index = max(valid_switch.keys(), key=lambda x: valid_switch[x])
    return choosen_switch_index