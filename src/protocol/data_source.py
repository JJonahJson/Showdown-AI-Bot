from abc import ABC, abstractmethod
from src.model.pokemontype import PokemonType
import mysql.connector


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
            user="",
            passwd="",
            database="showdown_db"
        )

    def get_pokemon_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT * FROM Pokemon as pkmn WHERE pkmn.name = %s"
        cursor.execute(parametric_query, name)
        result = cursor.fetchall()
        # TODO: Create and return pokemon object

    def get_pokemontype_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT pkmn_type FROM Pokemon as pkmn WHERE pkmn.name = %s"
        cursor.execute(parametric_query, name)
        result = cursor.fetchall()
        # TODO: Return Enum value
        # TODO: Tests
        return PokemonType[result[0][0]]

    def get_move_by_name(self, name):
        cursor = self.db_connection.cursor(prepared=True)
        parametric_query = "SELECT * FROM Moves as mv where mv.name = %s"
        cursor.execute(parametric_query, name)
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
