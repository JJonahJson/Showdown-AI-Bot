import json
import random
import time

import src.protocol.login as login
import src.protocol.request_parser as rp
import src.protocol.senders as sender
import src.protocol.state_update as su
from ai.chooser import Chooser
from ai.damage_tracker import DamageTracker
from src.model.field import BattleFieldSingle
from src.protocol.data_source import DatabaseDataSource
from src.protocol.enemy_updater import update_enemy_move, update_enemy_pokemon


class GameLoop:

    def __init__(self, ws):
        self.ws = ws
        self.battle_field = BattleFieldSingle(None, None, {}, {})
        with open("standard_answers", "r") as file:
            self.standard_answers = file.readlines()
        self.db = DatabaseDataSource()
        self.damage_tracker = DamageTracker()
        self.last_move = ""
        self.counter = 0

    async def challenge_loop(self, message):
        string_tab = message.split("|")
        if string_tab[1] == "challstr":
            # Login
            await login.log_in(self.ws, string_tab[2], string_tab[3])

        elif string_tab[1] == "updateuser" and string_tab[2] == " tapulabu":
            # Once we are connected.
            await sender.challenge(self.ws, "errevas", "gen7randombattle")

        elif "updatechallenges" in string_tab[1]:
            # If somebody challenges the bot
            try:
                if string_tab[2].split('\"')[3] != "challengeTo":
                    if string_tab[2].split('\"')[5] in "gen7randombattle":
                        await sender.sender(self.ws, "", "/accept " + string_tab[2].split('\"')[3])
                    else:
                        await sender.sender(self.ws, "", "/reject " + string_tab[2].split('\"')[3])
                        await sender.sender(self.ws, "", "/pm " + string_tab[2].split('\"')[3]
                                            + ", Sorry, I am designed only for randombattles")
            except KeyError:
                pass

        elif string_tab[1] == "pm" and "tapulabu" not in string_tab[2]:
            if string_tab[4] == ".info":
                await sender.sender(self.ws, "", "/pm " + string_tab[2] + ", Showdown Battle Bot active")
            await sender.sender(self.ws, "", "/pm " + string_tab[2] + ", Bring it on.")

        elif string_tab[1] == "updatesearch":
            to_parse = json.loads(string_tab[2])
            if to_parse["games"]:
                for k in to_parse["games"]:
                    if "battle" in k:
                        self.battle_field.room_name = k

        if "battle" in string_tab[0]:
            #   Battle concern message.
            await self.game_loop(message)

    async def game_loop(self, message):
        lines = message.splitlines()
        for line in lines[1:]:
            if line == '':
                continue
            current = line.split('|')
            if current[1] == "init":
                num_answer = random.randint(0, len(self.standard_answers) - 1)
                await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])
                time.sleep(3)
                await sender.sender(self.ws, self.battle_field.room_name, "/timer on")
            elif current[1] == "player" and len(current) > 3 and current[3].lower() == "tapulabu":
                # init del player id
                self.battle_field.player_id = current[2]
                # TODO: Check if the server init of turn numbers
                if "2" in current[2]:
                    self.battle_field.turn_number = 1
                else:
                    self.battle_field.turn_number = 0
            elif current[1] == "-damage":
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

            elif current[1] == "switch":
                # Handle the pokemons of the opponent
                if self.battle_field.player_id not in current[2]:
                    name = current[2].split(":")[1].strip()
                    level = int(current[3].split(",")[1].replace("L", "").strip())
                    if len(current[3].split(",")) == 3:
                        gender = current[3].split(",")[2].strip()
                    else:
                        gender = ""
                    update_enemy_pokemon(self.battle_field, self.db, name, level, gender)

            elif current[1] == "move":
                # Update the moveset of the active pokemon
                if self.battle_field.player_id not in current[2]:
                    move_name = current[3].strip()
                    self.last_move = move_name
                    update_enemy_move(self.battle_field, self.db, move_name)
            elif current[1] == "request":
                if "forceSwitch" in current[2]:
                    self.battle_field.turn_number = json.loads(current[2])["rqid"]
                    index = Chooser.choose_switch(self.battle_field)
                    await sender.sendswitch(self.ws, self.battle_field.room_name, index,
                                            self.battle_field.turn_number)
                    break
                if "wait" in current[2]:
                    self.battle_field.turn_number = json.loads(current[2])["rqid"]
                    break
                if current[2] == '':
                    continue
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
                    except KeyError as e:
                        print(e)
                        print(current[3])
                else:
                    # Populate team
                    active, bench, id = rp.parse_and_set(current[2], self.db)
                    self.battle_field.active_pokemon_bot = active
                    self.battle_field.all_pkmns_bot = bench
                    self.battle_field.turn_number = id
                    self.battle_field.bench_selector_side[1] = bench
                    self.battle_field.active_selector_side[1] = active

            elif current[1] == "teampreview":
                # TODO: IA Knapsack which pokemon do we carry
                # await battle.make_team_order(self.ws)
                pass
            elif current[1] == "turn":
                # TODO: Call IA to decide which action to do
                # An action is a move or a switch
                move = Chooser.choose_move(self.battle_field)
                await sender.sendmove(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number)

            elif current[1] == "callback" and current[2] == "trapped":
                # We cannot switch so we can only make a move
                move = Chooser.choose_move(self.battle_field)
                await sender.sendmove(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number)


            elif current[1] == "win":
                # Win state, leave the room
                await sender.sendmessage(self.ws, self.battle_field.player_id, "Well done, have a nice day!")
                await sender.leaving(self.ws, self.battle_field.player_id)
                exit(1)

            elif current[1] == "c" and "tapulabu" not in current[2]:
                # This is a message
                num_answer = random.randint(0, len(self.standard_answers) - 1)
                await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])
            else:
                su.update_state(current, self.battle_field)
                pass
