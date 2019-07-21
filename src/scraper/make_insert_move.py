import json

top_string = "INSERT INTO Moves (num, name, id_name, accuracy, base_power, category, pp, priority, chance, volatile_status, non_volatile_status, boost_atk, boost_def, boost_spa, boost_spd, boost_spe, boost_acc, boost_eva, target, move_type) VALUES\n"


filler = "({}),\n"

quoter = "'{}'"

result = ''

result += top_string

move_file = open("moves.json", "r")
moves = json.load(move_file)
move_file.close()

for move in moves:
   #print(move)
    if "num" in moves[move]:
        num = moves[move]["num"]
    else:
        num = 0
    name = quoter.format(moves[move]["name"].replace("'", ""))
    id_name = quoter.format(moves[move]["id"])
    accuracy = moves[move]["accuracy"]
    if accuracy == True:
        accuracy = 100
    base_power = moves[move]["basePower"]
    category = quoter.format(moves[move]["category"])
    pp = moves[move]["pp"]
    priority = moves[move]["priority"]
    if "chance" in moves[move]:
        chance = moves[move]["chance"]
    else:
        chance = 100

    if "volatileStatus" in moves[move]:
        volatile_status = quoter.format(moves[move]["volatileStatus"])
    else:
        volatile_status = "null"

    if "status" in moves[move]:
        non_volatile_status = quoter.format(moves[move]["status"])
    else:
        non_volatile_status = "null"

    if "boosts" in moves[move]:
        boosts = moves[move]["boosts"]
        if "atk" in boosts:
            boost_atk = boosts["atk"]
        else:
            boost_atk = 0

        if "def" in boosts:
            boost_def = boosts["def"]
        else:
            boost_def = 0
   
        if "spa" in boosts:
            boost_spa = boosts["spa"]
        else:
            boost_spa = 0
        
        if "spd" in boosts:
            boost_spd = boosts["spd"]
        else:
            boost_spd = 0

        if "spe" in boosts:
            boost_spe = boosts["spe"]
        else:
            boost_spe = 0

        if "accuracy" in boosts:
            boost_acc = boosts["accuracy"]
        else:
            boost_acc = 0

        if "evasion" in boosts:
            boost_eva = boosts["evasion"]
        else:
            boost_eva = 0

    else:
        boost_atk = 0
        boost_def = 0
        boost_spa = 0
        boost_spd = 0
        boost_spe = 0
        boost_acc = 0
        boost_eva = 0

    target = quoter.format(moves[move]["target"])
    move_type = quoter.format(moves[move]["type"])

    lista = [str(num), name, id_name, str(accuracy), str(base_power), category, str(pp), str(priority), str(chance), volatile_status, non_volatile_status, str(boost_atk), str(boost_def), str(boost_spa), str(boost_spd), str(boost_spe), str(boost_acc), str(boost_eva), target, move_type]
    to_insert = ','.join(lista)
    result+=filler.format(to_insert)

to_print = result[:len(result)-2]
print(to_print+';')
