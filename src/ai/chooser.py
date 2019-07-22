from src.model.field import BattleFieldSingle
from src.model.damagecalculator import DamageCalculator, TypeMultiplier


class Chooser:

    @staticmethod
    def choose_move(field: BattleFieldSingle):
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = []
        for index_move in moves:
            damage[index_move] = DamageCalculator.calculate(field.weather, field.field, field.active_pokemon_bot,
                                                            moves[index_move], field.active_pokemon_oppo)

        choosen_move = max(damage)
        return choosen_move

    @staticmethod
    def choose_switch(field: BattleFieldSingle):
        bot_team = field.all_pkmns_bot
        valid_switch = []
        for index_pkmn in bot_team:
            valid_switch[index_pkmn] = 0
            for type in bot_team[index_pkmn].types:
                for type_oppo in field.active_pokemon_oppo.types:
                    if type in TypeMultiplier.resistsTo[type_oppo]:
                        valid_switch[index_pkmn] += 1

                    if type in TypeMultiplier.weakTo[type_oppo]:
                        valid_switch[index_pkmn] -= 1

                    if type in TypeMultiplier.ineffectiveTo[type_oppo]:
                        valid_switch[index_pkmn] -= 1

        choosen_switch = max(valid_switch)
        return choosen_switch
