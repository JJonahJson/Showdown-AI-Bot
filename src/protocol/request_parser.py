import json

from model.pokemon import Pokemon
from model.stats import Stats
from model.status_type import StatusType


def get_active_moves(moves_list, db_connection):
    active_moves = {}
    index = 1
    for move in moves_list:
        move_retrieved = db_connection.get_move_by_name(move["id"].replace("'", ''))
        if "pp" in move.keys():
            move_retrieved.pp = move["pp"]
        else:
            move_retrieved.pp = 1
        active_moves[index] = move_retrieved
        if "disabled" in move.keys():
            active_moves[index].is_usable = not move["disabled"]
        index += 1
    return active_moves


def get_pokemons(pokemon_list, db_connection, active_moves):
    active_pokemon_bot = None
    bench_bot = {}
    counter = 1

    for pokemon in pokemon_list["pokemon"]:
        # Parse the pokemon's stats
        stats_dict = pokemon["stats"]
        cond = pokemon["condition"].split()
        splitted_details = pokemon["details"].split(",")

        if len(splitted_details) == 3:
            # Normal case
            level = int(splitted_details[1].replace("L","").strip())
            gender = splitted_details[2].strip()
        else:
            if "L" in splitted_details[1]:
                level = int(splitted_details[1].replace("L","").strip())
                gender = ""
            else:
                level = 75
                gender = splitted_details[1].replace("L","").strip()

        stats = Stats(int(cond[0].split("/")[0]),
                      stats_dict["atk"],
                      stats_dict["def"],
                      stats_dict["spa"],
                      stats_dict["spd"],
                      stats_dict["spe"],
                      level,
                      is_base=False)

        if len(cond) > 1:
            status = StatusType[cond[1].capitalize()]
        else:
            status = StatusType.Normal
        pkmn_name = pokemon["ident"].split(":")[1].strip()
        pkmn_type = db_connection.get_pokemontype_by_name(pkmn_name)
        level = int(pokemon["details"].split(",")[1].strip().replace("L", ""))
        if pokemon["active"]:
            if len(pokemon["details"].split(",")) > 2:
                if "Castform" not in pkmn_name:
                    gender = pokemon["details"].split(",")[2].strip()
                else:
                    gender = pokemon["details"].split(",")[1].strip()
            else:
                gender = ""
            active_pokemon_bot = Pokemon(pkmn_name,
                                         pkmn_type,
                                         gender,
                                         stats,
                                         active_moves,
                                         [],
                                         0.00,  # TODO: Get weight from db
                                         status,
                                         [],
                                         None,
                                         level)
            bench_bot[counter] = active_pokemon_bot
            counter += 1
        else:
            moves = {}
            index = 1
            for move in pokemon["moves"]:
                moves[index] = db_connection.get_move_by_name(move)
                index += 1
            pokemon = Pokemon(pkmn_name,
                              pkmn_type,
                              gender,
                              stats,
                              active_moves,
                              [],
                              0.00,  # TODO: Get weight from db
                              status,
                              [],
                              None,
                              level)
            bench_bot[counter] = pokemon
            counter += 1

    return active_pokemon_bot, bench_bot


def parse_and_set(message, db_connection):
    pokemon_json = json.loads(message)
    pokemons = {1: {}, 2: {}}
    counter = {1: 1, 2: 1}
    # TODO: Check the index of move 1 or 0?!
    moves = get_active_moves(pokemon_json["active"][0]["moves"], db_connection)
    active_pokemon_bot, bench_active = get_pokemons(
        pokemon_json["side"], db_connection, moves
    )
    return active_pokemon_bot, bench_active, pokemon_json["rqid"]
