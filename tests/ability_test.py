import unittest

from src.model.stats import Stats
from src.model.status import StatusType
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk


class AbilityTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AbilityTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100, )
        self.pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", self.stat, {}, [], 80.50,
                               StatusType.Normal, [], None, 50)

    def test_debuff_enemy_ability(self):
        pass

    def test_weather_ability(self):
        pass

    def test_field_ability(self):
        pass


if __name__ == '__main__':
    unittest.main()
