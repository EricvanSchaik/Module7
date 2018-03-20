class Sorter(object):
    """
    Base class for sorters. Defines the `sort` method.
    """
    def sort(self, elements):
        """
        Sorts the elements in the list.

        :param elements: The list of elements which has to be sorted
        :type elements: list
        :return: The sorted list of elements
        :rtype: list
        """
        raise NotImplementedError()


class InsertionSorter(Sorter):
    """
    Sorter implementation using the insertion sort strategy.
    """
    def sort(self, elements):
        # Replace this with a useful piece of code that actually sorts elements
        # The test assumes that you return a list
        for i in range(1, len(elements) - 1):
            current = elements[i]
            j = i - 1
            while j >= 0 and elements[j] > current:
                elements[j + 1] = elements[j]
                j -= 1
            elements[j + 1] = current
        return elements


class QuickSorter(Sorter):
    """
    Sorter implementation using the quick sort strategy.
    """
    def sort(self, elements):
        # Replace this with a useful piece of code that actually sorts elements
        # The test assumes that you return a list
        i = self.partition(elements)
        self.sort(elements[0:i-1])
        self.sort(elements[i+1:len(elements)-1])
        return elements


    def partition(self, elements):
        i, j = elements[0], elements[len(elements) - 1]
        pivot = elements[j]
        while i < j:
            while elements[i] < pivot and i < j:
                i += 1
            while elements[j - 1] >= pivot and i < j:
                j -= 1
            if i < j:
                elements[i], elements[j - 1] = elements[j - 1], elements[i]
                i += 1
                j -= 1
            if pivot < elements[i]:
                elements[i], elements[len(elements) - 1] = elements[len(elements) - 1], elements[i]
        return i
