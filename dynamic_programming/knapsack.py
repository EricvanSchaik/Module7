import typing
from functools import total_ordering


# This total ordening defines comparison functions in terms of other functions
# for example if you know when two objects are equal, you also know when they are not
@total_ordering
class Item(object):
    """
    An item for the knapsack problem.

    An item has a weight and a value. A solution to the knapsack problem
    maximizes the value of a set of items while keeping the total weight below
    a certain value.
    """
    def __init__(self, weight: int, value: int):
        """
        :param weight: The weight of this item.
        :param value: The value of this item.
        """
        self._weight = weight
        self._value = value

    @property
    def weight(self) -> int:
        """
        :return: The weight of this item.
        """
        return self._weight

    @property
    def value(self) -> int:
        """
        :return: The value of this item.
        """
        return self._value

    def __str__(self) -> str:
        return "Item (weight: {}, value {})".format(self.weight, self.value)

    def __eq__(self, other: "Item") -> bool:
        return self.weight == other.weight and self.value == other.value

    def __lt__(self, other: "Item") -> bool:
        return self.value < other.value or self.weight < other.weight


@total_ordering
class Knapsack(object):
    """
    A (partial) solution to the knapsack problem.

    A solution to the knapsack problem maximizes the value of a set of items
    while keeping the total weight below a certain value.
    """
    def __init__(self, max_weight: int, dictionary: dict=None):
        """
        :param max_weight: The maximum total weight of the solution.
        :param dictionary: An optional dictionary to pass to the instance.
        """
        self._max_weight = max_weight
        self.dictionary = dictionary if dictionary else {}
        self.items = []  # Use this to store the items you picked.

    @property
    def max_weight(self) -> int:
        return self._max_weight

    @property
    def valid(self):
        return self.weight <= self._max_weight

    def solve(self, items: typing.List[Item]) -> None:
        """
        Fills this knapsack with items. A subset of the items passed to this
        method might end up in the knapsack.

        This method should populate `self.items` with the chosen items. This
        method does not have to return anything.

        :param items: List of candidate items.
        """

        matrix = [[0 for j in range(self.max_weight + 1)] for i in range(len(items) + 1)]

        for j in range(self.max_weight):
            matrix[0][j] = 0

        for i in range(1, len(items) + 1):
            for j in range(self.max_weight + 1):
                if items[i - 1].weight > j:
                    matrix[i][j] = matrix[i - 1][j]
                else:
                    matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - items[i - 1].weight] + items[i - 1].value)
                    if matrix[i][j] != matrix[i - 1][j]:
                        if not self.dictionary.get(j - items[i - 1].weight):
                            knapsack = Knapsack(self.max_weight)
                            knapsack.items.append(items[i - 1])
                            self.dictionary[j] = knapsack
                        else:
                            self.dictionary[j - items[i - 1].weight].items.append(items[i - 1])
                            self.dictionary[j] = self.dictionary[j - items[i - 1].weight]

        for item in self.dictionary[self.max_weight].items:
            self.items.append(item)
            print(str(item.weight) + ":" + str(item.value) + "\n")


    @property
    def value(self) -> int:
        """
        :return: The sum of the values of the items in this knapsack.
        """
        total = 0
        for item in self.items:
            total = total + item.value

        return total

    @property
    def weight(self) -> int:
        """
        :return: The sum of the weights of the items in this knapsack.
        """
        total = 0
        for item in self.items:
            total = total + item.weight

        return total

    def __str__(self) -> str:
        return "Knapsack (weight: {}, value {}, items [{}])".format(
            self.weight,
            self.value,
            ", ".join(map(str, self.items))
        )

    def __eq__(self, other: "Knapsack") -> bool:
        return self.max_weight == other.max_weight and sorted(self.items) == sorted(other.items)

    def __lt__(self, other: "Knapsack") -> bool:
        return self.value < other.value or self.weight < other.weight
