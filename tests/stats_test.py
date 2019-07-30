import unittest

from model.stats_type import StatsType
from model.stats import Stats



class StatsTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(StatsTest, self).__init__(*args, **kwargs)
        self.stat = Stats(100, 100, 100, 100, 100, 100, is_base=False)

    def testIncreaseStat(self):
        counter = 1
        self.stat.modify(StatsType.Atk, counter)
        should_be = self.stat.real_stats[StatsType.Atk] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Atk)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        self.stat.modify(StatsType.Atk, 1)
        should_be = self.stat.real_stats[StatsType.Atk] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Atk)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testIncreaseAccuracyOrEvasiveness(self):
        counter = 1
        self.stat.modify(StatsType.Evasion, counter)
        should_be = self.stat.real_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Evasion)
        self.assertEqual(round(should_be), actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += 1
        self.stat.modify(StatsType.Evasion, 1)
        should_be = self.stat.real_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Evasion)
        self.assertEqual(round(should_be), actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseStat(self):
        counter = -1
        self.stat.modify(StatsType.Atk, counter)
        should_be = self.stat.real_stats[StatsType.Atk] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Atk)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter -= 1
        self.stat.modify(StatsType.Atk, -1)
        should_be = self.stat.real_stats[StatsType.Atk] * Stats.multipliers[counter]
        actual = self.stat.get_actual(StatsType.Atk)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testDecreaseAccuracyOrEvasiveness(self):
        counter = (-1)
        self.stat.modify(StatsType.Evasion, counter)
        should_be = self.stat.real_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Evasion)
        self.assertEqual(round(should_be), actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        counter += (-1)
        self.stat.modify(StatsType.Evasion, -1)
        should_be = self.stat.real_stats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = self.stat.get_actual(StatsType.Evasion)
        self.assertEqual(round(should_be), actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

    def testOverflowBuff(self):
        counter = 7
        self.stat.modify(StatsType.Atk, counter)
        should_be = self.stat.real_stats[StatsType.Atk] * Stats.multipliers[6]
        actual = self.stat.get_actual(StatsType.Atk)
        self.assertEqual(should_be, actual, "Stat should be {} instead of {}".format(str(should_be), str(actual)))

        self.assertEqual(self.stat.mul_stats[StatsType.Atk], 6,
                         "Multiplier should be 6 instead of {}".format(str(self.stat.mul_stats[StatsType.Atk])))
