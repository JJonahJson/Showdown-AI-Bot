from src.model.field import BattleFieldSingle


def update_enemy_pokemon(battle_field: BattleFieldSingle, db_con, pokemon_name: str, level: int, gender: str):
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
            battle_field.all_pkmns_oppo[current_index+1] = pokemon
            battle_field.switch_pokemon(2, current_index+1)
        else:
            # We need to switch the pokemom without adding it to the all_pkmns dict
            for index in battle_field.all_pkmns_oppo:
                if battle_field.all_pkmns_oppo[index].name == pokemon_name:
                    battle_field.switch_pokemon(2, index)


# TODO: Add update_enemy_move