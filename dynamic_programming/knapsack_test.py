import unittest

from knapsack import Item, Knapsack


class KnapSackTest(unittest.TestCase):
    def setUp(self):
        items = [Item(1, 1), Item(10, 1), Item(20, 2), Item(30, 3), Item(40, 4),
                 Item(50, 5), Item(50, 6), Item(40, 7), Item(30, 8), Item(20, 9)]

        self.solved = [Item(1, 1), Item(10, 1), Item(20, 2), Item(30, 3),
                       Item(50, 6), Item(40, 7), Item(30, 8), Item(20, 9)]

        self.solution = Knapsack(202)
        self.solution.solve(items)

    def test_knapsack_weight(self):
        self.assertEqual(self.solution.weight, 201)

    def test_knapsack_value(self):
        self.assertEqual(self.solution.value, 37)


if __name__ == '__main__':
    unittest.main()
