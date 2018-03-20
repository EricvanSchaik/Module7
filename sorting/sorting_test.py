import unittest
import random

from sorting import InsertionSorter, QuickSorter


def random_list(sample_size):
    """
    Sample n random values between 0...100 from the uniform distribution.
    """
    return [random.randrange(100) for i in range(sample_size)]


class TestSorters(unittest.TestCase):
    def setUp(self):
        # Seed the random generator to make the test cases deterministic
        # there are enough test cases to make sure the code works.
        random.seed(997)

        self.test_cases = []
        self.num_test_cases = 10

        # Make an array of test cases
        # First: Simple cases with 'well known' values in non-increasing order
        self.test_cases.append([])
        self.test_cases.append([1])
        self.test_cases.append([1, 1])
        self.test_cases.append([1, 2, 1])

        # Second: Special lengths
        for case_length in (5, 7, 11, 13, 2**2, 2**4, 2**8, 2**12):
            self.test_cases.append(random_list(case_length))

        # Third: Random test cases
        for i in range(self.num_test_cases):
            self.test_cases.append(random_list(10))

    def test_insertion(self):
        sorter = InsertionSorter()

        for case in self.test_cases:
            # The test copies the test case to prevent changes
            sorter_sorted = sorter.sort(case.copy())[:]

            # assertListEqual (Python >= 3.0)
            self.assertListEqual(sorter_sorted, sorted(case.copy()))

    def test_quicksort(self):
        sorter = QuickSorter()

        for case in self.test_cases:
            sorter_sorted = sorter.sort(case.copy())[:]

            self.assertListEqual(sorter_sorted, sorted(case.copy()))


if __name__ == '__main__':
    unittest.main()
