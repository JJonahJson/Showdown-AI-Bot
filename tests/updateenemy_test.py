import unittest
from src.protocol.data_source import DatabaseDataSource
from src.model.field import BattleFieldSingle
from src.protocol.enemy_updater import update_enemy_pokemon


class UpdateEnemyTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(UpdateEnemyTest, self).__init__(*args, **kwargs)
        self.ds = DatabaseDataSource()
        self.bf = BattleFieldSingle(None, None, {}, {})

    def test_add_in_empty(self):
        update_enemy_pokemon(self.bf, self.ds, "Sunflora", 89, "M")
        self.assertEqual(len(self.bf.bench_selector_side[2]), 1)

    def test_switch_present(self):
        update_enemy_pokemon(self.bf, self.ds, "Sunflora", 89, "M")
        update_enemy_pokemon(self.bf, self.ds, "Garchomp", 89, "M")
        self.assertEqual(len(self.bf.bench_selector_side[2]), 2)
        self.assertEqual(self.bf.active_pokemon_oppo.name, "Garchomp", "M")
        update_enemy_pokemon(self.bf, self.ds, "Sunflora", 89)
        self.assertEqual(len(self.bf.bench_selector_side[2]), 2)
        self.assertEqual(self.bf.active_pokemon_oppo.name, "Sunflora", "M")



if __name__ == '__main__':
    unittest.main()
