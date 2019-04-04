import unittest

from src.model.stats import Stats, StatsType

class StatsTest(unittest.TestCase):

    def testIncreaseStat(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 1
        stat.modify(StatsType.Attack, counter)
        shouldBe = stat.baseStats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.getActual(StatsType.Attack)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))

        counter += 1
        stat.modify(StatsType.Attack, 1)
        shouldBe = stat.baseStats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.getActual(StatsType.Attack)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))


    def testIncreaseAccuracyOrEvasiveness(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 1
        stat.modify(StatsType.Evasion, counter)
        shouldBe = stat.baseStats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.getActual(StatsType.Evasion)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))

        counter += 1
        stat.modify(StatsType.Evasion, 1)
        shouldBe = stat.baseStats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.getActual(StatsType.Evasion)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))


    def testDecreaseStat(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = -1
        stat.modify(StatsType.Attack, counter)
        shouldBe = stat.baseStats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.getActual(StatsType.Attack)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))

        counter -= 1
        stat.modify(StatsType.Attack, -1)
        shouldBe = stat.baseStats[StatsType.Attack] * Stats.multipliers[counter]
        actual = stat.getActual(StatsType.Attack)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))

    def testDecreaseAccuracyOrEvasiveness(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = (-1)
        stat.modify(StatsType.Evasion, counter)
        shouldBe = stat.baseStats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.getActual(StatsType.Evasion)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))

        counter += (-1)
        stat.modify(StatsType.Evasion, -1)
        shouldBe = stat.baseStats[StatsType.Evasion] * Stats.multipliersAE[counter]
        actual = stat.getActual(StatsType.Evasion)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))


    def testOverflowBuff(self):
        stat = Stats(100, 100, 100, 100, 100, 100)
        counter = 7
        stat.modify(StatsType.Attack, counter)
        shouldBe = stat.baseStats[StatsType.Attack] * Stats.multipliers[6]
        actual = stat.getActual(StatsType.Attack)
        self.assertEqual(shouldBe, actual, "Stat should be {} instead of {}".format(str(shouldBe), str(actual)))

        self.assertEqual(stat.mulStats[StatsType.Attack], 6, "Multiplier should be 6 instead of {}".format(str(stat.mulStats[StatsType.Attack]))) 


