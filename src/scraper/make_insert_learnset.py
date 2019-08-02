import json

top_string = "INSERT INTO Learnsets (id, name) VALUES\n"

quoter = "'{}'".format
tupler = "({}),\n".format


result = ""
result += top_string

json_file = open("learnsets.json")
learnset_dict = json.load(json_file)
json_file.close()


for pokemon in learnset_dict:
    for move in learnset_dict[pokemon]:
        result+="('{}', '{}'),\n".format(pokemon, move)

print(result[:len(result)-2]+";")
