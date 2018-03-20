"""
Implementation of a binary search tree.

Based on [1]
[1]: http://interactivepython.org/runestone/static/pythonds/Trees/SearchTreeImplementation.html
"""
import typing

class Tree(object):
    """
    A binary search tree.
    """
    def __init__(self, root: Node=None):
        self.root = root

    def __eq__(self, other: "Tree") -> bool:
        return self.root.__eq__(other)

    def __iter__(self) -> TreeIterator:
        return self.root.__iter__()

    def __len__(self) -> int:
        return self.root.__len__()

    def __str__(self) -> str:
        return self.root.__str__()

    def search(self, key: int) -> typing.Optional[Node]:
        """
        Searches for the key in the tree. Returns the node associated with the key.

        :param key: The key to find.
        :return: The node for the given key or `None` if there is no such node.
        """
        if self.root:
            return self._search(key, self.root)

        return None

    def _search(self, key: int, node: Node) -> typing.Optional[Node]:
        """
        Private method to find a key in the tree.

        :param key: The key to find.
        :param node: The current node that is looked at.
        :return: The node for the given key or `None` if there is no such node.
        """
        assert key is not None
        assert node is None or isinstance(node, Node)

        if node:
            if key < node.key:
                return self._search(key, node.left)
            elif key > node.key:
                return self._search(key, node.right)
            else:
                return node

        return None

    def insert(self, key: int) -> None:
        """
        Inserts a key into the tree. Does nothing if there already exists a
        node with the given key.

        :param key: The key to add.
        """
        assert key is not None

        if self.root:
            self._insert(key, self.root)
        else:
            self.root = Node(key)

    def _insert(self, key: int, node: Node) -> None:
        """
        Private method to find the place to insert the key in the tree, and
        insert it.

        :param key: The key to add.
        :param node: The current node that is looked at.
        """
        assert key is not None
        assert isinstance(node, Node)

        if self.search(key) is None:
            if key >= node.key:
                self.insert(key, node.right)
            else:
                self.insert(key, node.left)

    def remove(self, key: int) -> None:
        """
        Removes a key from the tree. Does nothing if the key was not present in
        the tree.

        :param key: The key to remove.
        """
        assert key is not None

        node = self.search(key)

        if node:
            if not (node.left and node.right):
                # Replace node with subtree
                if node.left:
                    self._replace(node, node.left)
                else:
                    self._replace(node, node.right)
            else:
                # Replace node with successor
                self._replace(node, node.successor())

    def _replace(self, old_node: Node, new_node: Node) -> None:
        """
        Private method which replaces a node in the tree with another node.

        :param old_node: The node to remove from the tree.
        :param new_node: The node to put in place of the old node.
        """
        assert isinstance(old_node, Node)
        assert new_node is None or isinstance(new_node, Node)

        if new_node:
            new_node.parent = old_node.parent

        if old_node.is_root():
            # New node is the new root
            self.root = new_node
        else:
            if old_node.is_left():
                old_node.parent.left = new_node
            elif old_node.is_right():
                old_node.parent.right = new_node

    def balance(self) -> None:
        """
        Balances the tree.
        """
        if self.root:
            self._balance(self.root)

    def _balance(self, node: Node) -> None:
        """
        Private method which balances the subtree at a given node.

        :param node: The node to be balanced.
        """
        assert isinstance(node, Node)

        raise NotImplementedError()

    def _rotate_left(self, node: Node) -> None:
        """
        Rotates the tree counterclockwise at the given node.

        :param node: The node to rotate the tree at.
        """
        assert isinstance(node, Node)
        assert isinstance(node.right, Node)

        y = node.right
        node.right = y.left
        y.left.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        else:
            if node == node.parent.left:
                node.parent.left = y
            else:
                node.parent.right = y
        y.left = node
        node.parent = y

    def _rotate_right(self, node: Node) -> None:
        """
        Rotates the tree clockwise at the given node.

        :param node: The node to rotate the tree at.
        """
        assert isinstance(node, Node)
        assert isinstance(node.left, Node)

        y = node.left
        node.left = y.right
        y.right.parent = node
        y.parent = node.parent
        if node.parent is None:
            self.root = y
        else:
            if node == node.parent.left:
                node.parent.left = y
            else:
                node.parent.right = y
        y.right = node
        node.parent = y

        raise NotImplementedError()

    def copy(self) -> "Tree":
        """
        Copies the tree recursively.

        :return: A new, copied tree.
        """
        return Tree(root=self.root.copy())

    def graphviz(self) -> str:
        """
        Formats the tree as Dot notation. Enter the code at [1] to see a
        graphic representation.
        [1]: http://www.webgraphviz.com to see a graphic representation.

        :return: The tree as Graphviz code.
        """
        tree = "digraph T {{\n{}}}"
        nodes = ""

        def write_node(node):
            """
            Helper function that recursively creates a string representation
            of the node and it's children.
            """
            out = ''

            if node.parent:
                out += "\"{}\" -> \"{}\"\n".format(node.parent.key, node.key)

            if node.left:
                out += write_node(node.left)
            if node.right:
                out += write_node(node.right)
            return out

        if self.root:
            nodes = write_node(self.root)

        return tree.format(nodes)


class Node(object):
    """
    A binary search tree node.

    Nodes are not meant to be created manually, a node is created by a `Tree`
    when a key is added using `Tree.insert()`.
    """
    def __init__(self, key: int, parent: "Node"=None):
        """
        :param key: The key of this node.
        :param parent: The parent node or `None` if this is the root node.
        """
        assert parent is None or isinstance(parent, Node)

        self.key = key
        self.parent = parent
        self.left = None
        self.right = None

    def __bool__(self) -> bool:
        return True

    def __iter__(self) -> TreeIterator:
        return TreeIterator(self)

    def __len__(self) -> int:
        length = 1
        if self.left:
            length += len(self.left)
        if self.right:
            length += len(self.right)
        return length

    def __str__(self) -> str:
        return "[{} {} {}]".format(str(self.left), self.key, str(self.right))

    def is_left(self) -> bool:
        """
        :return: Whether this node is the left child of its parent.
        """
        return self.parent and self.parent.left == self

    def is_right(self) -> bool:
        """
        :return: Whether this node is the right child of its parent.
        """
        return self.parent and self.parent.right == self

    def is_root(self) -> bool:
        """
        :return: Whether this node is the root of a tree.
        """
        return self.parent is None

    def is_leaf(self) -> bool:
        """
        :return: Whether this node is a leaf of the tree.
        """
        return self.left is None and self.right is None

    def first(self) -> "Node":
        """
        :return: The leftmost node in the subtree, or `self` if there is no left subtree.
        """
        if self.left:
            return self.left.first()
        else:
            return self

    def last(self) -> "Node":
        """
        :return: The rightmost node in the subtree, or `self` if there is no right subtree.
        """
        if self.right:
            return self.right.first()
        else:
            return self

    def successor(self) -> typing.Optional["Node"]:
        """
        :return: The successor (first larger node) of the current node.
        """
        if self.right:
            # Successor is in the right subtree
            return self.right.first()
        else:
            # Successor is the right ancestor
            return self.right_ancestor()

    def right_ancestor(self) -> typing.Optional["Node"]:
        """
        :return: The right ancestor (first larger parent) of the current node.
        """
        if self.is_root():
            # No parent, no ancestors
            return None

        if self.is_left():
            # This is the left child, so its parent is its larger ancestor
            return self.parent
        else:
            # This is the right child, call recursively
            return self.parent.right_ancestor()

    def copy(self, parent: typing.Optional["Node"]=None) -> "Node":
        """
        Copies the current node recursively.

        This method does not deep copy the keys.

        :param parent: The parent of the new, copied node.
        :return: The new, copied node.
        """
        assert parent is None or isinstance(parent, Node)

        node = Node(self.key, parent)

        if self.left:
            node.left = self.left.copy(self)
        if self.right:
            node.right = self.right.copy(self)

        return node


class TreeIterator(object):
    """
    Iterator for iterating over the keys of the nodes in a tree.
    """
    def __init__(self, node: Node):
        self.node = None
        self.next = node

    def __iter__(self) -> "TreeIterator":
        return self

    def __next__(self) -> int:
        if not self.next:
            raise StopIteration

        self.node = self.next
        self.next = self.node.successor()
        return self.node.key
