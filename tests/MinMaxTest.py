import unittest
from model.pokemon import Pokemon
from model.status_type import StatusType
from model.stats import Stats
from model.pokemon_type import PokemonType as pk
from model.move_type import MoveCategory
from model.stats_type import StatsType
from model.move import SingleMove
from model.field import BattleFieldSingle
from ai.IterativeDeepeningMinMax import IterativeDeepeningMinMax


def eval_fn(field):
    return 1

class MinMaxTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MinMaxTest, self).__init__(*args, **kwargs)
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

        self.pokemon1a.moves[1] = SingleMove('Flamethrower', 100, 90, MoveCategory.Special, 15, 0, False, 1, pk.Fire,
                                             StatsType.Spa, [], [], StatsType.Spd, 10, None, ("normal", StatusType.Brn))

        self.pokemon1a.moves[2] = SingleMove('Bite', 1, 60, MoveCategory.Physical, 25, 0, False, 1, pk.Dark,
                                             StatsType.Atk, [], [], StatsType.Def, 30, ("normal", StatusType.Flinch),
                                                                                        None)

        self.pokemon2a.moves[1] = SingleMove('Hydropump', 1, 110, MoveCategory.Special, 5, 0, False, 1, pk.Water,
                                             StatsType.Spa, [], [], StatsType.Spd, 100, None, None)
        self.pokemon2a.moves[2] = SingleMove('Psy Beam', 1, 65, MoveCategory.Special, 20, 0, False, 1, pk.Psychic,
                                             StatsType.Spa, [], [], StatsType.Spd, 10, ("normal",
                                                                                        StatusType.Confusion), None)
        self.battleField = BattleFieldSingle(self.pokemon1a, self.pokemon2a,
                                             {1: self.pokemon1a, 2: self.pokemon1b, 3: self.pokemon1c,
                                              4: self.pokemon1d, 5: self.pokemon1e, 6: self.pokemon1f},
                                             {1: self.pokemon2a})

        self.search = IterativeDeepeningMinMax()

    def test_something(self):
        move = self.search.make_decision(self.battleField, eval_fn)


if __name__ == '__main__':
    unittest.main()
