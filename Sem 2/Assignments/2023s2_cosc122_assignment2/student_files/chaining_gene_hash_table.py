"""
Author = your name should probably go here

This is a fun module that implements a ChainingGeneHashTable.

The table uses closed addressing.

A GeneLinkedList in each table slot is used to store
all the items that hash to a given slot.

You should count each gene comparison and each hash that is made.
"""

from classes2 import GeneLinkedList, GeneLink

# Uncomment the following line to be able to make your own testing Genes
# from classes2 import Gene


class ChainingGeneHashTable:
    """A Chaining Gene Hash Table stores Gene objects for efficient
    matching of genes to diseases, meaning faster diagnosis for
    patients. This particular variation makes use of linked lists
    to handle gene hash collisions.
    """

    def __init__(self, table_size):
        """Create a hash table of the correct size, reset counters.
        Be sure to use GeneLinkedList objects in your hash table.
        """
        self.table_size = table_size
        self.comparisons = 0
        self.hashes = 0
        self.hash_table = [GeneLinkedList() for _ in range(table_size)]

    def __str__(self):
        results = []
        for i, row in enumerate(self.hash_table):
            results.append(f"  {i}: {row}")
        results = [self.__class__.__name__ + "["] + results + ["]"]
        return "\n".join(results)

    def __getitem__(self, gene):
        """Look for the given gene in the hash table.
        If the gene is present, return its disease.
        If it is not, return None.
        """
        # ---start student section---
        pass
        # ===end student section===

    def insert(self, gene, disease):
        """Insert the given gene and disease into the hash table
        as a gene-disease pair (tuple).
        You may assume the gene has not been previously inserted
        into the table.
        """
        # ---start student section---
        pass
        # ===end student section===


if __name__ == "__main__":
    # put your own simple tests here
    # you don't need to submit this code
    print("Add some tests here...")

