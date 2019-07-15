import unittest

from src.model.pokemon import Pokemon
from src.model.stats import Stats
from src.model.status import Status, StatusType, PokemonType as pk


class StatusTest(unittest.TestCase):

    def testApplyNonVolatileStatus(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        pokemon = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", stat, None, None, 80.50, Status(StatusType.Normal),
                          [], None, 50)
        check = pokemon.nonVolatileStatus.applyNonVolatileStatus(Status(StatusType.Burned), pokemon)

        self.assertEqual(False, check)
        self.assertEqual(pokemon.nonVolatileStatus.type, StatusType.Normal)

        pokemon.nonVolatileStatus.applyNonVolatileStatus(Status(StatusType.Asleep), pokemon)

        self.assertEqual(pokemon.nonVolatileStatus.type, StatusType.Asleep)

    if __name__ == "__main__":
        unittest.main()
