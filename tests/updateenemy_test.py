import unittest
from src.protocol.data_source import DatabaseDataSource
from src.model.field import BattleFieldSingle
from src.protocol.enemy_updater import update_enemy_pokemon, update_enemy_move


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

    def test_add_enemy_move(self):
        update_enemy_pokemon(self.bf, self.ds, "Sunflora", 89, "M")
        update_enemy_move(self.bf, self.ds, "Bite")
        self.assertEqual(len(self.bf.active_pokemon_oppo.moves), 1)
        self.assertEqual(self.bf.active_pokemon_oppo.moves[1].move_name, "Bite")

    def test_add_duplicate_move(self):
        update_enemy_pokemon(self.bf, self.ds, "Sunflora", 89, "M")
        update_enemy_move(self.bf, self.ds, "Bite")
        update_enemy_move(self.bf, self.ds, "Bite")
        self.assertEqual(len(self.bf.active_pokemon_oppo.moves), 1)
        self.assertEqual(self.bf.active_pokemon_oppo.moves[1].move_name, "Bite")

    def test_add_multiple_move(self):
        update_enemy_pokemon(self.bf, self.ds, "Sunflora", 89, "M")
        update_enemy_move(self.bf, self.ds, "Bite")
        update_enemy_move(self.bf, self.ds, "Flamethrower")
        self.assertEqual(len(self.bf.active_pokemon_oppo.moves), 2)
        self.assertEqual(self.bf.active_pokemon_oppo.moves[1].move_name, "Bite")
        self.assertEqual(self.bf.active_pokemon_oppo.moves[2].move_name, "Flamethrower")


if __name__ == '__main__':
    unittest.main()
