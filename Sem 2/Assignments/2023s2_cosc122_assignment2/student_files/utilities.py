"""
utilities.py
A collection of useful structures to complete this assignment.
"""

import stats
import os
import shutil
import random
from classes2 import Gene

DATA_DIR = "./test_data/"



GENE_LENGTH = 16


def make_gene_list(iterable, sort_order=None):
    """Takes an iterable of strings and returns a list of Gene objects.
    This is helpful when testing.
    sort_order can be given as 'name', or 'random' with obvious results - see below.
    For example:
    >>> make_name_list(['a', 'b', 'c', 'd')
    returns a list with [Gene('a'), Gene('b')...]
    >>> make_name_list('abcd')
    also returns a list with [Gene('a'), Gene('b')...]
    """
    results = []
    for string in iterable:
        results.append(Gene(string))
    if sort_order == "gene":
        results.sort()
    elif sort_order == "random":
        random.shuffle(results)
    # else leave in the order they were given
    return results


def take(sequence, n):
    """Take the first min(n, len(sequence)) items from sequence.
    >>> genes = take(GeneSequenceGenerator(), 10)
    >>> print(list(genes))
    """
    i = 0
    seq = iter(sequence)
    while seq and i < n:
        yield next(seq)
        i += 1


def read_test_data(filename):
    """Read in the test data from the file given by `filename`,
    returns `(disease_info, patient, suffers_from)` for that file.
    For example:
    to read the file test_data-1d-2g-1-a.txt and

    >>> filename = "test_data-1d-2g-1-a.txt"
    >>> disease_info, patient, suffers_from = read_test_data(filename)
    """
    disease_info = []
    patient = []
    suffers_from = []
    with open(filename) as test_data_file:
        # Read details of diseases
        current_line = _get_next_line(test_data_file)

        disease_size = int(current_line)
        for _ in range(disease_size):
            current_line = _get_next_line(test_data_file)
            gene_str, disease = current_line.split(",", maxsplit=1)
            record = (Gene(gene_str), disease)
            disease_info.append(record)

        # Read patient genes
        current_line = _get_next_line(test_data_file)
        patient_size = int(current_line)
        for _ in range(patient_size):
            current_line = _get_next_line(test_data_file)
            patient.append(Gene(current_line))

        # Read expected diseases for patient
        current_line = _get_next_line(test_data_file)
        suffers_from_size = int(current_line)
        for _ in range(suffers_from_size):
            current_line = _get_next_line(test_data_file)
            # print(current_line)
            disease = current_line.strip()
            suffers_from.append(disease)

    return disease_info, patient, suffers_from


def _get_next_line(test_data_file):
    """Reads and returns one line from a test data file. Returns None if the end
    of file is reached."""
    current_line = test_data_file.readline()
    # Comment lines are not read.
    while current_line.startswith("#"):
        current_line = test_data_file.readline()

    # None is returned if the end of the file is reached.
    if len(current_line) == 0:
        return None
    return current_line.rstrip()


class GeneSequenceGenerator:
    """Generate a sequence of genes"""

    def __init__(self, max_size=None):
        self.max_size = max_size if max_size is not None else float("inf")

    def __iter__(self):
        i = 0
        while i < self.max_size:
            gene = ""
            for _ in range(GENE_LENGTH):
                gene += random.choice("acgt")
            yield Gene(gene)
            i += 1
