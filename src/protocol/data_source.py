from abc import ABC, abstractmethod
import mysql.connector

from src.model.pokemontype import PokemonType
from src.model.status import StatusType
from src.model.stats import Stats
from src.model.pokemon import Pokemon

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


        return Pok
        # TODO: Create and return pokemon object

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
        result = cursor.fetchall()
        # TODO: Return move object

    def get_movetype_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT mv.type FROM Moves as mv.name = %s"
        cursor.execute(parametric_query, name)
        result = cursor.fetchall()
        # TODO: Return Enum value
        # TODO: Tests
        return PokemonType[result[0][0]]
