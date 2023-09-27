"""
Author: Luke Donaldson-Scott

This is a module that implements a GeneBst and various supporting functions.

You should count each `Gene` comparison that is made.
See the handout for how to do this.
"""
import sys
from classes2 import Gene, GeneBstNode, bst_nested_repr

sys.setrecursionlimit(10**6)

# note you might want to import other things here for testing
# but your submission should only include the import line above.



class GeneBst:
    """A Gene Binary Search Tree stores Gene objects for efficient
    matching of genes to diseases, meaning faster diagnosis for
    patients.
    """

    def __init__(self, root=None):
        self.root = root
        self.comparisons = 0

    def insert(self, gene, disease):
        """
        Stores the gene, disease pair in the BST tree.
        This function updates an existing tree so:
        - If self.root is None set self.root to be a new GeneBstNode.
        - Returns Nothing
        - Assumes the gene is unlikely to already be in the tree and shouldn't check
          for the gene being in the current node first. Your code isn't limited to one
          comparison per loop but it shouldn't use the equality comparison first.
          You must figure out which gene comparison is done first.
          The SimpleBstStoreTests will help you figure it out. We recommend copying
          some of them over to your module and adjusting them for testing. You will
          waant to change the code to print stuff rather than using assertions.
        - If the gene already exists then the disease in that node should be updated
          to the given disease. This means that genes in the bst will be unique.
        - Any gene comparisons used should be kept track of via self.comparisons.
        NOTE: You shouldn't use recursion here as it will eventually cause
        Python to blow-up when testing large, worst case, data sets.
        """
        # ---start student section---
        if self.root is None:
            self.root = GeneBstNode(gene, disease)
        else:
            current = self.root
            while True:
                self.comparisons += 1
                if gene < current.gene:  # Access 'gene' directly
                    if current.left is None:
                        current.left = GeneBstNode(gene, disease)
                        break
                    else:
                        current = current.left
                elif gene > current.gene:  # Access 'gene' directly
                    if current.right is None:
                        current.right = GeneBstNode(gene, disease)
                        break
                    else:
                        current = current.right
                else:  # Gene already exists, update the disease
                    current.disease = disease  # Access 'disease' directly
                    break

        # ===end student section===

    def __getitem__(self, gene):
        """Returns the value associated with the given gene,
           or None if the gene is not present in the tree.
        - Your search should only check that the root contains the gene
          after ruling out that the gene can't be in a sub tree.
        - That is check if you need to search one of the sub trees first.
          The tests expect a specific comparison to be first, you will
          need to figure out which one it is :)
        - Any gene comparisons used should be kept track of via self.comparisons.
        NOTE: You shouldn't use recursion here as it will eventually cause
        Python to blow-up when testing large, worst case, data sets.
        """
        value = None
        # ---start student section---
        current = self.root
        while current:
            self.comparisons += 1
            if gene < current.gene:  # Access 'gene' directly
                current = current.left
            elif gene > current.gene:  # Access 'gene' directly
                current = current.right
            else:  # Gene found
                return current.disease  # Access 'disease' directly
        # ===end student section===
        return value

    def __len__(self):
        return num_nodes_in_tree(self.root)

    def __repr__(self):
        return bst_nested_repr(self.root)


def num_nodes_in_tree(root):
    """Returns the number of nodes in the tree starting at root.
    If the root is None then the number of nodes is zero.
    NOTE: recursion recommended here.
    """
    num_nodes = 0
    # ---start student section---
    if root is None:
        return 0
    num_nodes = 1 + num_nodes_in_tree(root.left) + num_nodes_in_tree(root.right)
    # ===end student section===
    return num_nodes


def bst_depth(root):
    """The level of a node is the number of edges from the root to the node
    The depth is the maximum level of nodes in a tree.
    Remember, the level of a node is how many edges there are on a path
    from the root to the node.
    So, the depth of a tree starting at the root is:
    - zero if the root is None
    - zero if the root has no children
    - 1 + the max depth of the trees starting at the left and right child
    NOTE: recursion recommended here.
    """
    depth = 0
    # ---start student section---
    if root is None:
        return 0
    depth = 1 + max(bst_depth(root.left), bst_depth(root.right))
    # ===end student section===
    return depth


def bst_in_order(root, result_list=None):
    """Returns a list containing (key, value) tuples
    from the bst, in the order of the keys.
    Basically does an in order traversal of the tree
    collecting (key, value) pairs as each node is visited.
    Returns an empty list if the root is None.
    This function shouldn't use any key comparisons!
    NOTE: recursion recommended here.
    """
    if result_list is None:
        result_list = []
    # ---start student section---
    if root:
        result_list = bst_in_order(root.left, result_list)
        result_list.append((root.gene, root.disease))
        result_list = bst_in_order(root.right, result_list)
    # ===end student section===
    return result_list


if __name__ == "__main__":
    # put your own simple tests here
    # you don't need to submit this code
    print("Add some tests here...")
