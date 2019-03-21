import unittest

import sys
sys.path.append("..")

from move import SingleMove, MultipleMove
from movefactory import MoveFactory

class Movetest(unittest.TestCase):

    def testFactory(self):
        singleMove = MoveFactory.CreateMove("single",
            "airslash", 95, 75, "special", 15, 0, False, 1, "Flying", None, None)
        doubleMove = MoveFactory.CreateMove("multiple",
            "airslash", 95, 75, "special", 15, 0, False, 1, "Flying", None, None)
        self.assertIsInstance(singleMove, SingleMove, "Should be SingleMove")
        self.assertIsInstance(doubleMove, MultipleMove, "should be MultipleMove")

    def testSingleMoveCreation(self):
        singleMove = MoveFactory.CreateMove("single",
        "airslash", 95, 75, "special", 15, 0, False, 1, "Flying", None, None)
        self.assertIsInstance(singleMove, SingleMove, "Should be instance of SingleMove")
        self.assertEqual(singleMove.moveName, "airslash", "Name test: should be airslash and is {}".format(singleMove.moveName))
        self.assertEqual(singleMove.accuracy, 95, "Accuracy test: should be 95 and is {}".format(singleMove.accuracy))
        self.assertEqual(singleMove.basePower, 75, "Basepower test: hould be 75 and is {}".format(singleMove.basePower))
        self.assertEqual(singleMove.category, "special", "Category test:should be special and is {}".format(singleMove.category))
        self.assertEqual(singleMove.pp, 15, "PP test: should be 15 and is {}".format(singleMove.pp))
        self.assertEqual(singleMove.priority, 0, "Priority test: should be 0 and is {}".format(singleMove.priority))
        self.assertEqual(singleMove.isZ, False, "isZ test: should be False and is {}".format(singleMove.isZ))
        self.assertEqual(singleMove.moveType, "Flying", "MoveType test: should be Flying is {}".format(singleMove.moveType))


if __name__ == "__main__":
    unittest.main()


