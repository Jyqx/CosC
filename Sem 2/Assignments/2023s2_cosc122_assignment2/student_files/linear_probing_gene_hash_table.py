"""
Author: Luke Donaldson-Scott

This is a module that implements a LinearProbingGeneHashTable.

The table uses open addressing, ie, collisions are resolved by
using linear probing.

You should count each gene comparison and each hash that is made.
See the handout for how to do this.
"""


# Uncomment the following line to be able to make your own testing Genes
from classes2 import Gene


class LinearProbingGeneHashTable:
    """A Linear Probing Gene Hash Table stores Gene objects for efficient
    matching of genes to diseases, meaning faster diagnosis for
    patients. This particular variation uses linear probing
    to handle collisions.
    """

    def __init__(self, table_size):
        """Create a hash table of the correct size, reset counters."""
        self.table_size = table_size
        self.comparisons = 0
        self.hashes = 0
        self.hash_table = [None] * table_size

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

        # Calculate the initial hash index for the gene
        initial_index = hash(gene) % self.table_size
        index = initial_index
        self.hashes += 1

        # Keep probing linearly until we find the gene or an empty slot
        while self.hash_table[index] is not None:
            stored_gene, disease = self.hash_table[index]
            self.comparisons += 1  # Increment the comparison count

            if stored_gene == gene:
                return disease  # Gene found, return the associated disease

            # Continue linear probing
            index = (index + 1) % self.table_size

        # Gene not found in the table
        return None

        # ===end student section===

    def insert(self, gene, disease):
        """Insert the given gene and disease into the hash table
        as a gene-disease pair (tuple). If the table is full,
        raise IndexError("The table is now full.").
        You may assume the gene has not been previously inserted
        into the table.
        """
        # ---start student section---

        # Check if the table is now full
        # if self.hashes == self.table_size:
        #     raise IndexError("The table is now full.")

        # Calculate the initial hash index for the gene
        initial_index = hash(gene) % self.table_size
        self.hashes += 1
        index = initial_index

        # Find the next available slot for insertion (linear probing)
        while self.hash_table[index] is not None:
            index = (index + 1) % self.table_size

        # Insert the gene-disease pair into the table
        self.hash_table[index] = (gene, disease)

        # ===end student section===


# if __name__ == "__main__":
#     # Create a LinearProbingGeneHashTable with a small table size for testing
#     gene_table = LinearProbingGeneHashTable(5)

#     geneA = Gene('atcg')
#     geneB = Gene('tcga')
#     geneC = Gene('cgta')
#     geneD = Gene('agct')
#     geneE = Gene('gcta')

#     # Insert gene-disease pairs
#     gene_table.insert(geneA, "DiseaseA")
#     gene_table.insert(geneB, "DiseaseB")
#     gene_table.insert(geneC, "DiseaseC")
    
#     print(gene_table)

#     # Test the __getitem__ method
#     print(gene_table[geneA])  # Output: DiseaseA
#     print(gene_table[geneB])  # Output: DiseaseB
#     print(gene_table[geneC])  # Output: DiseaseC
#     print(gene_table[geneD])  # Output: None (not found)

#     # Test collision handling and linear probing
#     gene_table.insert(geneD, "DiseaseD")
#     print(gene_table[geneD])  # Output: DiseaseD

#     # Test inserting a gene when the table is full (should raise IndexError)
#     try:
#         gene_table.insert(geneE, "DiseaseE")
#     except IndexError as e:
#         print("Error:", e)  # Output: Error: The table is now full.

#     # Display the hash table
#     print(gene_table)
#     # Check the number of comparisons made
#     print("Comparisons:", gene_table.comparisons)