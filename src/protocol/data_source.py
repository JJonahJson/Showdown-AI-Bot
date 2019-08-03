from abc import ABC, abstractmethod

import mysql.connector
import re
from model.move import SingleMove
from model.move_type import MoveCategory
from model.pokemon import Pokemon
from model.pokemon_type import PokemonType
from model.stats import Stats
from model.stats_type import StatsType
from model.status_type import StatusType


class AbstractDataSource(ABC):
    """Abstract class
    """

    @abstractmethod
    def get_pokemon_by_name(self, name):
        pass

    @abstractmethod
    def get_pokemontype_by_name(self, name):
        pass

    @abstractmethod
    def get_move_by_name(self, name):
        pass

    @abstractmethod
    def get_movetype_by_name(self, name):
        pass


class DatabaseDataSource(AbstractDataSource):
    """Class that allow us to connect to the db and retrieve pokemon's informations"""

    def __init__(self):
        super().__init__()
        self.db_connection = mysql.connector.connect(
            host="127.0.0.1",
            user="user",
            passwd="user",
            port=38928,
            database="showdown_db",
            use_pure=True
        )

    def get_pokemon_by_name(self, name, level=50):
        """Method that takes a pokemon name and return a complete pokemon object without moves.
        :param name: The pokemon name
        :param level: The pokemon level
        :return: A pokemon object with stats but empty moves
        """
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT * FROM Pokemon as pkmn WHERE pkmn.name = %s"
        cursor.execute(parametric_query, (name.replace("'", ""),))
        result = cursor.fetchall()
        stats = Stats(result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7],
                      level=level, is_base=True)
        pkmn_name = result[0][1]
        weight_kg = result[0][10]
        if not result[0][9]:
            type_list = [PokemonType[result[0][8]]]
        else:
            type_list = [PokemonType[result[0][8]], PokemonType[result[0][9]]]

        return Pokemon(pkmn_name, type_list, "", stats, {}, [], weight_kg, StatusType.Normal, [], None, level)

    def get_pokemontype_by_name(self, name):
        """Method that takes a pokemon name and return a pokemontype enum
        :param name: The name of the pokemon
        :return: The list of the pokemon types
        """
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT type_1, type_2 FROM Pokemon as pkmn WHERE pkmn.name = %s"
        cursor.execute(parametric_query, (name,))
        result = cursor.fetchall()
        if not result[0][1]:
            return [PokemonType[result[0][0]]]
        else:
            return [PokemonType[result[0][0]], PokemonType[result[0][1]]]

    # num,name, id_name, acc, base_power, category, pp, priority, chance, volatileStatus, nonvolatileStatus
    # all_boost, target, movetype
    def get_move_by_name(self, name):
        """Method that takes a move_name as input and returns a complete move object
        :param name: The move name
        :return: The move object
        """
        cursor = self.db_connection.cursor(prepared=True)
        has_numbers = re.search(r'\d+$', name)
        if "return102" in name:
            real_name = name[:len(name) - 3]
            real_power = int(name[-3:])
        elif "hiddenpower" in name and len(name) > 11 and has_numbers:
            real_name = name[:len(name) - 2]
        else:
            real_name = name

        parametric_query = "SELECT * FROM Moves as mv where mv.id_name = %s"
        cursor.execute(parametric_query, (real_name,))
        try:
            result = cursor.fetchall()[0]
        except:
            return None

        move_name = result[1]
        id_name = result[2]
        accuracy = result[3]
        if "return102" in name:
            base_power = real_power
        else:
            base_power = result[4]
        category = MoveCategory[result[5]]

        if result[5] == 'Physical':
            scale_with = StatsType.Atk
            defends_on = StatsType.Def
        elif result[5] == 'Special':
            scale_with = StatsType.Spa
            defends_on = StatsType.Spd
        else:
            # Per non avere None
            scale_with = StatsType.Spa
            defends_on = StatsType.Spd

        pp = result[6]
        priority = result[7]
        chance = result[8]
        if result[9]:
            volatile_status = StatusType[result[9].capitalize()]
        else:
            volatile_status = result[9]
        if result[10]:
            non_volatile_status = StatusType[result[10].capitalize()]
        else:
            non_volatile_status = result[10]

        boost_atk = result[11]
        boost_def = result[12]
        boost_spa = result[13]
        boost_spd = result[14]
        boost_spe = result[15]
        boost_acc = result[16]
        boost_eva = result[17]
        target = result[18]

        boosts = [
            (StatsType.Atk, boost_atk),
            (StatsType.Def, boost_def),
            (StatsType.Spa, boost_spa),
            (StatsType.Spd, boost_spd),
            (StatsType.Spe, boost_spe),
            (StatsType.Accuracy, boost_acc),
            (StatsType.Evasion, boost_eva)
        ]

        move_type = PokemonType[result[19]]

        if target == 'self':
            return SingleMove(move_name, accuracy, base_power, category, pp, priority, False, 1, move_type, scale_with,
                              list(filter(lambda x: x[1] != 0, boosts)), [], defends_on, chance, (target,
                                                                                                  volatile_status),
                              (target,
                               non_volatile_status))
        else:
            return SingleMove(move_name, accuracy, base_power, category, pp, priority, False, 1, move_type, scale_with,
                              [], list(filter(lambda x: x[1] != 0, boosts)), defends_on, chance, (target,
                                                                                                  volatile_status),
                              (target, non_volatile_status))

    def get_movetype_by_name(self, name):
        """Method that takes a move name as input and returns its type
        :param name: The move name
        :return: The type of the move
        """
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT mv.move_type FROM Moves as mv WHERE mv.name = %s"
        cursor.execute(parametric_query, (name,))
        result = cursor.fetchall()
        return PokemonType[result[0][0]]

    def get_possible_moves_by_name(self, pkmn_name, battle_type="Single"):
        """Method that takes a pokemon name and returns the possible moveset of that pokemon
        :param pkmn_name:
        :param battle_type:
        :return:
        """
        moves_set = {}
        index = 5
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT move FROM Randomsets WHERE pokemon = %s and battle_type = %s"
        cursor.execute(parametric_query, (pkmn_name, battle_type))
        results = cursor.fetchall()
        for result in results:
            moves_set[index] = self.get_move_by_name(result[0])
            index += 1
        return moves_set
