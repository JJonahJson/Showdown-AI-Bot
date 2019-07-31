from ai.chooser_type import Difficulty
from model.damage_calculator import DamageCalculator, StatusType
from model.field_type import Weather
from model.move_type import MoveCategory
from model.stats_type import StatsType
from model.status import immune


class Chooser:

    def __init__(self, difficulty):
        try:
            self.difficulty = Difficulty[difficulty.capitalize()]
            print("Starting bot with {} mode!".format(difficulty))
        except:
            print("{} not a supported difficulty!\n Use easy or normal or hard!".format(difficulty))
            exit(2)

        self.handler_move = {
            Difficulty.Easy: Chooser.__handle_easy_move__,
            Difficulty.Normal: Chooser.__handle_normal_move__,
            Difficulty.Hard: Chooser.__handle_hard_move__
        }

        self.handler_switch = {
            Difficulty.Easy: Chooser.__handle_easy_switch__,
            Difficulty.Normal: Chooser.__handle_normal_switch__,
            Difficulty.Hard: Chooser.__handle_hard_switch__
        }

    def choose_move(self, field, is_trapped=False):
        return self.handler_move[self.difficulty](field, is_trapped)

    def choose_switch(self, field):
        return self.handler_switch[self.difficulty](field)

    @staticmethod
    def __handle_easy_switch__(field):
        bot_team = field.all_pkmns_bot
        valid_switch = {}
        for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                field.active_pokemon_bot.name != x[1].name,
                                      bot_team.items())):

            valid_switch[index_pkmn] = 0
            for pkmn_type in bot_team[index_pkmn].types:
                for pkmn_type_oppo in field.active_pokemon_oppo.types:
                    if DamageCalculator.weak_to(pkmn_type_oppo, pkmn_type):
                        valid_switch[index_pkmn] += 1

                    if DamageCalculator.weak_to(pkmn_type, pkmn_type_oppo):
                        valid_switch[index_pkmn] -= 1

                    if DamageCalculator.resists_to(pkmn_type_oppo, pkmn_type):
                        valid_switch[index_pkmn] -= 1

                    if DamageCalculator.resists_to(pkmn_type, pkmn_type_oppo):
                        valid_switch[index_pkmn] += 1

                    if DamageCalculator.immune_to(pkmn_type, pkmn_type_oppo):
                        valid_switch[index_pkmn] += 2

                    if DamageCalculator.immune_to(pkmn_type_oppo, pkmn_type):
                        valid_switch[index_pkmn] -= 2

        choosen_switch_index = max(valid_switch.keys(), key=lambda x: valid_switch[x])
        return choosen_switch_index

    @staticmethod
    def __handle_easy_move__(field, is_trapped=False):
        # determine the index of the move with more damage inflicted to the opponent
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = {}
        for index_move in moves:
            damage[index_move] = DamageCalculator.calculate(field.weather, field.field, field.active_pokemon_bot,
                                                            moves[index_move], field.active_pokemon_oppo)

        max_damage_move_index = max(damage.keys(), key=lambda x: damage[x])

        print("Selected move:{} with predicted damage:{}".format(moves[max_damage_move_index].move_name, str(damage[
                                                                                                                 max_damage_move_index])))
        return max_damage_move_index, True

    @staticmethod
    def __handle_normal_move__(field, is_trapped=False):
        bot_may_die = False
        bot_has_protect = False
        # determine if the opponent is faster
        opponent_faster = field.active_pokemon_bot.stats.get_actual(StatsType.Spe) < \
                          field.active_pokemon_oppo.stats.get_actual(StatsType.Spe)

        # determine the index of the move with more damage inflicted to the opponent
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = {}
        for index_move in moves:
            if moves[index_move].category == MoveCategory.Status:
                if moves[index_move].non_volatile_status[1]:
                    if field.active_pokemon_oppo.non_volatile_status == StatusType.Normal and \
                            not ((field.active_pokemon_oppo.types[0] in immune[
                                moves[index_move].non_volatile_status[1]]) or (
                                         len(field.active_pokemon_oppo.types) > 1 and \
                                         field.active_pokemon_oppo.types[1] in
                                         immune[
                                             moves[
                                                 index_move].non_volatile_status[1]])):
                        return index_move, True
                elif moves[index_move].volatile_status[1]:
                    if not moves[index_move].volatile_status[1] in field.active_pokemon_oppo.volatile_status:
                        print("Selected move {}".format(moves[index_move].move_name))
                        return index_move, True

                else:
                    for stat, boost in moves[index_move].on_user_stats:
                        if field.active_pokemon_bot.stats.mul_stats[stat] == 0:
                            print("Selected move {}".format(moves[index_move].move_name))
                            return index_move, True

                    for stat, boost in moves[index_move].on_target_stats:
                        if field.active_pokemon_oppo.stats.mul_stats[stat] == 0:
                            print("Selected move {}".format(moves[index_move].move_name))
                            return index_move, True

            damage[index_move] = DamageCalculator.calculate(field.weather, field.field, field.active_pokemon_bot,
                                                            moves[index_move], field.active_pokemon_oppo)
            bot_has_protect = moves[index_move].move_name == "Protect"
            if bot_has_protect:
                protect_index = index_move

        max_damage_move_index = max(damage.keys(), key=lambda x: damage[x])

        # determine when opponent's hp may decrease
        oppo_is_damaging = (field.active_pokemon_oppo.non_volatile_status in [StatusType.Brn, StatusType.Psn,
                                                                              StatusType.Tox]) or (
                                   StatusType.Confusion in field.active_pokemon_oppo.volatile_status) or (
                                   field.weather in [Weather.Hail, Weather.Sandstorm])

        opponent_moves = field.active_pokemon_oppo.get_usable_moves()

        # check if an opponent's move kills the bot
        for index_move in opponent_moves:
            bot_may_die = (field.active_pokemon_bot.stats.get_actual_hp() - DamageCalculator.calculate(field.weather,
                                                                                                       field.field,
                                                                                                       field.active_pokemon_oppo,
                                                                                                       opponent_moves[
                                                                                                           index_move],
                                                                                                       field.active_pokemon_bot)) <= 0

        if oppo_is_damaging and bot_may_die and bot_has_protect and opponent_faster:
            return protect_index, True

        bench_bot = field.all_pkmns_bot
        for pkmn in bench_bot:
            if pkmn != 1:
                moves_actual = bench_bot[pkmn].moves
                for move in moves_actual:
                    if 2 * damage[max_damage_move_index] < DamageCalculator.calculate(field.weather, field.field,
                                                                                      bench_bot[pkmn],
                                                                                      moves_actual[move],
                                                                                      field.active_pokemon_oppo):
                        return pkmn, False

        if bot_may_die and opponent_faster and not bot_has_protect and len(
                dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                      field.active_pokemon_bot.name != x[1].name,
                            field.all_pkmns_bot.items()))) > 1:
            return Chooser.__handle_normal_switch__(field), False

        print("Selected move:{} with predicted damage:{}".format(moves[max_damage_move_index].move_name, str(damage[
                                                                                                                 max_damage_move_index])))
        return max_damage_move_index, True

    @staticmethod
    def __handle_normal_switch__(field):
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

    @staticmethod
    def __handle_hard_move__(field, is_trapped=False):
        pass

    @staticmethod
    def __handle_hard_switch__(field):
        pass
