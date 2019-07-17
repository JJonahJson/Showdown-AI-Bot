import unittest

from src.model.pokemon import Pokemon
from src.model.stats import Stats, StatsType
from src.model.status import Status, StatusType, PokemonType as pk


class StatusTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StatusTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100)
        self.pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", self.stat, {}, [], 80.50,
                               StatusType.Normal, [], None, 50)
        self.other_pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Female", self.stat, {}, [], 80.50,
                                     StatusType.Normal, [], None, 50)

    def test_apply_non_volatile_status(self):
        check = Status.apply_non_volatile_status(StatusType.Burned, self.pokemon)
        self.assertEqual(False, check)
        self.assertEqual(self.pokemon.non_volatile_status, StatusType.Normal)

        Status.apply_non_volatile_status(StatusType.Asleep, self.pokemon)

        self.assertEqual(self.pokemon.non_volatile_status, StatusType.Asleep)

    def test_add_volatile_status(self):
        self.assertNotIn(StatusType.Infatuated, self.pokemon.volatile_status)
        Status.add_volatile_status(StatusType.Infatuated, self.pokemon)
        self.assertIn(StatusType.Infatuated, self.pokemon.volatile_status)
        check = Status.add_volatile_status(StatusType.Infatuated, self.pokemon)
        self.assertEqual(False, check)

    def test_remove_volatile_status(self):
        Status.add_volatile_status(StatusType.Infatuated, self.pokemon)
        Status.remove_volatile_status(StatusType.Infatuated, self.pokemon)
        self.assertNotIn(StatusType.Infatuated, self.pokemon.volatile_status)

    def test_apply_infatuation(self):
        check = Status.apply_infatuation(self.pokemon, self.other_pokemon)
        self.assertEqual(True, check)
        check = Status.apply_infatuation(self.pokemon, self.other_pokemon)
        self.assertEqual(False, check)
        Status.remove_volatile_status(StatusType.Infatuated, self.pokemon)
        check = Status.apply_infatuation(self.pokemon, self.pokemon)
        self.assertEqual(False, check)

    def test_apply_paralysis_effect(self):
        Status.apply_non_volatile_status(StatusType.Paralyzed, self.pokemon)
        self.assertEqual(self.pokemon.stats.get_actual(StatsType.Spe), 50)

    def test_apply_poisoning_effect(self):
        Status.apply_non_volatile_status(StatusType.Poisoned, self.pokemon)
        print(self.pokemon.stats.get_actual_hp())
        Status.apply_poisoning_effect(self.pokemon)
        print(self.pokemon.stats.get_actual_hp())
        check = Status.apply_bad_poisoning_effect(self.pokemon)
        self.assertFalse(check)

    def test_remove_non_volatile_status(self):
        Status.apply_non_volatile_status(StatusType.Paralyzed, self.pokemon)
        Status.remove_non_volatile_status(self.pokemon)
        self.assertEqual(self.pokemon.stats.get_actual(StatsType.Spe), 100)

    def test_apply_fainted_effect(self):
        Status.apply_non_volatile_status(StatusType.Fainted, self.pokemon)
        self.assertEqual(0, self.pokemon.stats.get_actual_hp())


    if __name__ == "__main__":
        unittest.main()
