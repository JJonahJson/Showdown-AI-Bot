from ai.chooser_type import Difficulty
from model.damage_calculator import DamageCalculator, StatusType
from model.field_type import Weather
from model.stats_type import StatsType


class Chooser:

    def __init__(self, difficulty):
        try:
            self.difficulty = Difficulty[difficulty.capitalize()]
            print("Starting bot with {} mode!".format(difficulty))
        except :
            print("{} not a supported difficulty!\n Use easy or normal or hard!".format(difficulty))
            exit(2)

        self.handler_move = {
            Difficulty.Easy: Chooser._handle_easy_move,
        }

        self.handler_switch = {
            Difficulty.Easy: Chooser._handle_easy_switch
        }

    def choose_move(self, field):
        return self.handler_move[self.difficulty](field)

    def choose_switch(self, field):
        return self.handler_switch[self.difficulty](field)

    @staticmethod
    def _handle_easy_switch(field):
        bot_team = field.all_pkmns_bot
        valid_switch = {}
        for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                field.active_pokemon_bot.name != x[1].name,
                                      bot_team.items())):
            # TODO Convert to dict
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
    def _handle_easy_move(field):
        bot_may_die = False
        bot_has_protect = False
        # determine if the opponent is faster
        opponent_faster = field.active_pokemon_bot.stats.get_actual(StatsType.Spe) < \
                          field.active_pokemon_oppo.stats.get_actual(StatsType.Spe)

        # determine the index of the move with more damage inflicted to the opponent
        moves = field.active_pokemon_bot.get_usable_moves()
        damage = {}
        for index_move in moves:
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
        if oppo_is_damaging and bot_may_die and bot_has_protect:
            return protect_index

        print("Selected move:{} with predicted damage:{}".format(moves[max_damage_move_index].move_name, str(damage[
                                                                                                                 max_damage_move_index])))
        return max_damage_move_index
