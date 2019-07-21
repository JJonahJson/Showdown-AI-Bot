from src.model.move import SingleMove
from src.model.stats import Stats
from src.model.status import StatusType
from src.model.pokemon import Pokemon
from src.model.field import BattleFieldSingle

import json


def parse_and_set(message):
    pokemon_json = json.loads(message)
    # TODO: Add a component that retrieve the move from a db then we can parse the movesù

    battle_field = BattleFieldSingle(None, None, None, None)
    pokemons = {1: {}, 2: {}}
    counter = {1: 1, 2: 1}
    for pokemon in pokemon_json["side"]["pokemon"]:
        name = pokemon["ident"].split(":")[1].strip()
        hp = pokemon["condition"].split("/")[0].strip()
        sex = pokemon["details"].split(",")[2][1].strip()
        lv = int(pokemon["details"].split(",")[1][2:].strip())

        # Parsing stats
        atk = pokemon["stats"]["atk"]
        defense = pokemon["stats"]["def"]
        spa = pokemon["stats"]["spa"]
        spd = pokemon["stats"]["spd"]
        spe = pokemon["stats"]["spe"]

        stat = Stats(hp, atk, defense, spa, spd, spe, )

        # Item & Ability
        ability_name = pokemon["baseAbility"]
        item_name = pokemon["item"]

        # TODO: Need pokemon type, db
        pokemon_obj = Pokemon(name, None, sex, stat, None, 20, StatusType.Normal, [], None, None, lv)

        if pokemon_json["side"]["name"] == "tapulabu":
            side = 1
        else:
            side = 2

        if pokemon["active"] and side == 1:
            battle_field.active_pokemon_bot = pokemon_obj

        else:
            battle_field.active_pokemon_oppo = pokemon_obj

        battle_field.active_selector_side[side] = pokemon_obj

        pokemons[counter[side]][side] = pokemon_obj
        counter[side] += 1

    battle_field.all_pkmns_bot = pokemons[1]
    battle_field.all_pkmns_oppo = pokemons[2]
    return battle_field
