"""Module containing the unit tests for the result getting functions."""
import signal
import os
import shutil
import utilities
import unittest
import math
import random
import json
import sys
import time
from classes2 import GeneBstNode, Gene, bst_nested_repr

from bst_module import GeneBst, bst_depth, bst_in_order, num_nodes_in_tree

# from hash_module import HashTable, hash_result_finder
from stats import IS_MARKING_MODE, COMPARISONS, StatCounter
from utilities import read_test_data, make_gene_list

sys.setrecursionlimit(10**6)

actual_count = StatCounter.get_count
lock_counter = StatCounter.lock
unlock_counter = StatCounter.unlock
DATA_DIR = utilities.DATA_DIR
SEED = "a"


def intersect_size_from_filename(filename):
    """Returns the number of diseases a patient may have.
    Basically the size of the intersection of genes
    between the two lists.
    eg
    ig filename is 'test_data-20i-10r-5-a.txt'
    then this function would return 5
    """
    bits = filename.split("-")
    return int(bits[3])


def gene_disease_size_from_filename(filename):
    """Returns the number of gene disease pairs.
    eg
    ig filename is 'test_data-20i-10r-5-a.txt'
    then this function would return 20
    """
    bits = filename.split("-")
    raw = bits[1].strip("in")
    return int(raw)


def read_expected_comps(filename):
    """Reads a dictionary containing expected comparisons
    for each test data file with the given method from
    the given file.
    Returns a dictionary mapping data file genes to comparisons.
    """
    full_filename = os.path.abspath(os.path.join(DATA_DIR, filename))
    with open(full_filename) as infile:
        data = infile.read()
        expected_comps_dict = json.loads(data)
    return expected_comps_dict


def read_tested_mins_and_maxs(filename):
    """Reads a dictionary containing expected min and max genes in
    the expected list in the given file
    Returns a dictionary mapping data file genes to comparisons.
    """
    full_filename = os.path.abspath(DATA_DIR + filename)
    with open(full_filename) as infile:
        data = infile.read()
        expected_comps_dict = json.loads(data)
    return expected_comps_dict


# load as a global constants so file isn't loaded over and over :)
BST_EXPECTED_COMPS_FILENAME = "expected_bst_comps.txt"

if IS_MARKING_MODE:
    BST_EXPECTED_COMPS = "Can't use BST_EXPECTED_COMPS in marking mode!!!"
else:
    BST_EXPECTED_COMPS = read_expected_comps(BST_EXPECTED_COMPS_FILENAME)




class BaseTester(unittest.TestCase):
    def setUp(self):
        """This runs before each test case"""
        unlock_counter()
        StatCounter.reset_counts()
        self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = self.end_time - self.start_time
        print(f"{test_time:.4f}s", end=" ")


    def AssertListsEqual(self, list1, list2, msg=None):
        """Locks the counter when comparing lists"""
        lock_counter()
        self.assertEqual(list1, list2, msg=msg)
        unlock_counter()

    def AssertListInOrder(self, alist):
        """Checks to see if list is in order"""
        lock_counter()
        message_if_wrong = (
            "Your list should have been in ascending order, but it was not."
        )
        for i in range(1, len(alist)):
            self.assertLessEqual(alist[i - 1], alist[i], msg=message_if_wrong)
        unlock_counter()


class BaseTests(BaseTester):
    def get_bounds(self, left_length, right_length):
        raise NotImplementedError(
            "This method should be implemented by a subclass.")

    def result_list_test(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        disease_info, patient, expected_results = read_test_data(
            test_file_location)
        results, comparisons = self.function_to_test(disease_info, patient)

        message_if_wrong = "Your answer list doesn't match the expected answer list. "
        message_if_wrong += (
            "Note: Your list is the first list and the expected is the second."
        )
        self.AssertListsEqual(results, expected_results, msg=message_if_wrong)
        message_if_wrong = "Your answer list isn't the same type as the expected list!"
        self.assertEqual(type(results), type(
            expected_results), msg=message_if_wrong)

    def exact_comparisons_test(self, test_filename):
        # checks vs an exact number of comparisons
        # as opposed to a range
        test_file_location = DATA_DIR + test_filename
        disease_info, patient, expected_results = read_test_data(
            test_file_location)
        results, student_comparisons = self.function_to_test(
            disease_info, patient)
        intersect_size = intersect_size_from_filename(test_filename)
        expected_comparisons = self.expected_comparisons_dict[test_filename]

        message_if_wrong = (
            f"Your code reported using {student_comparisons} Gene comparisons "
        )
        message_if_wrong += (
            f"but it should have used {expected_comparisons} comparisons."
        )
        self.assertEqual(
            student_comparisons, expected_comparisons, msg=message_if_wrong
        )

    def internal_comparisons_test(self, test_filename):
        # checks that the reported/returned number of comparisons
        # equals the actual number of comparisons carried out
        test_file_location = DATA_DIR + test_filename
        disease_info, patient, expected_results = read_test_data(
            test_file_location)
        results, student_comparisons = self.function_to_test(
            disease_info, patient)
        true_comparisons = actual_count(COMPARISONS)

        message_if_wrong = (
            f"Your code reported using {student_comparisons} Gene {COMPARISONS} "
        )
        message_if_wrong += f"but it actually used {true_comparisons}. "
        message_if_wrong += f"This means you are miscounting Gene {COMPARISONS}, eg, "
        message_if_wrong += f"not counting Gene {COMPARISONS} when they are made or "
        message_if_wrong += f"counting Gene {COMPARISONS} that weren't made."
        self.assertEqual(student_comparisons,
                         true_comparisons, msg=message_if_wrong)

        if len(results) == 0 and len(expected_results) > 0:
            message_if_wrong = (
                f"Your code reported using {student_comparisons} Gene {COMPARISONS} "
            )
            message_if_wrong += f"and it actually used {true_comparisons}, but your code produced an empty results list. "
            message_if_wrong += (
                f"Double-check your insert and __getitem__ methods work correctly."
            )
            self.assertNotEqual(student_comparisons, 0, msg=message_if_wrong)

    def both_comparisons_test(self, test_filename):
        # checks vs an exact number of comparisons
        # and also checks that the reported comps matches actual comps
        test_file_location = DATA_DIR + test_filename
        disease_info, patient, expected_results = read_test_data(
            test_file_location)
        results, student_comparisons = self.function_to_test(
            disease_info, patient)
        intersect_size = intersect_size_from_filename(test_filename)
        expected_comparisons = self.expected_comparisons_dict[test_filename]

        message_if_wrong = (
            f"Your code reported using {student_comparisons} Gene comparisons "
        )
        message_if_wrong += (
            f"but it should have used {expected_comparisons} comparisons."
        )
        self.assertEqual(
            student_comparisons, expected_comparisons, msg=message_if_wrong
        )

        true_comparisons = actual_count(COMPARISONS)
        message_if_wrong = (
            f"Your code reported using {student_comparisons} Gene {COMPARISONS} "
        )
        message_if_wrong += f"but it actually used {true_comparisons}. "
        message_if_wrong += f"This means you are miscounting Gene {COMPARISONS}, eg, "
        message_if_wrong += f"not counting Gene {COMPARISONS} when they are made or "
        message_if_wrong += f"counting Gene {COMPARISONS} that weren't made."
        self.assertEqual(student_comparisons,
                         true_comparisons, msg=message_if_wrong)





class TrivialListTest(BaseTests):
    def setUp(self):
        super().setUp()

    def test_single_result_small(self):
        filename = "test_data-10g-10g-1-a.txt"
        self.result_list_test(filename)


class SmallTests(BaseTests):
    def setUp(self):
        super().setUp()

    def test_no_results_small(self):
        filename = "test_data-10g-10g-0-a.txt"
        self.result_list_test(filename)

    def test_single_results_small(self):
        filename = "test_data-10g-10g-1-a.txt"
        self.result_list_test(filename)

    def test_10_results_small(self):
        filename = "test_data-10g-10g-10-a.txt"
        self.result_list_test(filename)

    def test_no_results_small_exact_comparisons(self):
        filename = "test_data-10g-10g-0-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_exact_comparisons(self):
        filename = "test_data-10g-10g-1-a.txt"
        self.exact_comparisons_test(filename)

    def test_10_results_small_exact_comparisons(self):
        filename = "test_data-10g-10g-10-a.txt"
        self.exact_comparisons_test(filename)

    def test_no_results_small_internal_comparisons(self):
        filename = "test_data-10g-10g-0-a.txt"
        self.internal_comparisons_test(filename)

    def test_single_results_small_internal_comparisons(self):
        filename = "test_data-10g-10g-1-a.txt"
        self.internal_comparisons_test(filename)

    def test_10_results_small_internal_comparisons(self):
        filename = "test_data-10g-10g-10-a.txt"
        self.internal_comparisons_test(filename)


class MediumTests(BaseTests):
    def setUp(self):
        super().setUp()

    def test_no_results_medium(self):
        filename = "test_data-50d-50r-0-a.txt"
        self.result_list_test(filename)

    def test_no_results_medium_exact_comparisons(self):
        filename = "test_data-50d-50r-0-a.txt"
        self.exact_comparisons_test(filename)

    def test_no_results_medium_internal_comparisons(self):
        filename = "test_data-50d-50r-0-a.txt"
        self.internal_comparisons_test(filename)

    def test_single_results_medium(self):
        filename = "test_data-50d-50r-1-a.txt"
        self.result_list_test(filename)

    def test_single_results_medium_exact_comparisons(self):
        filename = "test_data-50d-50r-1-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_medium_internal_comparisons(self):
        filename = "test_data-50d-50r-1-a.txt"
        self.internal_comparisons_test(filename)

    def test_10_results_medium(self):
        filename = "test_data-50d-50r-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_medium_exact_comparisons(self):
        filename = "test_data-50d-50r-10-a.txt"
        self.exact_comparisons_test(filename)

    def test_10_results_medium_internal_comparisons(self):
        filename = "test_data-50d-50r-10-a.txt"
        self.internal_comparisons_test(filename)


class BigTests(BaseTests):
    def setUp(self):
        super().setUp()

    def test_no_results_big(self):
        filename = "test_data-1000d-1000g-0-a.txt"
        self.result_list_test(filename)

    def test_no_results_big_exact_comparisons(self):
        filename = "test_data-1000d-1000g-0-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_big(self):
        filename = "test_data-1000d-1000g-1-a.txt"
        self.result_list_test(filename)

    def test_single_results_big_exact_comparisons(self):
        filename = "test_data-1000d-1000g-1-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_big_internal_comparisons(self):
        filename = "test_data-1000d-1000g-1-a.txt"
        self.internal_comparisons_test(filename)

    def test_10_results_big(self):
        filename = "test_data-1000d-1000g-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_big_exact_comparisons(self):
        filename = "test_data-1000d-1000g-10-a.txt"
        self.exact_comparisons_test(filename)

    def test_10_results_big_internal_comparisons(self):
        filename = "test_data-1000d-1000g-10-a.txt"
        self.internal_comparisons_test(filename)

        # And some bad ones...

    def test_10_results_big_bad(self):
        filename = "test_data-1000g-1000g-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_big_bad_exact_comparisons(self):
        filename = "test_data-1000g-1000g-10-a.txt"
        self.exact_comparisons_test(filename)

    def test_10_results_big_bad_internal_comparisons(self):
        filename = "test_data-1000g-1000g-10-a.txt"
        self.internal_comparisons_test(filename)


class HugeTests(BaseTests):
    def setUp(self):
        super().setUp()

    def test_no_results_huge(self):
        filename = "test_data-10000d-50r-0-a.txt"
        self.result_list_test(filename)

    def test_no_results_huge_both_comparisons(self):
        filename = "test_data-10000d-50r-0-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_huge(self):
        filename = "test_data-10000d-50r-1-a.txt"
        self.result_list_test(filename)

    def test_single_results_huge_both_comparisons(self):
        filename = "test_data-10000d-50r-1-a.txt"
        self.both_comparisons_test(filename)

    def test_10_results_huge(self):
        filename = "test_data-10000d-50r-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_huge_both_comparisons(self):
        filename = "test_data-10000d-50r-10-a.txt"
        self.both_comparisons_test(filename)

    def test_10_results_huge(self):
        filename = "test_data-10000d-50r-50-a.txt"
        self.result_list_test(filename)

    def test_10_results_huge_both_comparisons(self):
        filename = "test_data-10000d-50r-50-a.txt"
        self.both_comparisons_test(filename)


class HugeSortedTests(BaseTests):
    def test_10_results_huge_sorted(self):
        filename = "test_data-10000g-50r-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_huge_both_comparisons_sorted(self):
        filename = "test_data-10000g-50r-10-a.txt"
        self.both_comparisons_test(filename)


class GinormousTests(BaseTests):
    def setUp(self):
        super().setUp()

    def test_no_results_ginormous_bad(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = "test_data-10000g-1000r-0-a.txt"
        self.result_list_test(filename)

    def test_no_results_ginormous_bad_both_comparisons(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = "test_data-10000g-1000r-0-a.txt"
        self.both_comparisons_test(filename)

    def test_single_result_ginormous_bad(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = "test_data-10000g-1000r-1-a.txt"
        self.result_list_test(filename)

    def test_single_result_ginormous_bad_both_comparisons(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = "test_data-10000g-1000r-1-a.txt"
        self.both_comparisons_test(filename)

    def test_10_results_ginormous_bad(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = "test_data-10000g-1000r-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_ginormous_bad_both_comparisons(self):
        # adding from sorted list is bad as it makes a max depth tree!
        filename = "test_data-10000g-1000r-10-a.txt"
        self.both_comparisons_test(filename)

    def test_no_results_ginormous_good(self):
        # notice how much quicker this is, thanks to a more balanced tree :)
        filename = "test_data-10000d-1000r-0-a.txt"
        self.result_list_test(filename)

    def test_no_results_ginormous_good_exact_comparisons(self):
        filename = "test_data-10000d-1000r-0-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_ginormous_good(self):
        filename = "test_data-10000d-1000r-1-a.txt"
        self.result_list_test(filename)

    def test_single_results_ginormous_good_exact_comparisons(self):
        filename = "test_data-10000d-1000r-1-a.txt"
        self.exact_comparisons_test(filename)

    def test_single_results_ginormous_good_internal_comparisons(self):
        filename = "test_data-10000d-1000r-1-a.txt"
        self.internal_comparisons_test(filename)

    def test_10_results_ginormous_good_exact_comparisons(self):
        filename = "test_data-10000d-1000r-10-a.txt"
        self.exact_comparisons_test(filename)

    def test_10_results_ginormous_good(self):
        filename = "test_data-10000d-1000r-10-a.txt"
        self.result_list_test(filename)

    def test_10_results_ginormous_good_internal_comparisons(self):
        filename = "test_data-10000d-1000r-10-a.txt"
        self.internal_comparisons_test(filename)


class SimpleBstStoreTests(BaseTester):
    def test_store_in_uninode_tree_v1(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene_to_add = Gene("aaa")
        value_to_add = "Crohn's disease"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene_to_add)
        self.assertEqual(bst.root.left.value, value_to_add)

    def test_store_in_uninode_tree_v2(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene_to_add = Gene("ttt")
        value_to_add = "Crohn's disease"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene_to_add)
        self.assertEqual(bst.root.right.value, value_to_add)

    def test_store_2_in_uninode_tree_v1(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1_to_add = Gene("cat")
        value1_to_add = "Crohn's disease"
        bst.insert(gene1_to_add, value1_to_add)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene1_to_add)
        self.assertEqual(bst.root.left.value, value1_to_add)

        gene2_to_add = Gene("tgt")
        value2_to_add = "PCT"
        bst.insert(gene2_to_add, value2_to_add)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene2_to_add)
        self.assertEqual(bst.root.right.value, value2_to_add)

    def test_store_2_in_uninode_tree_v1(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene_to_add = Gene("cat")
        value_to_add = "Crohn's disease"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene_to_add)
        self.assertEqual(bst.root.left.value, value_to_add)

        gene_to_add = Gene("tgt")
        value_to_add = "PCT"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene_to_add)
        self.assertEqual(bst.root.right.value, value_to_add)

    def test_store_2_in_uninode_tree_v2(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1 = Gene("cat")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)

        gene2 = Gene("aag")
        value2 = "PCT"
        bst.insert(gene2, value2)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)
        self.assertEqual(bst.root.left.left.key, gene2)
        self.assertEqual(bst.root.left.left.value, value2)

    def test_store_2_in_uninode_tree_v3(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1 = Gene("cat")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)

        gene2 = Gene("cct")
        value2 = "PCT"
        bst.insert(gene2, value2)
        self.assertEqual(bst.comparisons, 3)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)
        self.assertEqual(bst.root.left.right.key, gene2)
        self.assertEqual(bst.root.left.right.value, value2)

    def test_store_2_in_uninode_tree_v4(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1 = Gene("tct")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value1)

        gene2 = Gene("tgt")
        value2 = "PCT"
        bst.insert(gene2, value2)
        self.assertEqual(bst.comparisons, 4)
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value1)
        self.assertEqual(bst.root.right.right.key, gene2)
        self.assertEqual(bst.root.right.right.value, value2)

    def test_update_value_in_two_node_tree(self):
        # storing a new value for gene1 should mean that
        # the node is updated with the new value
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        value2 = "Stickler syndrome"
        bst.insert(gene1, value1)
        bst.insert(gene1, value2)
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value2)

    def test_update_value_in_two_node_tree_comps(self):
        # storing a new value for gene1 should mean that
        # the node is updated with the new value
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        value2 = "Stickler syndrome"
        bst.insert(gene1, value1)
        bst.insert(gene1, value2)
        self.assertEqual(bst.comparisons, 6)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value2)

    def test_store_in_uninode_tree_v1(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene_to_add = Gene("aaa")
        value_to_add = "Crohn's disease"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene_to_add)
        self.assertEqual(bst.root.left.value, value_to_add)

    def test_store_in_uninode_tree_v2(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene_to_add = Gene("ttt")
        value_to_add = "Crohn's disease"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene_to_add)
        self.assertEqual(bst.root.right.value, value_to_add)

    def test_store_2_in_uninode_tree_v1(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1_to_add = Gene("cat")
        value1_to_add = "Crohn's disease"
        bst.insert(gene1_to_add, value1_to_add)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene1_to_add)
        self.assertEqual(bst.root.left.value, value1_to_add)

        gene2_to_add = Gene("tgt")
        value2_to_add = "PCT"
        bst.insert(gene2_to_add, value2_to_add)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene2_to_add)
        self.assertEqual(bst.root.right.value, value2_to_add)

    def test_store_2_in_uninode_tree_v1(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene_to_add = Gene("cat")
        value_to_add = "Crohn's disease"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene_to_add)
        self.assertEqual(bst.root.left.value, value_to_add)

        bst.comparisons = 0  # Reset comparisons.
        gene_to_add = Gene("tgt")
        value_to_add = "PCT"
        bst.insert(gene_to_add, value_to_add)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene_to_add)
        self.assertEqual(bst.root.right.value, value_to_add)

    def test_store_2_in_uninode_tree_v2(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1 = Gene("cat")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)

        bst.comparisons = 0  # Reset comparisons.
        gene2 = Gene("aag")
        value2 = "PCT"
        bst.insert(gene2, value2)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)
        self.assertEqual(bst.root.left.left.key, gene2)
        self.assertEqual(bst.root.left.left.value, value2)

    def test_store_2_in_uninode_tree_v3(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1 = Gene("cat")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        self.assertEqual(bst.comparisons, 1)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)

        bst.comparisons = 0  # Reset comparisons.
        gene2 = Gene("cct")
        value2 = "PCT"
        bst.insert(gene2, value2)
        self.assertEqual(bst.comparisons, 3)
        self.assertEqual(bst.root.left.key, gene1)
        self.assertEqual(bst.root.left.value, value1)
        self.assertEqual(bst.root.left.right.key, gene2)
        self.assertEqual(bst.root.left.right.value, value2)

    def test_store_2_in_uninode_tree_v4(self):
        bst = GeneBst(root=GeneBstNode(Gene("ggt"), "Alkaptonuria"))
        gene1 = Gene("tct")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value1)

        bst.comparisons = 0  # Reset comparisons.
        gene2 = Gene("tgt")
        value2 = "PCT"
        bst.insert(gene2, value2)
        self.assertEqual(bst.comparisons, 4)
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value1)
        self.assertEqual(bst.root.right.right.key, gene2)
        self.assertEqual(bst.root.right.right.value, value2)

    def test_update_value_in_two_node_tree(self):
        # storing a new value for gene1 should mean that
        # the node is updated with the new value
        gene0 = Gene("ggt")
        value0 = 1234
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        value2 = "Stickler syndrome"
        bst.insert(gene1, value1)
        bst.insert(gene1, value2)
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value2)

    def test_update_value_in_two_node_tree_comps(self):
        # storing a new value for gene1 should mean that
        # the node is updated with the new value
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        value2 = "Stickler syndrome"
        bst.insert(gene1, value1)
        bst.insert(gene1, value2)
        self.assertEqual(bst.comparisons, 6)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(bst.root.right.key, gene1)
        self.assertEqual(bst.root.right.value, value2)


class SimpleGetValueTests(BaseTester):
    # Note: This testing assumes GeneBst.insert is working
    #       Errors in GeneBst.insert will causes errors here

    def test_get_value_in_uninode_tree_v1(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        value = bst[gene0]
        self.assertEqual(bst.comparisons, 2)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value0)

    def test_get_value_in_two_node_tree_v1(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("aag")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        StatCounter.reset_counts()
        bst.comparisons = 0

        value = bst[gene1]
        self.assertEqual(bst.comparisons, 3)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value1)

    def test_get_value_in_two_node_tree_v2(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        StatCounter.reset_counts()
        bst.comparisons = 0

        value = bst[gene1]
        self.assertEqual(bst.comparisons, 4)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value1)

    def test_get_value_in_3_node_trees(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("aag")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        gene2 = Gene("cat")
        value2 = "Bloom syndrome"
        bst.insert(gene2, value2)

        StatCounter.reset_counts()
        bst.comparisons = 0
        value = bst[gene2]
        self.assertEqual(bst.comparisons, 5)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value2)

        # try another variation of 3 node tree
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("cat")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        gene2 = Gene("aag")
        value2 = "Bloom syndrome"
        bst.insert(gene2, value2)

        StatCounter.reset_counts()
        bst.comparisons = 0
        value = bst[gene2]
        self.assertEqual(bst.comparisons, 4)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value2)

        # and another variation of 3 node tree
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tct")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        gene2 = Gene("tgt")
        value2 = "Bloom syndrome"
        bst.insert(gene2, value2)

        StatCounter.reset_counts()
        bst.comparisons = 0
        value = bst[gene2]
        self.assertEqual(bst.comparisons, 6)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value2)

        # and another variation of 3 node tree
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        gene2 = Gene("tct")
        value2 = "Bloom syndrome"
        bst.insert(gene2, value2)

        StatCounter.reset_counts()
        bst.comparisons = 0
        value = bst[gene2]
        self.assertEqual(bst.comparisons, 5)
        self.assertEqual(bst.comparisons, actual_count(COMPARISONS))
        self.assertEqual(value, value2)


class SimpleGeneBstNodeCountTests(BaseTester):
    def test_num_nodes_1(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        count = num_nodes_in_tree(bst.root)
        self.assertEqual(count, 1)

    def test_num_nodes_2(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("aag")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        size = num_nodes_in_tree(bst.root)
        self.assertEqual(size, 2)

        # and another 2 node tree
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        gene1 = Gene("tgt")
        value1 = "Crohn's disease"
        bst.insert(gene1, value1)
        size = num_nodes_in_tree(bst.root)
        self.assertEqual(size, 2)

    def test_num_nodes_10(self):
        # try with all nodes to right
        bst = GeneBst(root=GeneBstNode(0, 0))
        for i in range(1, 10):
            bst.insert(i, i)
            size = num_nodes_in_tree(bst.root)
            self.assertEqual(size, i + 1)
        # try with all nodes to left
        bst = GeneBst(root=GeneBstNode(10, 10))
        for i in range(9, 0, -1):
            bst.insert(i, i)
            size = num_nodes_in_tree(bst.root)
            self.assertEqual(size, 11 - i)

    def num_nodes_100(self):
        # try with all nodes to right
        bst = GeneBst(root=GeneBstNode(0, 0))
        for i in range(1, 100):
            bst.insert(i, i)
        size = num_nodes_in_tree(bst.root)
        self.assertEqual(size, 100)
        # try with all nodes to left
        bst = GeneBst(root=GeneBstNode(100, 100))
        for i in range(99, 0, -1):
            bst.insert(i, i)
        size = num_nodes_in_tree(bst.root)

        self.assertEqual(size, 100)

    def test_num_nodes_100_random(self):
        nums = list(range(100))
        random.shuffle(nums)
        bst = GeneBst(root=GeneBstNode(nums[0], 0))
        for i in range(1, 100):
            bst.insert(nums[i], i)
            size = num_nodes_in_tree(bst.root)
            self.assertEqual(size, i + 1)

    def test_num_nodes_1000_random(self):
        nums = list(range(1000))
        random.shuffle(nums)
        bst = GeneBst(root=GeneBstNode(nums[0], 0))
        for i in range(1, 1000):
            bst.insert(nums[i], i)
        size = num_nodes_in_tree(bst.root)
        self.assertEqual(size, 1000)


class SimpleBstDepthTests(BaseTester):
    def test_depth_1(self):
        gene0 = Gene("ggt")
        value0 = "Alkaptonuria"
        bst = GeneBst(root=GeneBstNode(gene0, value0))
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 0)

    def test_depth_10(self):
        # try with all nodes to right
        bst = GeneBst(root=GeneBstNode(0, 0))
        for i in range(1, 11):
            bst.insert(i, i)
            depth = bst_depth(bst.root)
            self.assertEqual(depth, i)
        # try with all nodes to left
        bst = GeneBst(root=GeneBstNode(11, 0))
        for i in range(10, 0, -1):
            bst.insert(i, i)
            depth = bst_depth(bst.root)
            self.assertEqual(depth, 11 - i)
        # try with 10 nodes to left and right
        for i in range(1, 11):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 10)

    def test_depth_zig_zag(self):
        # start with 5 to the right
        bst = GeneBst(root=GeneBstNode(0, 0))
        for i in range(100, 600, 100):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 5)
        # add 5 nodes to left of last node
        for i in range(490, 440, -10):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 10)
        # add 5 nodes to right of last node
        for i in range(440, 445, 1):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 15)

    def test_depth_medium(self):
        # start with 5 to the right
        bst = GeneBst(root=GeneBstNode(90, 0))
        for i in range(100, 600, 100):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 5)
        # add 5 nodes to left
        for i in range(80, 30, -10):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 5)
        # add 3 nodes to right of last node
        for i in range(600, 900, 100):
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 8)
        bst = GeneBst(root=GeneBstNode(50, 0))
        for i in [40, 30, 60, 45, 44, 59, 80, 58, 70, 90, 71]:
            bst.insert(i, i)
        depth = bst_depth(bst.root)
        self.assertEqual(depth, 4)



class SimpleBstInOrderTestFiles(BaseTester):
    def bst_in_order_test_small(self, test_filename):
        test_file_location = DATA_DIR + test_filename
        disease_info, _, _ = read_test_data(test_file_location)
        if disease_info:
            gene, disease = disease_info[0]
            bst = GeneBst(root=GeneBstNode(gene, disease))
            for gene, disease in disease_info[1:]:
                # print(gene)
                bst.insert(gene, disease)
            # expect a list with the records in order
            sorted_disease_info = sorted(disease_info, key=lambda x: x[0])
            expected_list = [(gene, disease)
                             for gene, disease in sorted_disease_info]
            StatCounter.reset_counts()
            student_answer_list = bst_in_order(bst.root)
            self.assertEqual(actual_count(COMPARISONS), 0)
            self.AssertListInOrder(student_answer_list)
            self.AssertListsEqual(student_answer_list, expected_list)

    def test_in_order_small_files(self):
        for filename in [
            "test_data-10d-2r-2-a.txt",
            "test_data-10g-2r-2-a.txt",
            "test_data-50d-50g-2-a.txt",
            "test_data-50d-50g-5-a.txt",
            "test_data-50d-50g-10-a.txt",
            "test_data-50g-50g-10-a.txt",
            "test_data-1000d-50r-1-a.txt",
            "test_data-10000d-5r-1-a.txt",
        ]:
            self.bst_in_order_test_small(filename)


# --------------------- Setup Tests for BSTs -----------------------------------
# -------------------------------------------------------------------------------


class BaseTestsBst(BaseTests):
    def setUp(self):
        super().setUp()
        self.function_to_test = self.run_disease_checker
        self.expected_comparisons_dict = BST_EXPECTED_COMPS


    def run_disease_checker(self, disease_information, patient):
        tree = GeneBst()
        diseases = []
        for gene, disease in disease_information:
            # self.assertEquals(entry, None)
            tree.insert(gene, disease)
        for gene in patient:
            disease = tree[gene]
            if disease is not None:
                diseases.append(disease)
        return (diseases, tree.comparisons)


class TrivialBstTests(BaseTestsBst, TrivialListTest):
    pass


class SmallBstTests(BaseTestsBst, SmallTests):
    pass


class MediumBstTests(BaseTestsBst, MediumTests):
    pass


class BigBstTests(BaseTestsBst, BigTests):
    pass


class HugeBstTests(BaseTestsBst, HugeTests):
    pass


class HugeSortedBstTests(BaseTestsBst, HugeSortedTests):
    pass


class GinormousBstTests(BaseTestsBst, GinormousTests):
    pass






def all_tests_suite():
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase
    # uncomment the following lines when you're
    # ready to run such tests

    # tests for BST functions/methods...
    suite.addTest(test_loader(SimpleBstStoreTests))
    # suite.addTest(test_loader(SimpleGetValueTests))
    # suite.addTest(test_loader(SimpleGeneBstNodeCountTests))
    # suite.addTest(test_loader(SimpleBstDepthTests))
    # suite.addTest(test_loader(SimpleBstInOrderTestFiles))

    # tests for BST on files...
    suite.addTest(test_loader(TrivialBstTests))
    # suite.addTest(test_loader(SmallBstTests))
    # suite.addTest(test_loader(MediumBstTests))
    # suite.addTest(test_loader(BigBstTests))
    # suite.addTest(test_loader(HugeBstTests))
    # suite.addTest(test_loader(HugeSortedBstTests))
    # suite.addTest(test_loader(GinormousBstTests))

    return suite




def main():
    """Makes a test suite and runs it. Will your code pass?"""
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)


if __name__ == "__main__":
    main()
