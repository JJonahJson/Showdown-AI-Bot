import unittest
import src.protocol.data_source as ds
from src.model.stats import StatsType as s
from src.model.pokemontype import PokemonType as pk


class DBTest(unittest.TestCase):

    def test_pokemon_type(self):
        db = ds.DatabaseDataSource()
        types = db.get_pokemontype_by_name("Blastoise")
        self.assertEqual(len(types), 1)
        self.assertEqual(types[0], pk.Water)

        types = db.get_pokemontype_by_name("Blaziken")
        self.assertEqual(len(types), 2)
        self.assertEqual(types[0], pk.Fire)
        self.assertEqual(types[1], pk.Fighting)

    def test_pokemon(self):
        db = ds.DatabaseDataSource()
        pokemon_obj = db.get_pokemon_by_name("Blaziken")
        self.assertEqual(pokemon_obj.name, "Blaziken")
        self.assertEqual(pokemon_obj.types[0], pk.Fire)
        self.assertEqual(pokemon_obj.types[1], pk.Fighting)
        self.assertEqual(pokemon_obj.stats.base_stats[s.HP], 80)
        self.assertEqual(pokemon_obj.stats.base_stats[s.Att], 120)
        self.assertEqual(pokemon_obj.stats.base_stats[s.Def], 70)
        self.assertEqual(pokemon_obj.stats.base_stats[s.Spa], 110)
        self.assertEqual(pokemon_obj.stats.base_stats[s.Spd], 70)
        self.assertEqual(pokemon_obj.stats.base_stats[s.Spe], 80)
        self.assertEqual(pokemon_obj.weight, 52.0)

    def test_get_move_type(self):
        db = ds.DatabaseDataSource()
        move_type = db.get_movetype_by_name("Flamethrower")
        self.assertEqual(move_type, pk.Fire)



if __name__ == '__main__':
    unittest.main()
