import unittest

from src.model.stats import Stats, StatsType


class StatsTest(unittest.TestCase):

    def testIncreaseStat(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 1
        stat.modify(StatsType.Att, counter)
        should_be = stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        stat.modify(StatsType.Att, 1)
        should_be = stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testIncreaseAccuracyOrEvasiveness(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 1
        stat.modify(StatsType.Eva, counter)
        should_be = stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        stat.modify(StatsType.Eva, 1)
        should_be = stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseStat(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = -1
        stat.modify(StatsType.Att, counter)
        should_be = stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter -= 1
        stat.modify(StatsType.Att, -1)
        should_be = stat.base_stats[StatsType.Att] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseAccuracyOrEvasiveness(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = (-1)
        stat.modify(StatsType.Eva, counter)
        should_be = stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += (-1)
        stat.modify(StatsType.Eva, -1)
        should_be = stat.base_stats[StatsType.Eva] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Eva)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testOverflowBuff(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 7
        stat.modify(StatsType.Att, counter)
        should_be = stat.base_stats[StatsType.Att] * Stats.multipliers[6]
        actual = stat.get_actual(StatsType.Att)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        self.assertEqual(stat.mul_stats[StatsType.Att], 6,
                         "Multiplier should be 6 instead of {}".format(str(stat.mul_stats[StatsType.Att])))
