import json
import random
import time

import src.protocol.login as login
import src.protocol.request_parser as rp
import src.protocol.senders as sender
import src.protocol.state_update as su
from src.protocol.enemy_updater import update_enemy_pokemon
from src.model.field import BattleFieldSingle
from src.protocol.data_source import DatabaseDataSource


class GameLoop:

    def __init__(self, ws):
        self.ws = ws
        self.battle_field = BattleFieldSingle(None, None, {}, {})
        with open("standard_answers", "r") as file:
            self.standard_answers = file.readlines()
        self.db = DatabaseDataSource()

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
            if to_parse["games"] and self.battle_field.room_name == "":
                for k in to_parse["games"]:
                    if "battle" in k:
                        self.battle_field.room_name = k
                        break

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
                num_answer = random.randint(0, len(self.standard_answers))
                await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])
                time.sleep(3)
                await sender.sender(self.ws, self.battle_field.room_name, "/timer on")
            elif current[1] == "player" and len(current) > 3 and current[3].lower() == "tapulabu":
                # init del player id
                self.battle_field.player_id = "p1"

            elif current[1] == "switch" and self.battle_field.battle_id not in current[2]:
                # Handle the pokemons of the opponent
                name = current[2].split(":")[1].strip()
                level = int(current[3].split(",")[1].replace("L", "").strip())
                gender = current[3].split(",")[2].strip()
                update_enemy_pokemon(self.battle_field, self.db, name, level, gender)
            elif current[1] == "request":
                if current[2] == '':
                    continue
                if len(current[2]) == 1:
                    try:
                        # Populate the team
                        # await battle.req_loader(current[3].split('\n')[1], self.ws)
                        active, bench = rp.parse_and_set(current[3].splitlines()[1], self.db)
                        self.battle_field.active_pokemon_bot = active
                        self.battle_field.all_pkmns_bot = bench
                        self.battle_field.bench_selector_side[1] = bench
                        self.battle_field.active_selector_side[1] = active
                    except KeyError as e:
                        print(e)
                        print(current[3])
                else:
                    # Populate team
                    active, bench = rp.parse_and_set(current[3].splitlines()[1], self.db)
                    self.battle_field.active_pokemon_bot = active
                    self.battle_field.all_pkmns_bot = bench
                    self.battle_field.bench_selector_side[1] = bench
                    self.battle_field.active_selector_side[1] = active

            elif current[1] == "teampreview":
            # TODO: IA Knapsack which pokemon do we carry
            # await battle.make_team_order(self.ws)

            elif current[1] == "turn":
                # TODO: Call IA to decide which action to do
                # An action is a move or a switch
                await battle.make_action(self.ws)

            elif current[1] == "callback" and current[2] == "trapped":
                # We cannot switch so we can only make a move
                await battle.make_move(self.ws)

            elif current[1] == "win":
                # Win state, leave the room
                await sender.sendmessage(self.ws, self.battle_field.player_id, "Well done, have a nice day!")
                await sender.leaving(self.ws, self.battle_field.player_id)
            elif current[1] == "c":
                # This is a message
                num_answer = random.randint(0, len(self.standard_answers))
                await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])
            else:
                su.update_state(current, self.battle_field)
                pass
