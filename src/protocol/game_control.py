import json
import random
import time

import protocol.login as login
import protocol.request_parser as rp
import protocol.senders as sender
from ai.chooser import Chooser
from ai.chooser_type import Difficulty
from ai.damage_tracker import DamageTracker
from model.field import BattleFieldSingle
from model.field_type import Field
from model.stats_type import StatsType
from model.status import Status
from model.status_type import StatusType
from protocol.data_source import DatabaseDataSource
from protocol.enemy_updater import update_enemy_move, update_enemy_pokemon


class GameLoop:
    """Main control class"""

    def __init__(self, ws, user_name, password, opponent_name, difficulty):
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
        self.chooser = Chooser(difficulty)

        self.bot_volatile = []
        self.oppo_volatile = []
        # TODO: Do same thing with volatile status
        self.mul_stats_bot = {
            StatsType.Atk: 0,
            StatsType.Def: 0,
            StatsType.Spa: 0,
            StatsType.Spd: 0,
            StatsType.Spe: 0,
            StatsType.Accuracy: 0,
            StatsType.Evasion: 0
        }
        self.mul_stats_oppo = {
            StatsType.Atk: 0,
            StatsType.Def: 0,
            StatsType.Spa: 0,
            StatsType.Spd: 0,
            StatsType.Spe: 0,
            StatsType.Accuracy: 0,
            StatsType.Evasion: 0
        }

        # Dict of handlers for the challenge section
        self.handler_challenge = {
            "challstr": self._handle_challstr,
            "updateuser": self._handle_update_user,
            "updatesearch": self._handle_update_search
        }

        # Dict of handlers of the battle section
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
            "-fieldend": self._handle_field_end,
            "-start": self._handle_start_vol,
            "-end": self._handle_end_vol

        }

    async def handle_message(self, message):
        """Main method of the class that dispatches and invokes the correct method
        :param message: The message received from the ws
        :return:
        """
        splitted = message.split("|")
        if "battle" not in splitted[0]:
            function = self.handler_challenge.get(splitted[1], self._handle_place_holder)
            await function(splitted)
        else:
            lines = message.splitlines()
            for line in lines[1:]:
                if line == '':
                    continue
                current = line.split("|")
                function = self.handler_battle.get(current[1], self._handle_place_holder)
                await function(current)

    async def _handle_place_holder(self, string_tab):
        """Placeholder function in case that the key is not in dict then do nothing.
        :param string_tab:
        :return:
        """
        pass

    async def _handle_challstr(self, string_tab):
        """Challstr message handler, when we receive challstr we can do the login procedure
        :param string_tab: message
        :return:
        """
        await login.log_in(self.ws, self.user_name, self.password, string_tab[2], string_tab[3])

    async def _handle_update_user(self, string_tab):
        """When we receive an updateuser means that we're ready to fight an opponent, so send the challenge
        :param string_tab:
        :return:
        """
        if self.user_name in string_tab[2]:
            await sender.challenge(self.ws, self.opponent_name, "gen7randombattle")

    async def _handle_update_search(self, string_tab):
        """Method that handles the creation of battle room and saves the room id and prints the link to watch the battle
        :param string_tab:
        :return:
        """
        to_parse = json.loads(string_tab[2])
        if to_parse["games"]:
            for k in to_parse["games"]:
                if "battle" in k:
                    self.battle_field.room_name = k
        print("If you want to follow the match go to this link https://play.pokemonshowdown.com/{}".format(
            self.battle_field.room_name))

    async def _handle_init(self, current):
        """Method that handles the first message of the communication with the showdown server
        :param current:
        :return:
        """
        num_answer = random.randint(0, len(self.standard_answers) - 1)
        await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])
        time.sleep(3)
        await sender.sender(self.ws, self.battle_field.room_name, "Send go {difficulty} if you want to change "
                                                                  "difficulty. Available difficulties are: easy, "
                                                                  "normal, hard!\n/timer on")

    async def _handle_player(self, current):
        """Method that handles the player message that saves our id and the opponent id
        :param current:
        :return:
        """
        if len(current) > 3 and current[3].lower() == self.user_name:
            self.battle_field.player_id = current[2]
            if "2" in current[2]:
                self.battle_field.turn_number = 1
            else:
                self.battle_field.turn_number = 0

    async def _handle_damage(self, current):
        """Method that handles the -damage message and updates the current hp of the pokemons
        :param current:
        :return:
        """
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
        """Method that handle the switch message and updates the current status of the battlefield
        :param current:
        :return:
        """
        if self.battle_field.player_id not in current[2]:
            name = current[2].split(":")[1].strip()
            level = int(current[3].split(",")[1].replace("L", "").strip())
            if len(current[3].split(",")) == 3:
                gender = current[3].split(",")[2].strip()
            else:
                gender = ""
            if self.battle_field.active_pokemon_oppo:
                for stats in self.battle_field.active_pokemon_oppo.stats.mul_stats:
                    self.battle_field.active_pokemon_oppo.stats.mul_stats[stats] = 0

            update_enemy_pokemon(self.battle_field, self.db, name, level, gender)
            for key in self.mul_stats_oppo:
                self.mul_stats_oppo[key] = 0
            self.oppo_volatile.clear()
            self.battle_field.active_pokemon_oppo.volatile_status.clear()
        else:
            for key in self.mul_stats_bot:
                self.mul_stats_bot[key] = 0
            self.bot_volatile.clear()

    async def _handle_move(self, current):
        """Method that handles the message move and updates the current moveset of the enemy
        :param current:
        :return:
        """
        if self.battle_field.player_id not in current[2]:
            move_name = current[3].strip()
            self.last_move = move_name
            update_enemy_move(self.battle_field, self.db, move_name)

    async def _handle_request(self, current):
        """Key method that handles the parsing of our team and saves the id of the next request
        :param current:
        :return:
        """
        if "forceSwitch" in current[2]:
            self.battle_field.turn_number = json.loads(current[2])["rqid"]
            index = self.chooser.choose_switch(self.battle_field)
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
                active, bench, number = rp.parse_and_set(current[2], self.db)
                self.battle_field.turn_number = number
                self.battle_field.active_pokemon_bot = active
                self.battle_field.all_pkmns_bot = bench
                self.battle_field.bench_selector_side[1] = bench
                self.battle_field.active_selector_side[1] = active
                for element in self.bot_volatile:
                    Status.add_volatile_status(element, self.battle_field.active_pokemon_bot)
                for key in self.mul_stats_bot:
                    self.battle_field.active_pokemon_bot.stats.mul_stats[key] = self.mul_stats_bot[key]
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
            for element in self.bot_volatile:
                Status.add_volatile_status(element, self.battle_field.active_pokemon_bot)
            for key in self.mul_stats_bot:
                self.battle_field.active_pokemon_bot.stats.mul_stats[key] = self.mul_stats_bot[key]
            print(self.battle_field.active_pokemon_bot.to_string())

    async def _handle_team_preview(self, current):
        """Method that handles the team preview message
        :param current:
        :return:
        """
        pass

    async def _handle_turn(self, current):
        """Method that handles the turn message which means that we can do a move, so we call the ai module
        :param current:
        :return:
        """
        # An action is a move or a switch
        move, is_move = self.chooser.choose_move(self.battle_field)
        if is_move:
            await sender.sendmove(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number,
                                  self.battle_field.active_pokemon_bot.can_mega,
                                  self.battle_field.active_pokemon_bot.moves[move].is_Z)
        else:
            await sender.sendswitch(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number)

    async def _handle_callback(self, current):
        """Method that handles the trapped state of the pokemon that cannot switch so he must do a move
        :param current:
        :return:
        """
        if current[2] == "trapped":
            move = self.chooser.choose_move(self.battle_field, True)
            await sender.sendmove(self.ws, self.battle_field.room_name, move, self.battle_field.turn_number)

    async def _handle_win(self, current):
        """Method that handles the win of the bot
        :param current:
        :return:
        """
        await sender.sendmessage(self.ws, self.battle_field.room_name, "Well done, have a nice day!")
        await sender.leaving(self.ws, self.battle_field.room_name)
        exit(1)

    async def _handle_chat(self, current):
        """Method that replies to the chat"""
        if self.user_name not in current[2]:
            if "go" in current[3]:
                try:
                    new_difficulty = Difficulty[current[3].split(" ")[1].capitalize()]
                    self.chooser.difficulty = new_difficulty
                    await sender.sender(self.ws, self.battle_field.room_name, "Difficulty is now set on: {}".format(
                        new_difficulty.value))
                except:
                    await sender.sender(self.ws, self.battle_field.room_name, "That difficulty is not supported "
                                                                              "yet!\nTry easy, normal or hard")

            else:
                num_answer = random.randint(0, len(self.standard_answers) - 1)
                await sender.sender(self.ws, self.battle_field.room_name, self.standard_answers[num_answer])

    async def _handle_faint(self, current):
        """Method that handles the fainting of a pokemon
        :param current:
        :return:
        """
        """faint"""
        if self.battle_field.player_id not in current[1]:
            Status.apply_non_volatile_status(StatusType.Fnt, self.battle_field.active_pokemon_bot)
        else:
            Status.apply_non_volatile_status(StatusType.Fnt, self.battle_field.active_pokemon_oppo)

    async def _handle_heal(self, current):
        """Method that handles the heal message and updates the hp of the pokemons"""
        """-heal"""
        if self.battle_field.player_id in current[2]:
            self.battle_field.update_heal(1, int(current[3].split("/")[0]))
        else:
            # TODO: The opponent is in %
            self.battle_field.update_heal(2, int(current[3].split("/")[0]))

    async def _handle_status(self, current):
        """Method that updates the status of the active pokemons
        :param current:
        :return:
        """
        """-status"""
        if self.battle_field.player_id in current[2]:
            self.battle_field.update_status(1, current[3])
        else:
            self.battle_field.update_status(2, current[3])

    async def _handle_curestatus(self, current):
        """Method that cures the status of the active pokemon
        :param current:
        :return:
        """
        """-curestatus"""
        if self.battle_field.player_id in current[2]:
            self.battle_field.update_status(1)
        else:
            self.battle_field.update_status(2)

    async def _handle_boost(self, current):
        """Method that handles the boost of the active pokemons' stats
        :param current:
        :return:
        """
        """-boost"""
        if self.battle_field.player_id in current[2]:
            self.battle_field.update_buff(1, current[3], int(current[4]))
            self.mul_stats_bot[StatsType[current[3].strip().capitalize()]] += int(current[4])
        else:
            self.battle_field.update_buff(2, current[3], int(current[4]))
            self.mul_stats_oppo[StatsType[current[3].strip().capitalize()]] += int(current[4])

    async def _handle_unboost(self, current):
        """Method that handles the boost of the negative pokemons' stats
        :param current:
        :return:
        """
        """-unboost"""
        if self.battle_field.player_id in current[2]:
            self.battle_field.update_buff(1, current[3], - int(current[4]))
            self.mul_stats_bot[StatsType[current[3].strip().capitalize()]] -= int(current[4])
        else:
            self.battle_field.update_buff(2, current[3], - int(current[4]))
            self.mul_stats_oppo[StatsType[current[3].strip().capitalize()]] -= int(current[4])

    async def _handle_weather(self, current):
        """Method that handles the weather message and updates the battlefield
        :param current:
        :return:
        """
        """-weather"""
        if current[2] == 'none':
            self.battle_field.update_weather("Normal")
        else:
            self.battle_field.update_weather(current[2])

    async def _handle_field_start(self, current):
        """Method that handles the set of the terrain
        :param current:
        :return:
        """
        """-fieldstart"""
        """<class 'list'>: ['', '-fieldstart', 'move: Grassy Terrain', '[from] ability: Grassy Surge', '[of] p2a: Tapu Bulu']"""
        # TODO Handle terrains
        terrain = current[2].split(":")[1].strip().split(" ")[0]
        self.battle_field.update_field(Field[terrain])

    async def _handle_field_end(self, current):
        """Method that resets the terrain
        :param current:
        :return:
        """
        """-fieldend"""
        self.battle_field.update_field(Field.Normal)

    async def _handle_start_vol(self, current):
        """|-start|p2a: Toxicroak|move: Taunt"""
        if "move" in current[3]:
            vol_status = current[3].split(":")[1].strip().replace(" ", "")
        else:
            vol_status = current[3].strip().capitalize().replace(" ", "")

        if self.battle_field.player_id in current[2]:
            Status.add_volatile_status(StatusType[vol_status],
                                       self.battle_field.active_pokemon_bot)
            self.bot_volatile.append(StatusType[vol_status])
        else:
            Status.add_volatile_status(StatusType[vol_status],
                                       self.battle_field.active_pokemon_oppo)
            self.oppo_volatile.append(StatusType[vol_status])

    async def _handle_end_vol(self, current):
        """|-end|p2a: Toxicroak|move: Taunt"""
        if "move" in current[3]:
            vol_status = current[3].split(":")[1].strip()
        else:
            vol_status = current[3].strip().capitalize()

        if self.battle_field.player_id in current[2]:
            Status.remove_volatile_status(StatusType[vol_status],
                                          self.battle_field.active_pokemon_bot)
            self.bot_volatile.remove(StatusType[vol_status])
        else:
            Status.remove_volatile_status(StatusType[vol_status],
                                          self.battle_field.active_pokemon_oppo)
            self.oppo_volatile.remove(StatusType[vol_status])
