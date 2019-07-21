import json

from src.model.field import BattleFieldSingle
from src.model.pokemon import Pokemon
from src.model.stats import Stats
from src.model.status import StatusType


def get_active_moves(moves_list, db_connection):
    active_moves = []
    for move in moves_list:
        move = db_connection.get_move_by_name(move["name"].replace("'", ''))
        move.pp = move["pp"]
        active_moves.append(move)
    return active_moves


def get_pokemons(pokemon_list, db_connection, active_moves, battle_id):
    active_pokemon_bot = None
    bench_bot = {}
    counter = 1

    for pokemon in pokemon_list["pokemon"]:
        # Parse the pokemon's stats
        stats_dict = pokemon["stats"]
        cond = pokemon["condition"].split()
        stats = Stats(int(cond[0].split("/")[0]),
                      stats_dict["atk"],
                      stats_dict["def"],
                      stats_dict["spa"],
                      stats_dict["spe"],
                      stats_dict["spd"],
                      int(pokemon["details"].split(",").strip().replace("L", "")),
                      is_base=False)

        if len(cond) > 1:
            status = StatusType[cond[1].capitalize()]
        else:
            status = StatusType.Normal
        pkmn_name = pokemon["ident"].split(":")[1].strip()
        pkmn_type = db_connection.get_pokemontype_by_name(pkmn_name)
        level = pokemon["details"].split(",")[1].strip().replace("L", "")
        if pokemon["active"]:
            gender = pokemon["details"].split(",")[2].strip()
            active_pokemon_bot = Pokemon(pkmn_name,
                                         pkmn_type,
                                         gender,
                                         stats,
                                         active_moves,
                                         [],
                                         0.00,  # TODO: Get weight from db
                                         status,
                                         [],
                                         level)
            bench_bot[counter] = active_pokemon_bot
            counter += 1
        else:
            moves = []
            for move in pokemon["moves"]:
                moves.append(db_connection.get_move_by_name(move))
                pokemon = Pokemon(pkmn_name,
                                  pkmn_type,
                                  gender,
                                  stats,
                                  active_moves,
                                  [],
                                  0.00,  # TODO: Get weight from db
                                  status,
                                  [],
                                  level)
                bench_bot[counter] = pokemon
                counter += 1

    return active_pokemon_bot, bench_bot


def parse_and_set(message, db_connection):
    pokemon_json = json.loads(message)
    pokemons = {1: {}, 2: {}}
    counter = {1: 1, 2: 1}
    # TODO: Check the index of move 1 or 0?!
    moves = get_active_moves(pokemon_json["active"]["moves"])
    active_pokemon_bot, bench_active= get_pokemons(
        pokemon_json["side"], db_connection, moves
    )
    return active_pokemon_bot, bench_active
