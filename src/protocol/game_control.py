import json
import random
import time

import protocol.login as login
import protocol.request_parser as rp
import protocol.senders as sender
from ai.chooser import Chooser
from ai.damage_tracker import DamageTracker
from model.field import BattleFieldSingle
from model.field_type import Field
from model.status import Status
from model.status_type import StatusType
from protocol.data_source import DatabaseDataSource
from protocol.enemy_updater import update_enemy_move, update_enemy_pokemon


class GameLoop:

    def __init__(self, ws, user_name, password, opponent_name):
        self.ws = ws
        self.user_name = user_name
        self.password = password
        self.opponent_name = opponent_name
        self.battle_field = BattleFieldSingle(None, None, {}, {})
        with open("standard_answers", "r") as file:
            self.standard_answers = file.readlines()
        self.db = DatabaseDataSource()
        self.damage_tracker = DamageTracker()
        self.last_move = ""
        self.counter = 0

        self.handler_challenge = {
            "challstr": self._handle_challstr,
            "updateuser": self._handle_update_user,
            "updatesearch": self._handle_update_search
        }

        self.handler_battle = {
            "init": self._handle_init,
            "player": self._handle_player,
            "-damage": self._handle_damage,
            "switch": self._handle_switch,
            "move": self._handle_move,
            "request": self._handle_request,
            "teampreview": self._handle_team_preview,
            "turn": self._handle_turn,
            "callaback": self._handle_callback,
            "win": self._handle_win,
            "c": self._handle_chat,
            "faint": self._handle_faint,
            "-heal": self._handle_heal,
            "-status": self._handle_status,
            "-curestatus": self._handle_curestatus,
            "-boost": self._handle_boost,
            "-unboost": self._handle_unboost,
            "-weather": self._handle_weather,
            "-fieldstart": self._handle_field_start,
            "-fieldend": self._handle_field_end

        }

    async def handle_message(self, message):
        splitted = message.split("|")
        if "battle" in splitted[0]:
            self.handler_battle[splitted[1]](splitted)
        else:
            lines = message.splitlines()
            for line in lines[1:]:
                if line == '':
                    continue
                current = line.split("|")
                self.handler_challenge[current[1]](current)

    async def _handle_challstr(self, string_tab):
        await login.log_in(self.ws, self.user_name, self.password, string_tab[2], string_tab[3])

    async def _handle_update_user(self, string_tab):
        if self.user_name in string_tab[2]:
            await sender.challenge(self.ws, self.opponent_name, "gen7randombattle")

    async def _handle_update_search(self, string_tab):
        to_parse = json.loads(string_tab[2])
        if to_parse["games"]:
            for k in to_parse["games"]:
                if "battle" in k:
                    self.battle_field.room_name = k
        print("If you want to follow the match go to this link https://play.pokemonshowdown.com/{}".format(
            self.battle_field.room_name))

    async def _handle_init(self, current):
        num_answer = random.randint(0, len(self.standard_answers) - 1)
        await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])
        time.sleep(3)

    async def _handle_player(self, current):
        if len(current) > 3 and current.lower() == self.user_name:
            self.battle_field.player_id = current[2]
            if "2" in current[2]:
                self.battle_field.turn_number = 1
            else:
                self.battle_field.turn_number = 0

    async def _handle_damage(self, current):
        if self.battle_field.player_id in current[2]:
            if 'fnt' not in current[3]:
                actual = int(current[3].split(" ")[0].split("/")[0].strip())
                total = int(current[3].split(" ")[0].split("/")[1].strip())
                damage_perc = round(actual / total)
                self.damage_tracker.add_damage(self.battle_field.active_pokemon_oppo, damage_perc,
                                               self.battle_field.active_pokemon_bot, self.last_move)

        else:
            if 'fnt' not in current[3]:
                damage_perc = int(current[3].split("/")[0].strip())
                self.damage_tracker.add_damage(self.battle_field.active_pokemon_bot, damage_perc,
                                               self.battle_field.active_pokemon_oppo, self.last_move)

    async def _handle_switch(self, current):
        if self.battle_field.player_id not in current[2]:
            name = current[2].split(":")[1].strip()
            level = int(current[3].split(",")[1].replace("L", "").strip())
            if len(current[3].split(",")) == 3:
                gender = current[3].split(",")[2].strip()
            else:
                gender = ""
            update_enemy_pokemon(self.battle_field, self.db, name, level, gender)

    async def _handle_move(self, current):
        if self.battle_field.player_id not in current[2]:
            move_name = current[3].strip()
            self.last_move = move_name
            update_enemy_move(self.battle_field, self.db, move_name)

    async def _handle_request(self, current):
        if "forceSwitch" in current[2]:
            self.battle_field.turn_number = json.loads(current[2])["rqid"]
            index = Chooser.choose_switch(self.battle_field)
            await sender.sendswitch(self.ws, self.battle_field.room_name, index,
                                    self.battle_field.turn_number)
            return
        if "wait" in current[2]:
            self.battle_field.turn_number = json.loads(current[2])["rqid"]
            return
        if current[2] == '':
            return
        if len(current[2]) == 1:
            try:
                # Populate the team
                # await battle.req_loader(current[3].split('\n')[1], self.ws)
                active, bench, id = rp.parse_and_set(current[2], self.db)
                self.battle_field.turn_number = id
                self.battle_field.active_pokemon_bot = active
                self.battle_field.all_pkmns_bot = bench
                self.battle_field.bench_selector_side[1] = bench
                self.battle_field.active_selector_side[1] = active
                print(self.battle_field.active_pokemon_bot.to_string())
            except KeyError as e:
                print(e)
                print(current[3])
        else:
            # Populate team
            active, bench, number = rp.parse_and_set(current[2], self.db)
            self.battle_field.active_pokemon_bot = active
            self.battle_field.all_pkmns_bot = bench
            self.battle_field.turn_number = number
            self.battle_field.bench_selector_side[1] = bench
            self.battle_field.active_selector_side[1] = active
            print(self.battle_field.active_pokemon_bot.to_string())

    async def _handle_team_preview(self, current):
        pass

    async def _handle_turn(self, current):
        # An action is a move or a switch
        move = Chooser.choose_move(self.battle_field)
        await sender.sendmove(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number)

    async def _handle_callback(self, current):
        if current[2] == "trapped":
            move = Chooser.choose_move(self.battle_field)
            await sender.sendmove(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number)

    async def _handle_win(self, current):
        await sender.sendmessage(self.ws, self.battle_field.room_name, "Well done, have a nice day!")
        await sender.leaving(self.ws, self.battle_field.room_name)
        exit(1)

    async def _handle_chat(self, current):
        if self.user_name not in current[2]:
            num_answer = random.randint(0, len(self.standard_answers) - 1)
            await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])

    async def _handle_faint(self, current):
        """faint"""
        if self.battle_field.player_id not in current[1]:
            Status.apply_non_volatile_status(StatusType.Fnt, self.battle_field.active_pokemon_bot)
        else:
            Status.apply_non_volatile_status(StatusType.Fnt, self.battle_field.active_pokemon_oppo)

    async def _handle_heal(self, current):
        """-heal"""
        if self.battle_field.player_id in current[1]:
            self.battle_field.update_heal(1, int(current[2].split("/")[0]))
        else:
            self.battle_field.update_heal(2, int(current[2].split("/")[0]))

    async def _handle_status(self, current):
        """-status"""
        if self.battle_field.player_id in current[1]:
            self.battle_field.update_status(1, current[2])
        else:
            self.battle_field.update_status(2, current[2])

    async def _handle_curestatus(self, current):
        """-curestatus"""
        if self.battle_field.player_id in current[1]:
            self.battle_field.update_status(1)
        else:
            self.battle_field.update_status(2)

    async def _handle_boost(self, current):
        """-boost"""
        if self.battle_field.player_id in current[1]:
            self.battle_field.update_buff(1, current[2], int(current[3]))
        else:
            self.battle_field.update_buff(2, current[2], int(current[3]))

    async def _handle_unboost(self, current):
        """-unboost"""
        if self.battle_field.player_id in current[1]:
            self.battle_field.update_buff(1, current[2], - int(current[3]))
        else:
            self.battle_field.update_buff(2, current[2], - int(current[3]))

    async def _handle_weather(self, current):
        """-weather"""
        self.battle_field.update_weather(current[2])

    async def _handle_field_start(self, current):
        """-fieldstart"""
        self.battle_field.update_field(current[2])

    async def _handle_field_end(self, current):
        """-fieldend"""
        self.battle_field.update_field(Field.Normal)
