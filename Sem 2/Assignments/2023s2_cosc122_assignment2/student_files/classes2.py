"""
classes.py

This module provides classes that are to be used to complete Assignment 2.

These have many careful restrictions placed on them, but do
provide a sufficient interface to solve the problems given.
"""

from stats import StatCounter


GENE_COMP_ERROR = "Can only compare Genes with other Genes, not {type}"


class Gene(object):
    """A simple variation on strings so that we can count comparisons."""

    def __init__(self, dna):
        if not all(c in {"a", "t", "c", "g"} for c in dna):
            raise ValueError(
                "The DNA sequence for this gene is broken: " + dna)
        self._dna = dna

    def __repr__(self):
        return repr(self._dna)

    def __str__(self):
        return str(self._dna)

    def __eq__(self, other):
        if other is None:
            StatCounter.increment("comparisons")
            return False
        if not isinstance(other, Gene):
            raise ValueError(GENE_COMP_ERROR.format(type=type(other)))
        StatCounter.increment("comparisons")
        return self._dna == other._dna

    def __le__(self, other):
        if not isinstance(other, Gene):
            raise ValueError(GENE_COMP_ERROR.format(type=type(other)))
        StatCounter.increment("comparisons")
        return self._dna <= other._dna

    def __ne__(self, other):
        if other is None:
            StatCounter.increment("comparisons")
            return False
        if not isinstance(other, Gene):
            raise ValueError(GENE_COMP_ERROR.format(type=type(other)))
        StatCounter.increment("comparisons")
        return self._dna != other._dna

    def __lt__(self, other):
        if not isinstance(other, Gene):
            raise ValueError(GENE_COMP_ERROR.format(type=type(other)))
        StatCounter.increment("comparisons")
        return self._dna < other._dna

    def __gt__(self, other):
        if not isinstance(other, Gene):
            raise ValueError(GENE_COMP_ERROR.format(type=type(other)))
        StatCounter.increment("comparisons")
        return self._dna > other._dna

    def __ge__(self, other):
        if not isinstance(other, Gene):
            raise ValueError(GENE_COMP_ERROR.format(type=type(other)))
        StatCounter.increment("comparisons")
        return self._dna >= other._dna

    def __hash__(self):
        StatCounter.increment("hashes")
        if self._dna is None:
            return 0
        value = ord(self._dna[0]) << 7
        for char in self._dna:
            value = self.__c_mul(1000003, value) ^ ord(char)
        value = value ^ len(self._dna)
        if value == -1:
            value = -2
        # The result is trimmed down to 31 bits (plus a sign bit) to give
        # consistent results on 32 and 64 bit systems
        # Otherwise hash() will implicitly do this based on the Python build
        # see https://docs.python.org/3/reference/datamodel.html#object.__hash__
        value = value % 0b0111_1111_1111_1111_1111_1111_1111_1111
        return value

    def __c_mul(self, a, b):
        return (int(a) * int(b)) & 0xFFFFFFFF


class GeneLink(object):
    """A single link/node in a GeneLinkedList. It has two attributes:
    1. data: typically a (gene, disease) tuple in the assignment context (but, in general, could contain anything)
    2. next_node, which is pointer to another GeneLink.
    Basically, think of this as a node in a linked list.
    """

    def __init__(self, data):
        self.data = data
        self.next_node = None

    def __str__(self):
        return "({})".format(str(self.data)) + " -> " + str(self.next_node)


class GeneLinkedList(object):
    """A linked list of GeneLinks."""

    def __init__(self):
        self.head = None

    def __iter__(self):
        raise ValueError("It would be no fun if we did this for you!")

    def __str__(self):
        return str(self.head)


class GeneBstNode:
    """A single Bst Node."""

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


def bst_nested_repr(root):
    """Returns a str of the nested list representation of the tree
    starting at the given node"""
    if root:
        left_repr = bst_nested_repr(root.left)
        right_repr = bst_nested_repr(root.right)
        result = f"[{repr(root.key)}:{repr(root.value)}, "
        result += f"{left_repr}, "
        result += f"{right_repr}]"
    else:
        result = "None"
    return result
