import unittest

from src.model.stats import Stats, StatsType


class StatsTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StatsTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100, is_base=False)

    def testIncreaseStat(self):
        counter = 1
        self.stat.modify(StatsType.Att, counter)
        should_be = self.stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        self.stat.modify(StatsType.Att, 1)
        should_be = self.stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testIncreaseAccuracyOrEvasiveness(self):
        counter = 1
        self.stat.modify(StatsType.Eva, counter)
        should_be = self.stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        self.stat.modify(StatsType.Eva, 1)
        should_be = self.stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseStat(self):
        counter = -1
        self.stat.modify(StatsType.Att, counter)
        should_be = self.stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter -= 1
        self.stat.modify(StatsType.Att, -1)
        should_be = self.stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseAccuracyOrEvasiveness(self):
        counter = (-1)
        self.stat.modify(StatsType.Eva, counter)
        should_be = self.stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += (-1)
        self.stat.modify(StatsType.Eva, -1)
        should_be = self.stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testOverflowBuff(self):
        counter = 7
        self.stat.modify(StatsType.Att, counter)
        should_be = self.stat.base_stats[StatsType.Att] * Stats.multipliers[6]
        actual = self.stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        self.assertEqual(self.stat.mul_stats[StatsType.Att], 6,
                         "Multiplier should be 6 instead of {}".format(str(self.stat.mul_stats[StatsType.Att])))
