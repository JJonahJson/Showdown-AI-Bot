import unittest

from src.model.pokemon import Pokemon
from src.model.stats import Stats
from src.model.status import Status, StatusType, PokemonType as pk

class StatusTest(unittest.TestCase):


    def __init__(self, *args, **kwargs):
        super(StatusTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100)
        self.pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", self.stat, {}, [], 80.50,
                               StatusType.Normal, [], None, 50)

    def test_apply_non_volatile_status(self):
        check = Status.apply_non_volatile_status(StatusType.Burned, self.pokemon)
        self.assertEqual(False, check)

        self.assertEqual(self.pokemon.non_volatile_status, StatusType.Normal)

        Status.apply_non_volatile_status(StatusType.Asleep, self.pokemon)
        self.assertNotEqual(self.pokemon.non_volatile_status, StatusType.Asleep)

    def test_add_volatile_status(self):
        self.assertNotIn(StatusType.Infatuated, self.pokemon.volatile_status)
        Status.add_volatile_status(StatusType.Infatuated, self.pokemon)
        self.assertIn(StatusType.Infatuated, self.pokemon.volatile_status)

    def test_remove_volatile_status(self):
        Status.add_volatile_status(StatusType.Infatuated, self.pokemon)
        Status.remove_volatile_status(StatusType.Infatuated, self.pokemon)
        self.assertNotIn(StatusType.Infatuated, self.pokemon.volatile_status)

    if __name__ == "__main__":
        unittest.main()
