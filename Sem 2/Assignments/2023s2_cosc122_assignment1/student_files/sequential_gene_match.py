""" Filename: sequential_gene_match.py
    Author: Luke Donaldson-Scott

A module for finding the genetic similarity between
two genomes using a linear search.
"""
 # rom classes import Genome, Gene
from classes import GeneList

# Uncomment the following line to be able to make your own testing Genes
<<<<<<< HEAD
from classes import Genome, Gene
=======
from classes import Gene, Genome
>>>>>>> 8533c15da2f5f3100e11b7c3f1758848649304e5

def sequential_gene_match(first_genome, second_genome):
    """ This function takes two Genome objects, and returns a GeneList
        and an integer. The GeneList is of all genes that are common
        between first_genome and second_genome, while the integer is how many
        comparisons it took to find all the similar genes.
        The Genes in the result GeneList should be in the same order as
        they appear in first_genome.
    """
    common_genes = GeneList()
    comparisons = 0
<<<<<<< HEAD
    # ===start student section===
    for gene1 in first_genome:
        # Iterate through genes in the second genome
=======
    # ---start student section---
    for gene1 in first_genome:
>>>>>>> 8533c15da2f5f3100e11b7c3f1758848649304e5
        for gene2 in second_genome:
            comparisons += 1
            if gene1 == gene2:
                common_genes.append(gene1)
<<<<<<< HEAD
    # ===end student section===
=======
                break    
     # ===end student section===
>>>>>>> 8533c15da2f5f3100e11b7c3f1758848649304e5
    return common_genes, comparisons


genome1 = Genome([Gene('atcg'), Gene('ctga')])
genome2 = Genome([Gene('gtcg'), Gene('atcg')])
print(sequential_gene_match(genome1, genome2))
