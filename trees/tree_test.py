import unittest

from trees.tree import Tree


class TestTree(unittest.TestCase):
    def setUp(self):
        self.tree = Tree()

    def test_insert(self):
        # Add root node
        self.tree.insert(4)
        self.assertEqual(self.tree.root.key, 4)
        self.assertTrue(self.tree.root.is_root())
        self.assertTrue(self.tree.root.is_leaf())

        # Add some more nodes
        self.tree.insert(1)
        self.assertEquals(self.tree.root.left.key, 1)
        self.tree.insert(7)
        self.assertEquals(self.tree.root.right.key, 7)
        self.tree.insert(2)
        self.assertEquals(self.tree.root.left.right.key, 2)
        self.tree.insert(6)
        self.assertEquals(self.tree.root.right.left.key, 6)

    def test_rotate_left(self):
        sequence = [5, 3, 4, 2, 6]
        nodes = {}

        # Add nodes
        for key in sequence:
            self.tree.insert(key)
            nodes[key] = self.tree.search(key)

        # Rotate
        self.tree._rotate_left(self.tree.root)

        # Check tree structure
        self.assertEquals(self.tree.root.key, 6)
        self.assertEquals(self.tree.root.left.key, 5)
        self.assertEquals(self.tree.root.left.left.key, 3)
        self.assertEquals(self.tree.root.left.left.left.key, 2)
        self.assertEquals(self.tree.root.left.left.right.key, 4)

        # Compare if rotation was done using pointers instead of value reassignment
        for key, node in nodes.items():
            self.assertEquals(self.tree.search(key), node)

    def test_rotate_right(self):
        sequence = [5, 3, 4, 2, 6]
        nodes = {}

        # Add nodes
        for key in sequence:
            self.tree.insert(key)
            nodes[key] = self.tree.search(key)

        # Rotate
        self.tree._rotate_right(self.tree.root)

        # Check tree structure
        self.assertEquals(self.tree.root.key, 3)
        self.assertEquals(self.tree.root.left.key, 2)
        self.assertEquals(self.tree.root.right.key, 5)
        self.assertEquals(self.tree.root.right.left.key, 4)
        self.assertEquals(self.tree.root.right.right.key, 6)

        # Compare if rotation was done using pointers instead of value reassignment
        for key, node in nodes.items():
            self.assertEquals(self.tree.search(key), node)

    def test_balance(self):
        sequence = [7, 5, 8, 3, 6, 2, 4]
        nodes = {}

        # Add nodes
        for key in sequence:
            self.tree.insert(key)
            nodes[key] = self.tree.search(key)

        # Balance
        self.tree.balance()

        # Check balanced
        def is_balanced(node):
            left = len(node.left) if node.left else 0
            right = len(node.right) if node.right else 0
            left_balanced = is_balanced(node.left) if node.left else True
            right_balanced = is_balanced(node.right) if node.right else True
            balanced = abs(left - right) <= 1
            return balanced and left_balanced and right_balanced

        self.assertTrue(is_balanced(self.tree.root))

