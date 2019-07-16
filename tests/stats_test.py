import unittest

from src.model.stats import Stats, StatsType


class StatsTest(unittest.TestCase):

    def testIncreaseStat(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 1
        stat.modify(StatsType.Attack, counter)
        should_be = stat.base_stats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Attack)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        stat.modify(StatsType.Attack, 1)
        should_be = stat.base_stats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Attack)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testIncreaseAccuracyOrEvasiveness(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 1
        stat.modify(StatsType.Evasion, counter)
        should_be = stat.base_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Evasion)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        stat.modify(StatsType.Evasion, 1)
        should_be = stat.base_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Evasion)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseStat(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = -1
        stat.modify(StatsType.Attack, counter)
        should_be = stat.base_stats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Attack)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter -= 1
        stat.modify(StatsType.Attack, -1)
        should_be = stat.base_stats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.get_actual(StatsType.Attack)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseAccuracyOrEvasiveness(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = (-1)
        stat.modify(StatsType.Evasion, counter)
        should_be = stat.base_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Evasion)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += (-1)
        stat.modify(StatsType.Evasion, -1)
        should_be = stat.base_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.get_actual(StatsType.Evasion)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testOverflowBuff(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 7
        stat.modify(StatsType.Attack, counter)
        should_be = stat.base_stats[StatsType.Attack] * Stats.multipliers[6]
        actual = stat.get_actual(StatsType.Attack)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        self.assertEqual(stat.mul_stats[StatsType.Attack], 6,
                         "Multiplier should be 6 instead of {}".format(str(stat.mul_stats[StatsType.Attack])))
