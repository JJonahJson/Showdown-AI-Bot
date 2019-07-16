from src.model.field import Weather, Field


class BattleParser:

    def parse_major(self, line, field):
        if line[0] == "-fail":
            pass
        elif line[0] == "-damage":
            if field.player_id in line[1]:
                field.update_damage(1, int(line[2]))
            else:
                field.update_damage(2, int(line[2]))
        elif line[0] == "-heal":
            pass
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
            field.update_weather(Weather.to_string[line[2]])
        elif line[0] == "-fieldstart":
            field.update_field(Field.to_string[line[2]])
        elif line[0] == "-fieldend":
            field.update_field(Field.Normal)
        elif line[0] == "-supereffective":
            pass
        elif line[0] == "-resisted":
            pass
        elif line[0] == "-immune":
            pass
        elif line[0] == "-item":
            if field.player_id in line[1]:
                battle.bot_team.active().item = line[2].lower().replace(" ", "")
            else:
                battle.enemy_team.active().item = line[2].lower().replace(" ", "")
        elif line[0] == "-enditem":
            if battle.player_id not in line[1]:
                battle.bot_team.active().item = None
            else:
                battle.enemy_team.active().item = None
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


def parse_minor(self, line, field):
    pass


def parse(self, line, field):
    if line[0][0] != "-":
        parse_major(line, field)
    else:
        parse_minor(line, field)
