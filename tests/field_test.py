import unittest

from src.model.field import BattleFieldSingle, Weather
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk
from src.model.stats import Stats


class FieldTest(unittest.TestCase):

    def testSwitch(self):
        stats = Stats(100, 100, 100, 100, 100, 100)
        pokemon1 = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", stats, None, None, None, None, None, None, 50)
        pokemon2 = Pokemon("Kyogre", [pk.Water], "", stats, None, None, None, None, None, None, 50)
        pokemon3 = Pokemon("Qwilfish", [pk.Water, pk.Poison], "Male", stats, None, None, None, None, None, None, 50)
        pokemon4 = Pokemon("Gyarados", [pk.Water, pk.Flying], "Male", stats, None, None, None, None, None, None, 50)
        battleField = BattleFieldSingle(pokemon1, pokemon2, {1: pokemon4},
                                        {1: pokemon3})
        battleField.switch_pokemon(1, 1)

        self.assertEqual(battleField.active_pokemon_bot, pokemon4)
        self.assertEqual(battleField.active_selector_side[1], pokemon4)
        self.assertEqual(battleField.active_pokemon_oppo, pokemon2)

    def test_tostring_weather(self):
        self.assertEqual(Weather["Raindance"], Weather.Raindance)

    if __name__ == "__main__":
        unittest.main()
