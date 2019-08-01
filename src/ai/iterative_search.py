import math

from model.stats_type import StatsType
from model.status_type import StatusType
from ai.SwitchHelper import switch_help


class IterativeDeepeningMinMax:

    @staticmethod
    def make_decision(field, eval_fn):
        value = (-math.inf, None, None)
        curr_depth_limit = 1
        # Loop through possible moves
        if len(field.all_pkmns_oppo) == 1:
            # For each bot move
            for bot_move in field.active_pokemon_bot.moves:
                # For each opponent known move
                for oppo_moves in field.active_pokemon_oppo.moves:
                    new_state = IterativeDeepeningMinMax.create_state(field, bot_move, True, oppo_moves, True)
                    # BOTH MOVES
                    value = (max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, curr_depth_limit), value[0]), bot_move, True)
                # For each not known move of the opponent
                for possible_oppo_moves in field.active_pokemon_oppo.possible_moves:
                    new_state = IterativeDeepeningMinMax.create_state(field, bot_move, True, possible_oppo_moves, True)
                    value = (max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, curr_depth_limit), value[0]), bot_move, True)

            # All possibles switch WE SWITCH HE ATTACC
            for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                    field.active_pokemon_bot.name != x[1].name,
                                          field.all_pkmns_bot.items())):
                # For each kno
                for oppo_moves in field.active_pokemon_oppo.moves:
                    new_state = IterativeDeepeningMinMax.create_state(field, index_pkmn, False, oppo_moves, True)
                    value = (max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, curr_depth_limit), value[0]), index_pkmn, False)
                # For each not known move of the opponent
                for possible_oppo_moves in field.active_pokemon_oppo.possible_moves:
                    new_state = IterativeDeepeningMinMax.create_state(field, index_pkmn, False, possible_oppo_moves, True)
                    value = (max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, curr_depth_limit), value[0]), index_pkmn, False)
        else:

            # HE SWITCH AND WE ATTAC
            for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                    field.active_pokemon_bot.name != x[1].name,
                                          field.all_pkmns_oppo.items())):

                for bot_move in field.active_pokemon_bot.moves:
                    new_state = IterativeDeepeningMinMax.create_state(field, bot_move, True, index_pkmn, False)
                    value = (max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, curr_depth_limit), value[0]), bot_move, True)

                # BOTH SWITCH
                for index_bot_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                            field.active_pokemon_bot.name != x[1].name,
                                                  field.all_pkmns_bot.items())):
                    new_state = IterativeDeepeningMinMax.create_state(field, index_bot_pkmn, False, index_pkmn, False)
                    value = (max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, curr_depth_limit), value[0]),
                             index_bot_pkmn, False)
        return value

    @staticmethod
    def max_value(field, eval_fn, depth_limit):
        value = -math.inf
        if depth_limit == 2 or field.active_pokemon_oppo.non_volatile_status == StatusType.Fnt or len(
                dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                      field.active_pokemon_bot.name != x[1].name,
                            field.all_pkmns_oppo.items()))) == 0:

            return eval_fn(field)
        else:
            # If there is not pokemon known from the oppo
            if len(field.all_pkmns_oppo) == 1:
                # For each bot move
                for bot_move in field.active_pokemon_bot.moves:
                    # For each opponent known move

                    for oppo_moves in field.active_pokemon_oppo.moves:
                        new_state = IterativeDeepeningMinMax.create_state(field, bot_move, True, oppo_moves, True)
                        # BOTH MOVES
                        value = max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, depth_limit + 1), value)

                    # For each not known move of the opponent
                    for possible_oppo_moves in field.active_pokemon_oppo.possible_moves:
                        new_state = IterativeDeepeningMinMax.create_state(field, bot_move, True, possible_oppo_moves, True)
                        value = max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, depth_limit + 1), value)

                # All possibles switch WE SWITCH HE ATTACC
                for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                        field.active_pokemon_bot.name != x[1].name,
                                              field.all_pkmns_bot.items())):
                    # For each kno
                    for oppo_moves in field.active_pokemon_oppo.moves:
                        new_state = IterativeDeepeningMinMax.create_state(field, index_pkmn, False, oppo_moves, True)
                        value = max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, depth_limit + 1), value)
                    # For each not known move of the opponent
                    for possible_oppo_moves in field.active_pokemon_oppo.possible_moves:
                        new_state = IterativeDeepeningMinMax.create_state(field, index_pkmn, False, possible_oppo_moves, True)
                        value = max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, depth_limit + 1), value)
            else:

                # HE SWITCH AND WE ATTAC
                for index_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                        field.active_pokemon_bot.name != x[1].name,
                                              field.all_pkmns_oppo.items())):

                    for bot_move in field.active_pokemon_bot.moves:
                        new_state = IterativeDeepeningMinMax.create_state(field, bot_move, True, index_pkmn, False)
                        value = max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, depth_limit + 1), value)

                    # BOTH SWITCH
                    for index_bot_pkmn in dict(filter(lambda x: x[1].non_volatile_status is not StatusType.Fnt and
                                                                field.active_pokemon_bot.name != x[1].name,
                                                      field.all_pkmns_bot.items())):
                        new_state = IterativeDeepeningMinMax.create_state(field, index_bot_pkmn, False, index_pkmn, False)
                        value = max(IterativeDeepeningMinMax.max_value(new_state, eval_fn, depth_limit + 1), value)

            return value

    @staticmethod
    def create_state(field, move1, is_move1, move2, is_move_2):
        new_field = field.deepcopy()
        if not is_move1 and not is_move_2:
            new_field.switch_pokemon(1, move1)
            new_field.switch_pokemon(2, move2)
        elif is_move1 and not is_move_2:
            new_field.switch_pokemon(2, move2)
            new_field.do_move(1, move1)
            # check fainted
        elif not is_move1 and is_move_2:
            new_field.switch_pokemon(1, move1)
            new_field.do_move(2, move2)
            # check fainted
        else:
            if field.active_pokemon_bot.stats.get_actual(StatsType.Spe) > field.active_pokemon_oppo.stats.get_actual(
                    StatsType.Spe):
                new_field.do_move(1, move1)
                new_field.do_move(2, move2)
                if field.active_pokemon_bot.non_volatile_status == StatusType.Fnt:
                    new_field.switch_pokemon(1, switch_help(field))
            else:
                new_field.do_move(2, move2)
                if field.active_pokemon_bot.non_volatile_status == StatusType.Fnt:
                    new_field.switch_pokemon(1, switch_help(field))
                else:
                    new_field.do_move(1, move1)
        return new_field
