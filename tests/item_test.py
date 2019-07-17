import unittest

from src.model.stats import Stats
from src.model.status import StatusType
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk


class ItemTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ItemTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100)
        self.pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", self.stat, {}, [], 80.50,
                               StatusType.Normal, [], None, 50)

    def test_stats_item(self):
        pass

    def test_move_item(self):
        pass

    def test_choice_item(self):
        pass

    def test_damage_item(self):
        pass

    def test_healing_berry(self):
        pass


if __name__ == '__main__':
    unittest.main()
