from src.model.field import Field
from src.model.status import StatusType


def update_state(line, field):
    if line[0] == "move":
        pass
    elif line[0] == "switch":
        if field.player_id not in line[1]:
            field.switch_pokemon(2, field.get_pokemon_index_by_name(2, line[2].split(',')[0]))
    elif line[0] == "swap":
        pass
    elif line[0] == "detailschange":
        pass
    elif line[0] == "cant":
        pass
    elif line[0] == "faint":
        if field.player_id not in line[1]:
            field.active_pokemon_bot.status = StatusType.Fainted
        else:
            field.active_pokemon_oppo.status = StatusType.Fainted
    if line[0] == "-fail":
        pass
    elif line[0] == "-damage":
        if field.player_id in line[1]:
            field.update_damage(1, int(line[2].split("/")[0]))
        else:
            field.update_damage(2, int(line[2].split("/")[0]))
    elif line[0] == "-heal":
        if field.player_id in line[1]:
            field.update_heal(1, int(line[2].split("/")[0]))
        else:
            field.update_heal(2, int(line[2].split("/")[0]))
    elif line[0] == "-status":
        if field.player_id in line[1]:
            field.update_status(1, line[2])
        else:
            field.update_status(2, line[2])
    elif line[0] == "-curestatus":
        if field.player_id in line[1]:
            field.update_status(1)
        else:
            field.update_status(2)
    elif line[0] == "-cureteam":
        pass
    elif line[0] == "-boost":
        if field.player_id in line[1]:
            field.update_buff(1, line[2], int(line[3]))
        else:
            field.update_buff(2, line[2], int(line[3]))
    elif line[0] == "-unboost":
        if field.player_id in line[1]:
            field.update_buff(1, line[2], - int(line[3]))
        else:
            field.update_buff(2, line[2], - int(line[3]))
    elif line[0] == "-weather":
        field.update_weather(line[2])
    elif line[0] == "-fieldstart":
        field.update_field(line[2])
    elif line[0] == "-fieldend":
        field.update_field(Field.Normal)
    elif line[0] == "-supereffective":
        pass
    elif line[0] == "-resisted":
        pass
    elif line[0] == "-immune":
        pass
    elif line[0] == "-item":
        pass
    elif line[0] == "-enditem":
        pass
    elif line[0] == "-ability":
        pass
    elif line[0] == "-endability":
        pass
    elif line[0] == "-transform":
        pass
    elif line[0] == "-mega":
        pass
    elif line[0] == "-activate":
        pass
    elif line[0] == "-hint":
        pass
    elif line[0] == "-center":
        pass
    elif line[0] == "-message":
        pass
    else:
        pass
