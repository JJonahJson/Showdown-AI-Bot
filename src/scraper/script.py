with open("pokemon.json", "r") as old_json:
    for line in old_json.read().splitlines():
        if "species" in line:
            print(line)
        elif "types" in line:
            print(line)
        elif "baseStats" in line:
            print(line)
        elif "num" in line:
            print(line)
        elif "abilities" in line:
            print(line)
        elif "weightkg" in line:
            print(line.replace(',',''))
        elif "}" in line:
            print(line)
        else:
            pkmn_name = line.split(":")[0].strip()
            quoted_line = line.replace(pkmn_name,'"{}"'.format(pkmn_name))
            print(quoted_line)

