import unittest
import json
import src.protocol.request_parser as rp
from src.protocol.data_source import DatabaseDataSource


class RequestParser(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(RequestParser, self).__init__(*args, **kwargs)

        self.ds = DatabaseDataSource()
        with open("request.json", "r") as json_test:
            self.req_dict = json.load(json_test)

    def test_parse_active_moves(self):
        active_moves = rp.get_active_moves(self.req_dict["active"][0]["moves"], self.ds)
        self.assertEqual(active_moves[0].move_name, "Scald")
        self.assertEqual(active_moves[0].pp, 24)

    def test_parse_pokemons(self):
        active_moves = rp.get_active_moves(self.req_dict["active"][0]["moves"], self.ds)
        active_pokemon, all_pokemon = rp.get_pokemons(self.req_dict["side"], self.ds, active_moves)
        self.assertEqual(active_pokemon.name, "Omastar")
        self.assertEqual(len(all_pokemon), 6)



if __name__ == '__main__':
    unittest.main()
