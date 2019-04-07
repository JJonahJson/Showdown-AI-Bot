from src.model.field import BattleField
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk
from src.model.stats import Stats

import unittest


class FieldTest(unittest.TestCase):

    def testSwitch(self):

        stats = Stats(100,100,100,100,100, 100)
        pokemon1 = Pokemon("Incineroar",[pk.Fire, pk.Dark], "Male", stats, None, None, None, None, None, 50)
        pokemon2 = Pokemon("Kyogre",[pk.Water], "", stats, None, None, None, None, None, 50)
        pokemon3 = Pokemon("Qwilfish",[pk.Water, pk.Poison], "Male", stats, None, None, None, None, None, 50)
        pokemon4 = Pokemon("Gyarados",[pk.Water, pk.Flying], "Male", stats, None, None, None, None, None, 50)
        battleField = BattleField({1:pokemon1, 2:pokemon2}, {1:pokemon3, 2:pokemon4}, {1:pokemon3, 2:pokemon4}, {1:pokemon1, 2:pokemon2})
        battleField.switchPokemon(1,1,1)

        self.assertEqual(battleField.activePokemonSide1[1], pokemon3)
        self.assertEqual(battleField.inactivePokemonSide1[1], pokemon1)


if __name__ == "__main__":
    unittest.main()