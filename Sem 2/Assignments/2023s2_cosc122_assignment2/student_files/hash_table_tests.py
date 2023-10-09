"""
tests.py
A module of unit tests to verify your answers to the
genetic similarity functions.
"""
import shutil
import os
import time
import signal
import unittest
import math

from classes2 import Gene, GeneLinkedList, GeneLink
from stats import StatCounter, ACCESSES, COMPARISONS, HASHES, IS_MARKING_MODE
from utilities import read_test_data, DATA_DIR


from chaining_gene_hash_table import ChainingGeneHashTable
from linear_probing_gene_hash_table import LinearProbingGeneHashTable


TEST_FILE_FORMAT = DATA_DIR + "test_data-{db}{s1}-{genes}{s2}-{present}-a.txt"
real_count = StatCounter.get_count



# es


class TypeAssertion(object):
    def assertTypesEqual(self, a, b, msg=""):
        if type(a) != type(b):
            if not msg:
                template = "Type {} does not match type {}"
                error_msg = template.format(type(a), type(b))
            else:
                error_msg = msg
            raise AssertionError(error_msg)


class BaseTestGeneLookup(unittest.TestCase, TypeAssertion):
    def setUp(self):
        """Runs before every test case"""
        StatCounter.unlock()
        StatCounter.reset_counts()
        self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = self.end_time - self.start_time
        print(f"{test_time:.4f}s", end=" ")


    def get_bounds(
        self, table_size, gene_count, patient_genome_length, bad_gene_count, scale
    ):
        lower_bound = bad_gene_count
        upper_bound = patient_genome_length * int(
            scale * gene_count * gene_count / table_size
        )
        return lower_bound, upper_bound

    def run_disease_checker(self, table_size, disease_information, patient):
        """ Adds all the gene -> disease database info to a hash table.
        Then uses the hashtable to check for any disease related genes in the
        patient genome.
        """
        table = self.hash_table_class(table_size)
        diseases = []
        for gene, disease in disease_information:
            table.insert(gene, disease)
        for gene in patient:
            disease = table[gene]
            if disease is not None:
                diseases.append(disease)
        return (diseases, table.comparisons, table.hashes)

    def common_genes_test(self, test_file_name, table_size):
        """Test that the given hash table returns the correct
        result for the file specified by test_file_name.
        """
        disease_information, patient, true_answer = read_test_data(
            test_file_name)
        student_answer, _, _ = self.run_disease_checker(
            table_size, disease_information, patient
        )
        message_if_wrong = "Searching using your hash table doesn't produce"
        message_if_wrong += "the expected list of diseases.\nNote: "
        message_if_wrong += "Your list is the 1st list and the expected is the 2nd."
        self.assertEqual(student_answer, true_answer, msg=message_if_wrong)
        # es

    def _internal_counter_test(self, test_file_name, table_size, counter):
        """Test that the student has correctly counted the code against what
        we have counted. This does not mean that the count is correct, just
        that it was correctly counted.
        """
        disease_information, patient, expected_results = read_test_data(
            test_file_name)
        results, student_comps, student_hashes = self.run_disease_checker(
            table_size, disease_information, patient
        )
        actual_count = real_count(counter)
        if counter == COMPARISONS:
            student_count = student_comps
        else:
            student_count = student_hashes
        message_if_wrong = f"Your code reported using {student_count} Gene {counter} "
        message_if_wrong += f"but it actually used {actual_count}. "
        message_if_wrong += f"This means you are miscounting Gene {counter}, eg, "
        message_if_wrong += f"not counting Gene {counter} when they are made or "
        message_if_wrong += f"counting Gene {counter} that weren't made."
        self.assertEqual(student_count, actual_count, msg=message_if_wrong)

        if len(results) == 0 and len(expected_results) > 0:
            message_if_wrong = (
                f"Your code reported using {student_count} Gene {counter} "
            )
            message_if_wrong += f"and it actually used {actual_count}, but your code produced an empty results list. "
            message_if_wrong += (
                f"Double-check your insert and __getitem__ methods work correctly."
            )
            self.assertNotEqual(student_count, 0, msg=message_if_wrong)

    def internal_comparisons_test(self, test_file_name, table_size):
        """Test that the student has correctly counted the
        number of comparisons used. This does not mean that the count is correct,
        just that it was correctly counted.
        """
        self._internal_counter_test(test_file_name, table_size, COMPARISONS)

    def internal_hashes_test(self, test_file_name, table_size):
        """Test that the student has correctly counted the
        number of hashes used. This does not mean that the count is correct,
        just that it was correctly counted.
        """
        self._internal_counter_test(test_file_name, table_size, HASHES)

    def comparisons_test(self, test_file_name, table_size, scale=1, target=None):
        """Test that the number of comparisons that the student made is
        within the expected bounds (provided by self.get_bounds, or target)
        """
        disease_information, patient, true_answer = read_test_data(
            test_file_name)
        if target is None:
            lower_bound, upper_bound = self.get_bounds(
                table_size,
                len(disease_information),
                len(patient),
                len(true_answer),
                scale,
            )
        _, student_count, _ = self.run_disease_checker(
            table_size, disease_information, patient
        )
        if target is not None:
            message_if_wrong = (
                f"Your code reported using {student_count} Gene comparisons "
            )
            message_if_wrong += f"but it should have used {target} comparisons."
            self.assertEqual(student_count, target, msg=message_if_wrong)
        else:
            message_if_wrong = (
                f"Your code reported using {student_count} Gene comparisons "
            )
            message_if_wrong += (
                f"but it should use {lower_bound} <= comparisons <= {upper_bound}."
            )

            self.assertTrue(
                lower_bound <= student_count <= upper_bound, msg=message_if_wrong
            )

    def hashes_test(self, test_file_name, table_size):
        """Test that the number of hashes that the student made is
        within the expected bounds.
        """
        disease_information, patient, _ = read_test_data(test_file_name)
        _, _, student_hashes = self.run_disease_checker(
            table_size, disease_information, patient
        )
        target_hashes = len(patient) + len(disease_information)
        message_if_wrong = (
            f"Your code reported using {student_hashes} Gene hashes "
        )
        message_if_wrong += f"but it should have used {target_hashes} hashes."
        self.assertEqual(student_hashes, target_hashes, msg=message_if_wrong)


class EmptyDatasetTests(BaseTestGeneLookup):
    # == Tests with an empty dataset ==#

    def test_empty(self):
        test_file = TEST_FILE_FORMAT.format(
            db=0, s1="d", genes=0, s2="r", present=0)
        self.common_genes_test(test_file, table_size=1)

    def test_empty_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=0, s1="d", genes=0, s2="r", present=0)
        self.internal_comparisons_test(test_file, table_size=1)

    def test_empty_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=0, s1="d", genes=0, s2="r", present=0)
        self.internal_hashes_test(test_file, table_size=1)

    def test_empty_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=0, s1="d", genes=0, s2="r", present=0)
        self.comparisons_test(test_file, table_size=1, scale=1)

    def test_empty_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=0, s1="d", genes=0, s2="r", present=0)
        self.hashes_test(test_file, table_size=1)


class TrivialDatasetTests(BaseTestGeneLookup):
    # == Tests with a trivially tiny dataset ==#

    def test_tiny(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1, s1="d", genes=2, s2="r", present=1)
        self.common_genes_test(test_file, table_size=1)

    def test_tiny_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1, s1="d", genes=2, s2="r", present=1)
        self.internal_comparisons_test(test_file, table_size=1)

    def test_tiny_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1, s1="d", genes=2, s2="r", present=1)
        self.internal_hashes_test(test_file, table_size=1)

    def test_tiny_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1, s1="d", genes=2, s2="r", present=1)
        self.comparisons_test(test_file, table_size=1, scale=1)

    def test_tiny_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1, s1="d", genes=2, s2="r", present=1)
        self.hashes_test(test_file, table_size=1)


class SmallDatasetTests(BaseTestGeneLookup):
    # == Tests with a small dataset ==#

    def test_small_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.common_genes_test(test_file, table_size=50)

    def test_small_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_comparisons_test(test_file, table_size=50)

    def test_small_tiny_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_hashes_test(test_file, table_size=50)

    def test_small_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.comparisons_test(test_file, table_size=50, scale=0.5)

    def test_small_tiny_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.hashes_test(test_file, table_size=50)

    def test_small_low_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.common_genes_test(test_file, table_size=30)

    def test_small_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_comparisons_test(test_file, table_size=30)

    def test_small_low_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_hashes_test(test_file, table_size=30)

    def test_small_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.comparisons_test(test_file, table_size=30, scale=0.3)

    def test_small_low_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.hashes_test(test_file, table_size=30)

    def test_small_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.common_genes_test(test_file, table_size=15)

    def test_small_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_comparisons_test(test_file, table_size=15)

    def test_small_medium_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_hashes_test(test_file, table_size=15)

    def test_small_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.comparisons_test(test_file, table_size=15, scale=0.3)

    def test_small_medium_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.hashes_test(test_file, table_size=15)

    def test_small_high_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.common_genes_test(test_file, table_size=11)

    def test_small_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_comparisons_test(test_file, table_size=11)

    def test_small_high_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_hashes_test(test_file, table_size=11)

    def test_small_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.comparisons_test(test_file, table_size=11, scale=0.9)

    def test_small_high_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.hashes_test(test_file, table_size=11)

    def test_small_full_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.common_genes_test(test_file, table_size=10)

    def test_small_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_comparisons_test(test_file, table_size=10)

    def test_small_full_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.internal_hashes_test(test_file, table_size=10)

    def test_small_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.comparisons_test(test_file, table_size=10, scale=1)

    def test_small_full_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=50, s2="r", present=2)
        self.hashes_test(test_file, table_size=10)


class MediumDatasetTests(BaseTestGeneLookup):
    # == Tests with a medium dataset ==#

    def test_medium_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.common_genes_test(test_file, table_size=200)

    def test_medium_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_comparisons_test(test_file, table_size=200)

    def test_medium_tiny_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_hashes_test(test_file, table_size=200)

    def test_medium_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.comparisons_test(test_file, table_size=200, scale=0.2)

    def test_meduim_tiny_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.hashes_test(test_file, table_size=200)

    def test_medium_low_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.common_genes_test(test_file, table_size=150)

    def test_medium_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_comparisons_test(test_file, table_size=150)

    def test_medium_low_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_hashes_test(test_file, table_size=150)

    def test_medium_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.comparisons_test(test_file, table_size=150, scale=0.2)

    def test_meduim_low_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.hashes_test(test_file, table_size=150)

    def test_medium_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.common_genes_test(test_file, table_size=100)

    def test_medium_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_comparisons_test(test_file, table_size=100)

    def test_medium_medium_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_hashes_test(test_file, table_size=100)

    def test_medium_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.comparisons_test(test_file, table_size=100, scale=0.1)

    def test_meduim_medium_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.hashes_test(test_file, table_size=100)

    def test_medium_high_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.common_genes_test(test_file, table_size=60)

    def test_medium_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_comparisons_test(test_file, table_size=60)

    def test_medium_high_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_hashes_test(test_file, table_size=60)

    def test_medium_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.comparisons_test(test_file, table_size=60, scale=0.25)

    def test_meduim_high_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.hashes_test(test_file, table_size=60)

    def test_medium_full_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.common_genes_test(test_file, table_size=50)

    def test_medium_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_comparisons_test(test_file, table_size=50)

    def test_medium_full_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.internal_hashes_test(test_file, table_size=50)

    def test_medium_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.comparisons_test(test_file, table_size=50, scale=1)

    def test_meduim_full_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=50, s1="d", genes=50, s2="r", present=50)
        self.hashes_test(test_file, table_size=50)


class LargeDatasetTests(BaseTestGeneLookup):
    # == Tests with a large dataset ==#

    def test_large_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=5000)

    def test_large_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=5000)

    def test_large_tiny_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=5000)

    def test_large_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=5000, scale=0.1)

    def test_large_tiny_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=5000)

    def test_large_low_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=2500)

    def test_large_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=2500)

    def test_large_low_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=2500)

    def test_large_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=2500, scale=0.1)

    def test_large_low_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=2500)

    def test_large_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=1250)

    def test_large_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=1250)

    def test_large_meduim_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=1250)

    def test_large_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=1250, scale=0.1)

    def test_large_medium_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=1250)

    def test_large_high_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=1050)

    def test_large_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=1050)

    def test_large_high_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=1050)

    def test_large_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=1050, scale=0.1)

    def test_large_high_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=1050)

    def test_large_full_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=1000)

    def test_large_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=1000)

    def test_large_full_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_hashes_test(test_file, table_size=1000)

    def test_large_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=1000, scale=1)

    def test_large_full_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=1000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=1000)


class HugeDatasetTests(BaseTestGeneLookup):
    # == Tests with a huge dataset ==#

    def test_huge_tiny_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=50000)

    def test_huge_tiny_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=50000)

    def test_huge_tiny_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=50000)

    def test_huge_tiny_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=50000, scale=0.1)

    def test_huge_tiny_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=50000)

    def test_huge_low_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=25000)

    def test_huge_low_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=25000)

    def test_huge_low_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=25000)

    def test_huge_low_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=25000, scale=0.1)

    def test_huge_low_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=25000)

    def test_huge_medium_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=12500)

    def test_huge_medium_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=12500)

    def test_huge_meduim_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=12500)

    def test_huge_medium_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=12500, scale=0.1)

    def test_huge_medium_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=12500)

    def test_huge_high_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=10500)

    def test_huge_high_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=10500)

    def test_huge_high_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=10500)

    def test_huge_high_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=10500, scale=0.1)

    def test_huge_high_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=10500)

    def test_huge_full_load(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.common_genes_test(test_file, table_size=10000)

    def test_huge_full_load_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_comparisons_test(test_file, table_size=10000)

    def test_huge_full_load_internal_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.internal_hashes_test(test_file, table_size=10000)

    def test_huge_full_load_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.comparisons_test(test_file, table_size=10000, scale=1)

    def test_huge_full_load_hashes(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10000, s1="d", genes=1000, s2="r", present=50
        )
        self.hashes_test(test_file, table_size=10000)






class TestGeneLookupChaining(BaseTestGeneLookup):
    """Unit tests for the chaining hash table."""

    def setUp(self):
        self.hash_table_class = ChainingGeneHashTable
        super().setUp()


class ChainingEmptyTestGeneLookup(TestGeneLookupChaining, EmptyDatasetTests):
    pass


class ChainingTrivialTestGeneLookup(TestGeneLookupChaining, TrivialDatasetTests):
    pass


class ChainingSmallTestGeneLookup(TestGeneLookupChaining, SmallDatasetTests):
    pass


class ChainingMediumTestGeneLookup(TestGeneLookupChaining, MediumDatasetTests):
    pass


class ChainingLargeTestGeneLookup(TestGeneLookupChaining, LargeDatasetTests):
    pass


class ChainingHugeTestGeneLookup(TestGeneLookupChaining, HugeDatasetTests):
    pass


class TestGeneLookupLinearProbing(BaseTestGeneLookup):
    """Unit tests for the linear probing hash table."""

    def setUp(self):
        self.hash_table_class = LinearProbingGeneHashTable
        super().setUp()

    def test_overfull_table(self):
        test_file = TEST_FILE_FORMAT.format(
            db=10, s1="d", genes=2, s2="r", present=2)
        with self.assertRaises(IndexError):
            self.common_genes_test(test_file, table_size=9)


class LinearProbingEmptyTestGeneLookup(TestGeneLookupLinearProbing, EmptyDatasetTests):
    pass


class LinearProbingTrivialTestGeneLookup(
    TestGeneLookupLinearProbing, TrivialDatasetTests
):
    pass


class LinearProbingSmallTestGeneLookup(TestGeneLookupLinearProbing, SmallDatasetTests):
    pass


class LinearProbingMediumTestGeneLookup(
    TestGeneLookupLinearProbing, MediumDatasetTests
):
    pass


class LinearProbingLargeTestGeneLookup(TestGeneLookupLinearProbing, LargeDatasetTests):
    pass


class LinearProbingHugeTestGeneLookup(TestGeneLookupLinearProbing, HugeDatasetTests):
    pass


def all_tests_suite():
    """Combines test cases from various classes to make a
    big suite of tests to run.
    You can comment out tests you don't want to run and uncomment
    tests that you do want to run :)
    """
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase

    # suite.addTest(test_loader(LinearProbingEmptyTestGeneLookup))
    # suite.addTest(test_loader(LinearProbingTrivialTestGeneLookup))
    # suite.addTest(test_loader(LinearProbingSmallTestGeneLookup))
    # suite.addTest(test_loader(LinearProbingMediumTestGeneLookup))
    suite.addTest(test_loader(LinearProbingLargeTestGeneLookup))
    # suite.addTest(test_loader(LinearProbingHugeTestGeneLookup))

    # uncomment the following line when ready for chaining...
    # suite.addTest(test_loader(ChainingEmptyTestGeneLookup))
    # suite.addTest(test_loader(ChainingTrivialTestGeneLookup))
    # suite.addTest(test_loader(ChainingSmallTestGeneLookup))
    # suite.addTest(test_loader(ChainingMediumTestGeneLookup))
    # suite.addTest(test_loader(ChainingLargeTestGeneLookup))
    # suite.addTest(test_loader(ChainingHugeTestGeneLookup))

    return suite


    # # suite.addTest(test_loader(LinearProbingHugeTestGeneLookup))


def main():
    """Makes a test suite and runs it. Will your code pass?"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)



if __name__ == "__main__":
    main()
