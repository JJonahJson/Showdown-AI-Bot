from model.field import BattleFieldSingle


def update_enemy_pokemon(battle_field: BattleFieldSingle, db_con, pokemon_name: str, level: int, gender: str):
    """Function that updates the current available pokemons of the opponet
    :param battle_field: BattleField object
    :param db_con: A db connection
    :param pokemon_name: A pokemon name
    :param level: The pokemon level
    :param gender: The gender
    :return:
    """
    # If the oppo doesn't have pokemons
    if not battle_field.all_pkmns_oppo:
        # Add the pokemon
        pokemon = db_con.get_pokemon_by_name(pokemon_name, level)
        pokemon.gender = gender
        battle_field.active_pokemon_oppo = pokemon
        battle_field.active_selector_side[2] = pokemon
        battle_field.all_pkmns_oppo[1] = pokemon
    else:
        # if the pokmemon name is not in the all pokemon dict
        if pokemon_name not in list(map(lambda x: x[1].name, battle_field.all_pkmns_oppo.items())):
            # add the pokemon
            pokemon = db_con.get_pokemon_by_name(pokemon_name, level)
            current_index = max(battle_field.all_pkmns_oppo.keys())
            battle_field.all_pkmns_oppo[current_index + 1] = pokemon
            battle_field.switch_pokemon(2, current_index + 1)
        else:
            # We need to switch the pokemom without adding it to the all_pkmns dict
            for index in battle_field.all_pkmns_oppo:
                if battle_field.all_pkmns_oppo[index].name == pokemon_name:
                    battle_field.switch_pokemon(2, index)


def update_enemy_move(battle_field: BattleFieldSingle, db_con, move_name):
    """Method that updates the moveset of the opponent's active pokemon.
    :param battle_field: Battlefield object
    :param db_con: A database connection
    :param move_name: A move name
    :return:
    """
    if not battle_field.active_pokemon_oppo.moves:
        move = db_con.get_move_by_name(move_name.replace(" ", "").replace("-", "").replace(".", "").lower())
        if move:
            battle_field.active_pokemon_oppo.moves[1] = move
    elif move_name not in list(map(lambda x: x[1].move_name, battle_field.active_pokemon_oppo.moves.items())):
        move = db_con.get_move_by_name(move_name.replace(" ", "").replace("-", "").replace(".", "").lower())
        if move:
            current_index = max(battle_field.active_pokemon_oppo.moves.keys())
            battle_field.active_pokemon_oppo.moves[current_index + 1] = move


22
