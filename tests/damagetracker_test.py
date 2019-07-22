import unittest

from src.ai.damage_tracker import DamageTracker
from src.model.move import SingleMove, MoveCategory
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk
from src.model.stats import StatsType, Stats


class DamageTrackerTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(DamageTrackerTest, self).__init__(*args, **kwargs)

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

    def test_add_track(self):
        tracker = DamageTracker()
        tracker.add_damage(self.pokemon1, 30, self.pokemon1.moves[1], self.pokemon2)
        self.assertEqual(len(tracker.tracker), 1)
        self.assertEqual(tracker.get_damage(self.pokemon1, self.pokemon1.moves[1], self.pokemon2), 30)

    def test_remove_caster(self):
        tracker = DamageTracker()
        tracker.add_damage(self.pokemon1, 30, self.pokemon1.moves[1], self.pokemon2)
        tracker.add_damage(self.pokemon2, 50, self.pokemon1.moves[2], self.pokemon1)
        tracker.remove_caster(self.pokemon1)
        self.assertEqual(len(tracker.tracker), 1)
        self.assertEqual(tracker.get_damage(self.pokemon1, self.pokemon1.moves[1], self.pokemon2), -1)

    def test_remove_target(self):
        tracker = DamageTracker()
        tracker.add_damage(self.pokemon1, 30, self.pokemon1.moves[1], self.pokemon2)
        tracker.add_damage(self.pokemon2, 50, self.pokemon1.moves[2], self.pokemon1)
        tracker.remove_target(self.pokemon1)
        self.assertEqual(len(tracker.tracker), 1)
        self.assertEqual(tracker.get_damage(self.pokemon1, self.pokemon1.moves[1], self.pokemon2), 30)
        pass


if __name__ == '__main__':
    unittest.main()
