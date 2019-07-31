import json

top_string = "INSERT INTO Abilities (id, name, weather, modify_stat, stat, value, target, type)"


result = ''
result += top_string


quoter = "'{}'".format
tupler = "({}),\n".format


abi_file = open("abilities.json", "r")
abi_dict = json.load(abi_file)
abi_file.close()


for abi in abi_dict:
    id_abi = quoter(abi_dict[abi]["id"].strip())
    name = quoter(abi_dict[abi]["name"].strip())

    if "weather" in abi_dict[abi]:
        weather = quoter(abi_dict[abi]["weather"].strip())
    else:
        weather = "null"

    if "modify_stat" in abi_dict[abi]:
        modify_stat = quoter(abi_dict[abi]["modify_stat"].strip())
    else:
        modify_stat = "null"

    if "multiplier" in abi_dict[abi]:
        multiplier = str(abi_dict[abi]["multiplier"])
    else:
        multiplier = "null"

    if "stat" in abi_dict[abi]:
        stat = quoter(abi_dict[abi]["stat"])
    else:
        stat = "null"

    if "value" in abi_dict[abi]:
        value = str(abi_dict[abi]["value"])
    else:
        value = "null"

    if "target" in abi_dict[abi]:
        target = quoter(abi_dict[abi]["target"].strip())
    else:
        target = "null"

    if "type" in abi_dict[abi]:
        type_abi = quoter(abi_dict[abi]["type"].strip())
    else:
        type_abi = "null"

    lista = [id_abi, name, weather, modify_stat, multiplier, stat, value, target, type_abi]
    stringona = ','.join(lista)
    result+=tupler(stringona)

print(result[:len(result)-2]+";")
    
