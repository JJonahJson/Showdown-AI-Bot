import unittest
from src.model.stats import Stats, StatsType
from src.model.pokemon import Pokemon
from src.model.move import SingleMove, MoveCategory
from src.model.pokemontype import PokemonType as pk
from src.model.status import StatusType
from src.ai.chooser import Chooser
from src.model.field import BattleFieldSingle


class ChooserTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ChooserTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100, )

        self.pokemon1a = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", self.stat, {}, [], 80.50,
                                 StatusType.Normal, [], None, 50)
        self.pokemon2a = Pokemon("Starmie", [pk.Water, pk.Psychic], "Female", self.stat, {}, [], 80,
                                 StatusType.Normal, [], None, 50)
        self.pokemon1b = Pokemon("Charizard", [pk.Fire, pk.Flying], "Male", self.stat, {}, [], 90.50,
                                 StatusType.Normal, [], None, 50)
        self.pokemon1c = Pokemon("Venusaur", [pk.Grass, pk.Poison], "Male", self.stat, {}, [], 100,
                                 StatusType.Normal, [], None, 50)
        self.pokemon1d = Pokemon("Raichu", [pk.Electric], "Male", self.stat, {}, [], 30,
                                 StatusType.Normal, [], None, 50)
        self.pokemon1e = Pokemon("Shiftry", [pk.Grass, pk.Dark], "Male", self.stat, {}, [], 59.6,
                                 StatusType.Normal, [], None, 50)
        self.pokemon1f = Pokemon("Arbok", [pk.Poison], "Male", self.stat, {}, [], 65,
                                 StatusType.Normal, [], None, 50)

        self.pokemon1a.moves[1] = SingleMove('Flamethrower', 1, 90, MoveCategory.Damage, 15, 0, False, 1, pk.Fire,
                                            StatsType.Spa, [], [], StatsType.Spd, 10, None, StatusType.Brn)
        self.pokemon1a.moves[2] = SingleMove('Bite', 1, 60, MoveCategory.Damage, 25, 0, False, 1, pk.Dark,
                                            StatsType.Atk, [], [], StatsType.Def, 30, StatusType.Flinch, None)

        self.pokemon2a.moves[1] = SingleMove('Hydropump', 1, 110, MoveCategory.Damage, 5, 0, False, 1, pk.Water,
                                            StatsType.Spa, [], [], StatsType.Spd, 100, None, None)
        self.pokemon2a.moves[2] = SingleMove('Psy Beam', 1, 65, MoveCategory.Damage, 20, 0, False, 1, pk.Psychic,
                                            StatsType.Spa, [], [], StatsType.Spd, 10, StatusType.Confusion, None)
        self.battleField = BattleFieldSingle(self.pokemon1a, self.pokemon2a,
                                             {1: self.pokemon1a, 2: self.pokemon1b, 3: self.pokemon1c,
                                              4: self.pokemon1d, 5: self.pokemon1e, 6: self.pokemon1f}, {1: self.pokemon2a})

    def test_choose_move(self):
        index = Chooser.choose_move(self.battleField)
        self.assertEqual(2, index)

    def test_switch_move(self):
        index = Chooser.choose_switch(self.battleField)
        self.assertEqual(5, index)