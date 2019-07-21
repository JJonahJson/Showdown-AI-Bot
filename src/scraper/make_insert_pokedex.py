import json

top_string = "INSERT INTO Pokemon (num, name, hp, atk, def, spa, spd, spe, type_1, type2_weight) VALUES\n"


filler = "({}),\n"

quoter = "'{}'"

result = ''

result += top_string

pokemon_file = open("pokedex.json", "r")
pokemons = json.load(pokemon_file)
pokemon_file.close()

for pkmn_name in pokemons:
    num = pokemons[pkmn_name]["num"]
    name = quoter.format(pokemons[pkmn_name]["species"])
    if len(pokemons[pkmn_name]["types"]) == 2:
        type_1 = quoter.format(pokemons[pkmn_name]["types"][0])
        type_2 = quoter.format(pokemons[pkmn_name]["types"][1])
    else:
        type_1 = quoter.format(pokemons[pkmn_name]["types"][0])
        type_2 = "null"
    hp = pokemons[pkmn_name]["baseStats"]["hp"]
    atk = pokemons[pkmn_name]["baseStats"]["atk"]
    defense = pokemons[pkmn_name]["baseStats"]["def"]
    spa = pokemons[pkmn_name]["baseStats"]["spa"]
    spd = pokemons[pkmn_name]["baseStats"]["spd"]
    spe = pokemons[pkmn_name]["baseStats"]["spe"]
    weight = pokemons[pkmn_name]["weightkg"]
    lista = [str(num), name, str(hp), str(atk), str(defense), str(spa), str(spd), str(spe), type_1, type_2, str(weight)]
    to_insert = ','.join(lista)
    result+=filler.format(to_insert)

to_print = result[:len(result)-2]
print(to_print+';')
