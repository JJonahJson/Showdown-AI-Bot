import logging

from ai.chooser_type import Difficulty
from model.damage_calculator import DamageCalculator, StatusType
from model.field_type import Weather
from model.move_type import MoveCategory
from model.stats_type import StatsType
from model.status import immune
from model.pokemon_type import PokemonType
from ai.iterative_search import IterativeDeepeningMinMax

logger = logging.getLogger("Chooser")


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
            Difficulty.Hard: Chooser.__handle_normal_switch__
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
        logger.info("Easy-Switch {} with {}!".format(field.active_pokemon_bot, field.all_pkmns_bot[
            choosen_switch_index]))
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

        print("Selected move:{} with predicted damage:{}".format(moves[max_damage_move_index].move_name,
                                                                 str(damage[max_damage_move_index])))
        logger.info("{} selected move {} with predicted damage {} against {}".format(field.active_pokemon_bot,
                                                                                     moves[
                                                                                         max_damage_move_index].move_name,
                                                                                     str(damage[
                                                                                             max_damage_move_index]),
                                                                                     field.active_pokemon_oppo))

        return max_damage_move_index, True

    @staticmethod
    def __handle_normal_move__(field, is_trapped=False):
        bot_may_die = False
        bot_has_protect = False

        if StatusType.Encore in field.active_pokemon_bot.volatile_status:
            for move in field.active_pokemon_bot.get_usable_moves():
                return move, True

        # determine if the opponent is faster
        opponent_faster = field.active_pokemon_bot.stats.get_actual(StatsType.Spe) < \
                          field.active_pokemon_oppo.stats.get_actual(StatsType.Spe)

        # determine the index of the move with more damage inflicted to the opponent
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = {}
        for index_move in moves:
            if moves[index_move].category == MoveCategory.Status:
                if moves[index_move].non_volatile_status[1]:

                    immune_to_move_type = DamageCalculator.immune_to(field.active_pokemon_oppo.types[0],
                                                                     moves[index_move].move_type) or (len(
                        field.active_pokemon_oppo.types) > 1 and DamageCalculator.immune_to(
                        field.active_pokemon_oppo.types[1], moves[index_move].move_type))

                    immune_status_type = ((field.active_pokemon_oppo.types[0] in immune[
                        moves[index_move].non_volatile_status[1]]) or (
                                                  len(field.active_pokemon_oppo.types) > 1 and \
                                                  field.active_pokemon_oppo.types[1] in
                                                  immune[
                                                      moves[
                                                          index_move].non_volatile_status[1]]))

                    if field.active_pokemon_oppo.non_volatile_status == StatusType.Normal and not immune_status_type \
                            and not immune_to_move_type:
                        logger.info("{} selected move {} with non volatile status {} against {}".format(
                            field.active_pokemon_bot,
                            moves[index_move].move_name,
                            moves[index_move].non_volatile_status[1].name,
                            field.active_pokemon_oppo))
                        return index_move, True

                elif moves[index_move].volatile_status[1] and moves[index_move].move_name != "Protect" \
                        and moves[index_move].move_name != "Kingsshield":
                    if moves[index_move].volatile_status[0] == "self":
                        if not moves[index_move].volatile_status[1] in field.active_pokemon_bot.volatile_status:
                            print("Selected move {}".format(moves[index_move].move_name))
                            logger.info("{} selected move {} with volatile status {} for {}".format(
                                field.active_pokemon_bot,
                                moves[index_move].move_name,
                                moves[index_move].volatile_status[1].name,
                                field.active_pokemon_bot))
                            return index_move, True
                    else:
                        if not moves[index_move].volatile_status[1] in field.active_pokemon_oppo.volatile_status:
                            print("Selected move {}".format(moves[index_move].move_name))
                            logger.info("{} selected move {} with volatile status {} against {}".format(
                                field.active_pokemon_bot,
                                moves[index_move].move_name,
                                moves[index_move].volatile_status[1].name,
                                field.active_pokemon_oppo))
                            return index_move, True

                else:
                    for stat, boost in moves[index_move].on_user_stats:
                        if field.active_pokemon_bot.stats.mul_stats[stat] == 0:
                            print("Selected move {}".format(moves[index_move].move_name))
                            logger.info("{} selected move {} with self-boost on {} of {} stages".format(
                                field.active_pokemon_bot,
                                moves[index_move].move_name,
                                stat.value,
                                str(boost)))
                            return index_move, True

                    for stat, boost in moves[index_move].on_target_stats:
                        if field.active_pokemon_oppo.stats.mul_stats[stat] == 0:
                            print("Selected move {}".format(moves[index_move].move_name))
                            logger.info("{} selected move {} with enemy-unboost on {} of {} stages".format(
                                field.active_pokemon_bot,
                                moves[index_move].move_name,
                                stat.name,
                                str(boost)))
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
            logger.info("Selected Protect against {}".format(field.active_pokemon_oppo))
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
                        logger.info("MoreDamage Switch {} with {}".format(field.active_pokemon_bot,
                                                                          field.all_pkmns_bot[pkmn]))
                        return pkmn, False

        if bot_may_die and opponent_faster and not bot_has_protect and len(
                dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                      field.active_pokemon_bot.name != x[1].name,
                            field.all_pkmns_bot.items()))) > 1:
            logging.info("MayDieFasterSwitch")
            return Chooser.__handle_normal_switch__(field), False

        print("Selected move:{} with predicted damage:{}".format(moves[max_damage_move_index].move_name, str(damage[
                                                                                                                 max_damage_move_index])))

        logger.info("{} selected move {} with predicted damage {} against {}".format(field.active_pokemon_bot,
                                                                                     moves[
                                                                                         max_damage_move_index].move_name,
                                                                                     str(damage[
                                                                                             max_damage_move_index]),
                                                                                     field.active_pokemon_oppo))
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
        logging.info("Switch {} with {}".format(field.active_pokemon_bot, field.all_pkmns_bot[choosen_switch_index]))
        return choosen_switch_index

    @staticmethod
    def __handle_hard_move__(field, is_trapped=False):
        result = IterativeDeepeningMinMax.make_decision(field, Chooser.valuation_action)
        return result[1], result[2]

    @staticmethod
    def __handle_hard_switch__(field):
        pass

    @staticmethod
    def valuation_action(field):
        valuation = 0
        active_bot = field.active_pokemon_bot
        active_oppo = field.active_pokemon_oppo
        moves_bot = active_bot.moves
        moves_oppo = active_oppo.moves
        possible_moves_oppo = active_oppo.possible_moves
        weather = field.weather
        terrain = field.field
        bench_bot = field.all_pkmns_bot
        bench_oppo = field.all_pkmns_oppo

        for pkmn in bench_bot:
            # Number of bot pkmns fainted
            if bench_bot[pkmn].non_volatile_status == StatusType.Fnt:
                valuation -= 50
            # Number of bot pkmns with status changed
            elif bench_bot[pkmn].non_volatile_status != StatusType.Normal:
                valuation -= 5

            if bench_bot[pkmn].non_volatile_status != StatusType.Fnt:
                hp_left = (bench_bot[pkmn].stats.get_actual_hp() / (bench_bot[pkmn].stats.real_stats[StatsType.HP])) * 100

                if hp_left < 75:
                    valuation -= 2

                if hp_left < 50:
                    valuation -= 4

                if hp_left < 25:
                    valuation -= 8

        # Points of mul_stats changed for active bot
        for stat in active_bot.stats.mul_stats:
            valuation += active_bot.stats.mul_stats[stat]*2

        # Points of mul_stats changed for active oppo
        for stat in active_oppo.stats.mul_stats:
            valuation -= active_oppo.stats.mul_stats[stat]*2

        # Number of opponent pkmns fainted
        for pkmn in bench_oppo:
            # Number of opponent pkmns fainted
            if bench_oppo[pkmn].non_volatile_status == StatusType.Fnt:
                valuation += 20
            # Number of opponent pkmns with status changed
            elif bench_oppo[pkmn].non_volatile_status != StatusType.Normal:
                valuation -= 20
            hp_left = (bench_oppo[pkmn].stats.get_actual_hp() / bench_oppo[pkmn].stats.real_stats[StatsType.HP]) * 100

            if hp_left < 75:
                valuation += 20

            if hp_left < 50:
                valuation += 40

            if hp_left < 25:
                valuation += 80

        # Points with  rain weather
        if weather in [Weather.Raindance, Weather.Primordialsea]:

            for move in moves_bot:
                if moves_bot[move].move_type == PokemonType.Water:
                    valuation += 1
                elif moves_bot[move].move_type == PokemonType.Fire:
                    valuation -= 1
                if "Thunder" == moves_bot[move].move_name:
                    valuation += 1

            for move in moves_oppo:
                if moves_oppo[move].move_type == PokemonType.Water:
                    valuation -= 1
                elif moves_oppo[move].move_type == PokemonType.Fire:
                    valuation += 1
                if "Thunder" == moves_oppo[move].move_name:
                    valuation -= 1

            for move in possible_moves_oppo:
                if possible_moves_oppo[move].move_type == PokemonType.Water:
                    valuation -= 1
                elif possible_moves_oppo[move].move_type == PokemonType.Fire:
                    valuation += 1
                if "Thunder" == possible_moves_oppo[move].move_name:
                    valuation -= 1

        elif weather in [Weather.Sunnyday, Weather.Desolateland]:

            for move in moves_bot:
                if moves_bot[move].move_type == PokemonType.Water:
                    valuation -= 1
                elif moves_bot[move].move_type == PokemonType.Fire:
                    valuation += 1
                if "Solar Beam" == moves_bot[move].move_name:
                    valuation += 1

            for move in moves_oppo:
                if moves_oppo[move].move_type == PokemonType.Water:
                    valuation += 1
                elif moves_oppo[move].move_type == PokemonType.Fire:
                    valuation -= 1
                if "Solar Beam" == moves_oppo[move].move_name:
                    valuation -= 1

            for move in possible_moves_oppo:
                if possible_moves_oppo[move].move_type == PokemonType.Water:
                    valuation += 1
                elif possible_moves_oppo[move].move_type == PokemonType.Fire:
                    valuation -= 1
                if "Solar Beam" == possible_moves_oppo[move].move_name:
                    valuation -= 1

        for bot_pkmn_type in active_bot.types:
            for oppo_pkmn_type in active_oppo.types:
                if DamageCalculator.weak_to(oppo_pkmn_type, bot_pkmn_type):
                    valuation += 5
                if DamageCalculator.resists_to(bot_pkmn_type, oppo_pkmn_type):
                    valuation += 5
                if DamageCalculator.immune_to(bot_pkmn_type, oppo_pkmn_type):
                    valuation += 5
                if DamageCalculator.weak_to(bot_pkmn_type, oppo_pkmn_type):
                    valuation -= 5
                if DamageCalculator.resists_to(oppo_pkmn_type, bot_pkmn_type):
                    valuation -= 5
                if DamageCalculator.immune_to(oppo_pkmn_type, bot_pkmn_type):
                    valuation -= 10
            for oppo_move in moves_oppo:
                oppo_move_type = moves_oppo[oppo_move].move_type
                if DamageCalculator.resists_to(bot_pkmn_type, oppo_move_type):
                    valuation += 10
                if DamageCalculator.immune_to(bot_pkmn_type, oppo_move_type):
                    valuation += 10
                if DamageCalculator.weak_to(bot_pkmn_type, oppo_move_type):
                    valuation -= 5
                if DamageCalculator.resists_to(oppo_move_type, bot_pkmn_type):
                    valuation -= 5
                if DamageCalculator.immune_to(oppo_move_type, bot_pkmn_type):
                    valuation -= 5
            for oppo_move in possible_moves_oppo:
                oppo_move_type = possible_moves_oppo[oppo_move].move_type
                if DamageCalculator.resists_to(bot_pkmn_type, oppo_move_type):
                    valuation += 10
                if DamageCalculator.immune_to(bot_pkmn_type, oppo_move_type):
                    valuation += 10
                if DamageCalculator.weak_to(bot_pkmn_type, oppo_move_type):
                    valuation -= 5
                if DamageCalculator.resists_to(oppo_move_type, bot_pkmn_type):
                    valuation -= 5
                if DamageCalculator.immune_to(oppo_move_type, bot_pkmn_type):
                    valuation -= 5

        for oppo_pkmn_type in active_oppo.types:
            for bot_move in moves_bot:
                bot_move_type = moves_bot[bot_move].move_type
                if DamageCalculator.weak_to(oppo_pkmn_type, bot_move_type):
                    valuation += 10
                if DamageCalculator.resists_to(bot_move_type, oppo_pkmn_type):
                    valuation += 1
                if DamageCalculator.immune_to(bot_move_type, oppo_pkmn_type):
                    valuation += 1
                if DamageCalculator.weak_to(bot_move_type, oppo_pkmn_type):
                    valuation -= 1
                if DamageCalculator.resists_to(oppo_pkmn_type, bot_move_type):
                    valuation -= 1
                if DamageCalculator.immune_to(oppo_pkmn_type, bot_move_type):
                    valuation -= 1
        return valuation
