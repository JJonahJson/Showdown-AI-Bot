import unittest
from src.model.stats import Stats, StatsType
from src.model.pokemon import Pokemon
from src.model.move import SingleMove, MoveCategory
from src.model.pokemontype import PokemonType as pk
from src.model.status import StatusType


class ChooserTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ChooserTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100, )
        self.incineroar_moves = SingleMove('Flamethrower', 1, 90, MoveCategory.Damage, 15, 0, False, 1, pk.Fire,
                                           StatsType.Spa, [], [], StatsType.Spd, 10, None, StatusType.Brn)
        self.pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", self.stat, {}, [], 80.50,
                               StatusType.Normal, [], None, 50)
        self.pokemon = Pokemon("Starmie", [pk.Water, pk.Psychic], "Female", self.stat, {}, [], 80.50,
                               StatusType.Normal, [], None, 50)
