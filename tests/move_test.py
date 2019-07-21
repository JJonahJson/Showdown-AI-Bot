import unittest

from src.model.field import Weather as w, Field as f
from src.model.move import SingleMove, MoveCategory
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk
from src.model.stats import StatsType, Stats


class MoveTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MoveTest, self).__init__(*args, **kwargs)
        stats = Stats(100, 100, 100, 100, 100, 100, )

        move1 = SingleMove("Lanciafiamme", 100, 100, MoveCategory.Damage, 10, 0, False, 15, pk.Fire,
                           StatsType.Spa, None, None, StatsType.Spd, 100, None, None)

        move2 = SingleMove("Idropompa", 100, 100, MoveCategory.Damage, 10, 0, False, 15, pk.Water,
                           StatsType.Spa, None, None, StatsType.Spd, 100, None, None)

        moves = {1: move1,
                 2: move2}

        self.pokemon1 = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", stats, moves, None, None, None,
                                None, None, 50)
        self.pokemon2 = Pokemon("Kyogre", [pk.Water], "", stats, moves, None, None, None, None, None, 50)

    def test_invoke(self):
        self.pokemon1.use_move(1, self.pokemon2, w.Normal, f.Normal)
        self.assertNotEqual(self.pokemon2.stats.damage, 0)
        self.assertEqual(self.pokemon1.moves[1].pp, 9)


if __name__ == '__main__':
    unittest.main()
