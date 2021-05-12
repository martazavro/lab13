"""
File: linkedbst.py
Author: Ken Lambert
"""

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import time
import random


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""  # pylint: disable=C0103
            if node != None:
                s += recurse(node.right, level + 1)  # pylint: disable=C0103
                s += "| " * level  # pylint: disable=C0103
                s += str(node.data) + "\n"  # pylint: disable=C0103
                s += recurse(node.left, level + 1)  # pylint: disable=C0103
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):  # pylint: disable=C0103
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left  # pylint: disable=C0103
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right  # pylint: disable=C0103
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None  # pylint: disable=C0103
        preRoot = BSTNode(None)  # pylint: disable=C0103
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root  # pylint: disable=C0103
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data  # pylint: disable=C0103
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left  # pylint: disable=C0103
            else:
                direction = 'R'
                currentNode = currentNode.right  # pylint: disable=C0103

        # Return None if the item is absent
        if itemRemoved == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right  # pylint: disable=C0103

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left  # pylint: disable=C0103

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):  # pylint: disable=C0103
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data  # pylint: disable=C0103
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Height
        '''
        def height1(top):
            '''
            Help
            '''
            if top:
                result = max(height1(top.left), height1(top.right))
                return result + 1
            else:
                return 0
        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(len(self) + 1) - 1

    def range_find(self, low, high):  # pylint: disable=C0103
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        rangee = []
        value = low
        while value != high+1:
            if self.find(value):
                rangee.append(value)
            value += 1
        return rangee

    def rebalance(self):
        '''
        Rebalances the tree.
        :return: self
        '''
        tree_elements = list(self.inorder())
        self.clear()

        def tree_recursion(tree, items):
            if items:
                mid = len(items) // 2
                node = items[mid]
                tree.add(node)
                tree_recursion(tree, items[:mid])
                tree_recursion(tree, items[mid+1:])
                return tree

        self = tree_recursion(self, tree_elements)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        new_list = []
        old_list = list(self.inorder())
        for value in old_list:
            if value > item:
                new_list.append(value)
        if new_list:
            return min(new_list)
        else:
            return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        new_list = []
        old_list = list(self.inorder())
        for value in old_list:
            if value < item:
                new_list.append(value)
        if new_list:
            return max(new_list)
        else:
            return None

    @staticmethod
    def read_file(path):
        """
        Read file and put all the words into the list
        """
        words = []
        with open(path, 'r') as file:
            for word in file:
                words.append(word)
        return words

    def search_list(self, all_words, words):

        start = time.time()
        counter = 0

        for word in all_words:
            if word in words:
                counter += 1
        time_taken = time.time() - start
        return time_taken

    def search_dict(self, words):
        tree = LinkedBST()
        words = words[:1000]
        for word in words:
            tree.add(word)

        start = time.time()
        counter = 0
        while counter != 10000:
            idx = random.randint(0, len(words)-1)
            tree.find(words[idx])
            counter += 1
        time_taken = time.time() - start
        return time_taken

    def search_dict_unsorted(self, words):

        tree = LinkedBST()
        words = list(set(words))[:1000]
        for word in words:
            tree.add(word)

        start = time.time()
        counter = 0
        while counter != 10000:
            idx = random.randint(0, len(words)-1)
            tree.find(words[idx])
            counter += 1
        time_taken = time.time() - start
        return time_taken

    def search_balanced_tree(self, words):
        tree = LinkedBST()
        words = list(set(words))[:900]
        for word in words:
            tree.add(word)

        tree.rebalance()
        start = time.time()
        counter = 0
        while counter != 10000:
            idx = random.randint(0, len(words)-1)
            tree.find(words[idx])
            counter += 1
        time_taken = time.time() - start
        return time_taken

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        all_words = self.read_file(path)
        words = all_words[:10000]
        print()
        print('-------------------------------')
        print()
        print(
            f'Search time for 10,000 random words in an alphabetically ordered dictionary is {round(self.search_list(words, words), 3)} seconds.')
        print()
        print('-------------------------------')
        print()
        print(
            f'Search time for 10,000 random words in the sorted dictionary, which is represented as a binary search tree. is {round(self.search_dict(words), 3)} seconds.')
        print()
        print('-------------------------------')
        print()
        print(
            f'Search time for 10,000 random words in the unsorted dictionary, which is represented as a binary search tree. is {round(self.search_dict_unsorted(words), 3)} seconds.')
        print()
        print('-------------------------------')
        print()
        print(
            f'Search time for 10,000 random words in the dictionary, which is represented as a binary search tree after its balancing is {round(self.search_balanced_tree(words), 3)} seconds.')
        print()
        print('-------------------------------')


if __name__ == '__main__':
    LinkedBST().demo_bst('words.txt')
