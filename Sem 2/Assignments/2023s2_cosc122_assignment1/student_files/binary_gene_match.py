""" Filename: binary_gene_match.py
    Author: your name should potentially go here

A module for finding the genetic similarity between 
two genomes using a binary search.
"""
from classes import GeneList


# Uncomment the following line to be able to make your own testing Genes
# from classes import Gene, Genome




def binary_gene_match(first_genome, second_genome):
    """ This function takes two Genome objects, and returns a GeneList
        and an integer.
        The second_genome will be in alphabetical/lexicographic order.
        The GeneList is of all genes that are common
        between first_genome and second_genome,
        while the integer is how many comparisons it took to find all 
        the similar genes.
        The Genes in the result GeneList should be in the same order as 
        they appear in first_genome.
        HINT: a helper function will be helpful :)
    """
    comparisons = 0
    common_genes = GeneList()
    # ---start student section---
    pass
    # ===end student section===
    return common_genes, comparisons
