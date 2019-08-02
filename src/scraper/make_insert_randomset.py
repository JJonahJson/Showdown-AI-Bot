import json

top_string = "INSERT INTO Randomsets (pokemon, battle_type, move) VALUES\n"

quoter = "'{}'".format
tupler = "({}),\n".format

result = ""
result += top_string

json_file = open("randomsets.json")
randomset_dict = json.load(json_file)
json_file.close()

for pokemon in randomset_dict:
    for battle_type in randomset_dict[pokemon]:
        for move in randomset_dict[pokemon][battle_type]:
            if "Double" in battle_type:
                battle_type = "Double"
            else:
                battle_type = "Single"
            result+="('{}', '{}', '{}'),\n".format(pokemon, battle_type, move)

print(result[:len(result)-2]+";")
