from abc import ABC, abstractmethod

import mysql.connector

from src.model.move import SingleMove
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType
from src.model.stats import Stats, StatsType
from src.model.status import StatusType


class AbstractDataSource(ABC):

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

    def __init__(self):
        super().__init__()
        self.db_connection = mysql.connector.connect(
            host="172.17.0.2",
            user="user",
            passwd="user",
            database="showdown_db",
            use_pure=True
        )

    def get_pokemon_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT * FROM Pokemon as pkmn WHERE pkmn.name = %s"
        cursor.execute(parametric_query, (name,))
        result = cursor.fetchall()
        stats = Stats(result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7])
        pkmn_name = result[0][1]
        weight_kg = result[0][10]
        if not result[0][9]:
            type_list = [PokemonType[result[0][8]]]
        else:
            type_list = [PokemonType[result[0][8]], PokemonType[result[0][9]]]

        return Pokemon(pkmn_name, type_list, "", stats, None, None, weight_kg, StatusType.Normal, [], None, 50)

    def get_pokemontype_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT type_1, type_2 FROM Pokemon as pkmn WHERE pkmn.name = %s"
        cursor.execute(parametric_query, (name,))
        result = cursor.fetchall()
        # TODO: Return Enum value
        # TODO: Tests
        if not result[0][1]:
            return [PokemonType[result[0][0]]]
        else:
            return [PokemonType[result[0][0]], PokemonType[result[0][1]]]

    # num,name, id_name, acc, base_power, category, pp, priority, chance, volatileStatus, nonvolatileStatus
    # all_boost, target, movetype
    def get_move_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT * FROM Moves as mv where mv.name = %s"
        cursor.execute(parametric_query, (name,))
        result = cursor.fetchall()[0]

        move_name = result[1]
        id_name = result[2]
        accuracy = result[3]
        base_power = result[4]
        category = result[5]

        if category == 'Physical':
            scale_with = StatsType.Att
            defends_on = StatsType.Def
        else:
            scale_with = StatsType.Spa
            defends_on = StatsType.Spd

        pp = result[6]
        priority = result[7]
        chance = result[8]
        volatile_status = StatusType[result[9]]
        non_volatile_status = StatusType[result[10]]
        boost_atk = result[11]
        boost_def = result[12]
        boost_spa = result[13]
        boost_spd = result[14]
        boost_spe = result[15]
        boost_acc = result[16]
        boost_eva = result[17]
        target = result[18]

        boosts = [
            (StatsType.att, boost_atk),
            (StatsType.Def, boost_def),
            (StatsType.Spa, boost_spa),
            (StatsType.Spd, boost_spd),
            (StatsType.Spe, boost_spe),
            (StatsType.Acc, boost_acc),
            (StatsType.Eva, boost_eva)
        ]

        move_type = PokemonType[result[19]]

        if target == 'self':
            return SingleMove(move_name, accuracy, base_power, category, pp, priority, False, 1, move_type, scale_with,
                              filter(lambda x: x[1] != 0, boosts), [], defends_on, chance, (target, volatile_status),
                              (target,
                               non_volatile_status))
        else:
            return SingleMove(move_name, accuracy, base_power, category, pp, priority, False, 1, move_type, scale_with,
                              [], filter(lambda x: x[1] != 0, boosts), defends_on, chance, (target, volatile_status),
                              (target, non_volatile_status))

    def get_movetype_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT mv.move_type FROM Moves as mv WHERE mv.name = %s"
        cursor.execute(parametric_query, (name,))
        result = cursor.fetchall()
        return PokemonType[result[0][0]]
