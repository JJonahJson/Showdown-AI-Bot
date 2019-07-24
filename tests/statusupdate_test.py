import unittest
import src.protocol.state_update as su

from src.model.field import BattleFieldSingle
from src.model.field import Weather
from src.model.pokemon import Pokemon
from src.model.pokemontype import PokemonType as pk
from src.model.stats import Stats
from src.model.stats_type import StatsType
from model.status_type import StatusType


def build_string(selector, parameters):
    return "{}|pokeid|{}".format(selector, parameters).split("|")


class StatusUpdateTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StatusUpdateTest, self).__init__(*args, **kwargs)
        stats = Stats(100, 100, 100, 100, 100, 100, )

        self.pokemon1 = Pokemon("Incineroar", [pk.Fire, pk.Dark], "Male", stats, None, None, None, None, None, None, 50)
        self.pokemon2 = Pokemon("Kyogre", [pk.Water], "", stats, None, None, None, None, None, None, 50)
        self.pokemon3 = Pokemon("Qwilfish", [pk.Water, pk.Poison], "Male", stats, None, None, None, None, None, None,
                                50)
        self.pokemon4 = Pokemon("Gyarados", [pk.Water, pk.Flying], "Male", stats, None, None, None, None, None, None,
                                50)
        self.battle_field = BattleFieldSingle(self.pokemon1, self.pokemon2, {1: self.pokemon4}, {1: self.pokemon3})
        self.battle_field.player_id = "pokeid"

    def test_switch_weather_rain(self):
        su.update_state(build_string("-weather", "raindance"), self.battle_field)
        self.assertEqual(self.battle_field.weather, Weather.Raindance)

    def test_switch_weather_sun(self):
        su.update_state(build_string("-weather", "sunnyday"), self.battle_field)
        self.assertEqual(self.battle_field.weather, Weather.Sunnyday)

    def test_boost_stat(self):
        su.update_state(build_string("-boost", "att|1"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_bot.stats.mul_stats[StatsType.Atk], 1)

    def test_unboost_stat(self):
        su.update_state(build_string("-unboost", "att|1"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_bot.stats.mul_stats[StatsType.Atk], -1)

    def test_status(self):
        su.update_state(build_string("-status", "tox"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_bot.non_volatile_status, StatusType.Tox)

    def test_curestatus(self):
        self.battle_field.active_pokemon_bot.non_volatile_status = StatusType.Psn
        su.update_state(build_string("-curestatus", "bau"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_bot.non_volatile_status, StatusType.Normal)

    def test_fieldstart(self):
        pass

    def test_fieldend(self):
        pass

    def test_damage(self):
        su.update_state(build_string("-damage", "40/100"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_bot.stats.damage, 40)

    def test_heal(self):
        self.battle_field.active_pokemon_bot.stats.damage = 40
        su.update_state(build_string("-heal", "20/100"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_bot.stats.damage, 20)

    def test_switch(self):
        su.update_state("switch|ciao|Qwilfish,".split("|"), self.battle_field)
        self.assertEqual(self.battle_field.active_pokemon_oppo, self.pokemon3)


if __name__ == '__main__':
    unittest.main()
