"""
tests.py
A module of unit tests to verify your answers to the
genetic similarity functions.
"""

import os
import shutil
import time
import unittest
import math
import signal

import utilities
from classes import Gene, Genome, GeneList
from stats import StatCounter, IS_MARKING_MODE

from sequential_gene_match import sequential_gene_match
from binary_gene_match import binary_gene_match

TEST_FOLDER = './test_data/'
TEST_FILE_TEMPLATE = "test_data/test_data-{size}-{common}{sort}.txt"


real_count = StatCounter.get_count


class TypeAssertion(object):

    def assertTypesEqual(self, a, b, msg=''):
        if type(a) != type(b):
            if not msg:
                template = "Type {} does not match type {}"
                error_msg = template.format(type(a), type(b))
            else:
                error_msg = msg
            raise AssertionError(error_msg)


class BaseTestCommonGenes(unittest.TestCase, TypeAssertion):

    def setUp(self):
        """Runs before every test case"""
        StatCounter.reset_counts()
        self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = (self.end_time - self.start_time)
        print(f'{test_time:.4f}s', end=' ')

    def get_bounds(self, left_length, right_length):
        raise NotImplementedError("This method should be "
                                  "implemented by a subclass.")

    def common_genes_test(self, test_file_name,
                          genetic_similarity_function):
        """ Test that the given genetic_similarity_function returns the correct
            result for the file specified by test_file_name.
        """
        (first_genome,
         second_genome,
         true_answer) = utilities.read_test_data(test_file_name)

        student_answer, _ = genetic_similarity_function(first_genome,
                                                        second_genome)
        message_if_wrong = f"Your answer list doesn't match the expected answer list. "
        message_if_wrong += f"Note: Your list is the first list and the expected is the second."
        self.assertEqual(student_answer, true_answer, message_if_wrong)
        message_if_wrong = f"Your answer list isn't the same type as the expected list!"
        self.assertTypesEqual(student_answer, true_answer, message_if_wrong)

    def internal_comparisons_test(self, test_file_name,
                                  genetic_similarity_function):
        """ Test that the student has correctly counted the code against what
            we have counted. This does not mean that the count is correct, just
            that it was correctly counted.
        """
        (first_genome,
         second_genome, _) = utilities.read_test_data(test_file_name)

        _, student_count = genetic_similarity_function(first_genome,
                                                       second_genome)
        actual_count = real_count('comparisons')
        message_if_wrong = f'Your code reported using {student_count} Gene comparisons '
        message_if_wrong += f'but it actually used {actual_count}. '
        message_if_wrong += f'This means you are miscounting Gene comparisons, eg, '
        message_if_wrong += f'not counting Gene comparisons when they are made or '
        message_if_wrong += f"counting Gene comparisons that weren't made."
        self.assertEqual(student_count, actual_count, msg=message_if_wrong)

    def comparisons_test(self, test_file_name, genetic_similarity_function,
                         target=None):
        """ Test that the number of comparisons that the student made is
            within the expected bounds (provided by self.get_bounds, or target)
        """
        (first_genome,
         second_genome, _) = utilities.read_test_data(test_file_name)
        if target is None:
            lower_bound, upper_bound = self.get_bounds(len(first_genome),
                                                       len(second_genome))

        _, student_count = genetic_similarity_function(first_genome,
                                                       second_genome)
        if target is not None:
            message_if_wrong = f'Your code reported using {student_count} Gene comparisons '
            message_if_wrong += f'but it should have used {target} comparisons.'
            self.assertEqual(student_count, target, message_if_wrong)
        else:
            valid_count_range = range(lower_bound, upper_bound + 1)
            message_if_wrong = f'Your code reported using {student_count} Gene comparisons '
            message_if_wrong += f'but it should use {lower_bound} <= comparisons < {upper_bound+1}.'
            self.assertIn(student_count, valid_count_range, message_if_wrong)


class TestCommonGenesSequential(BaseTestCommonGenes):
    """ Unit tests for the sequential common gene finder.
    """

    def get_filename(self, size, common):
        return TEST_FILE_TEMPLATE.format(size=size, common=common, sort='')

    def get_bounds(self, m, n):
        return m, m * n

    def common_genes_test(self, test_file_name):
        super().common_genes_test(test_file_name,
                                  sequential_gene_match)

    def internal_comparisons_test(self, test_file_name):
        super().internal_comparisons_test(test_file_name,
                                          sequential_gene_match)

    def comparisons_test(self, test_file_name, expected=None):
        super().comparisons_test(test_file_name,
                                 sequential_gene_match,
                                 expected)


class TestCommonGenesBinary(BaseTestCommonGenes):
    """ Unit tests for the sequential common gene finder.
    """

    def get_filename(self, size, common):
        return TEST_FILE_TEMPLATE.format(size=size, common=common, sort='-s')

    def get_bounds(self, m, n):
        logn = int(math.log(n, 2))
        lower = m * (logn + 1) - 2
        upper = m * (logn + 2) + 2
        return lower, upper

    def common_genes_test(self, test_file_name):
        super().common_genes_test(test_file_name, binary_gene_match)

    def internal_comparisons_test(self, test_file_name):
        super().internal_comparisons_test(test_file_name,
                                          binary_gene_match)

    def comparisons_test(self, test_file_name, expected=None):
        super().comparisons_test(test_file_name,
                                 binary_gene_match,
                                 expected)




class TinyTests(BaseTestCommonGenes):

    def test_tiny(self):
        test_file = self.get_filename(size=2, common=1)
        self.common_genes_test(test_file)

    def test_tiny_internal_comparisons(self):
        test_file = self.get_filename(size=2, common=1)
        self.internal_comparisons_test(test_file)

    def test_tiny_comparisons(self):
        test_file = self.get_filename(size=2, common=1)
        self.comparisons_test(test_file)


class SmallTests(BaseTestCommonGenes):

    def test_small_none_common(self):
        test_file = self.get_filename(size=10, common=0)
        self.common_genes_test(test_file)

    def test_small_none_common_internal_comparisons(self):
        test_file = self.get_filename(size=10, common=0)
        self.internal_comparisons_test(test_file)

    def test_small_none_common_comparisons(self):
        test_file = self.get_filename(size=10, common=0)
        self.comparisons_test(test_file)

    def test_small_some_common(self):
        test_file = self.get_filename(size=10, common=3)
        self.common_genes_test(test_file)

    def test_small_some_common_internal_comparisons(self):
        test_file = self.get_filename(size=10, common=3)
        self.internal_comparisons_test(test_file)

    def test_small_some_common_comparisons(self):
        test_file = self.get_filename(size=10, common=3)
        self.comparisons_test(test_file)

    def test_small_all_common(self):
        test_file = self.get_filename(size=10, common=10)
        self.common_genes_test(test_file)

    def test_small_all_common_internal_comparisons(self):
        test_file = self.get_filename(size=10, common=10)
        self.internal_comparisons_test(test_file)

    def test_small_all_common_comparisons(self):
        test_file = self.get_filename(size=10, common=10)
        self.comparisons_test(test_file)


class LargeTests(BaseTestCommonGenes):

    def test_large_none_common(self):
        test_file = self.get_filename(size=1000, common=0)
        self.common_genes_test(test_file)

    def test_large_none_common_internal_comparisons(self):
        test_file = self.get_filename(size=1000, common=0)
        self.internal_comparisons_test(test_file)

    def test_large_none_common_comparisons(self):
        test_file = self.get_filename(size=1000, common=0)
        self.comparisons_test(test_file)

    def test_large_some_common(self):
        test_file = self.get_filename(size=1000, common=250)
        self.common_genes_test(test_file)

    def test_large_some_common_internal_comparisons(self):
        test_file = self.get_filename(size=1000, common=250)
        self.internal_comparisons_test(test_file)

    def test_large_some_common_comparisons(self):
        test_file = self.get_filename(size=1000, common=250)
        self.comparisons_test(test_file)

    def test_large_all_common(self):
        test_file = self.get_filename(size=1000, common=1000)
        self.common_genes_test(test_file)

    def test_large_all_common_internal_comparisons(self):
        test_file = self.get_filename(size=1000, common=1000)
        self.internal_comparisons_test(test_file)

    def test_large_all_common_comparisons(self):
        test_file = self.get_filename(size=1000, common=1000)
        self.comparisons_test(test_file)


class LargerTests(BaseTestCommonGenes):

    def test_larger_none_common(self):
        test_file = self.get_filename(size=5000, common=0)
        self.common_genes_test(test_file)

    def test_larger_none_common_internal_comparisons(self):
        test_file = self.get_filename(size=5000, common=0)
        self.internal_comparisons_test(test_file)

    def test_larger_none_common_comparisons(self):
        test_file = self.get_filename(size=5000, common=0)
        self.comparisons_test(test_file)

    def test_larger_some_common(self):
        test_file = self.get_filename(size=5000, common=2500)
        self.common_genes_test(test_file)

    def test_larger_some_common_internal_comparisons(self):
        test_file = self.get_filename(size=5000, common=2500)
        self.internal_comparisons_test(test_file)

    def test_larger_some_common_comparisons(self):
        test_file = self.get_filename(size=5000, common=2500)
        self.comparisons_test(test_file)

    def test_larger_all_common(self):
        test_file = self.get_filename(size=5000, common=5000)
        self.common_genes_test(test_file)

    def test_larger_all_common_internal_comparisons(self):
        test_file = self.get_filename(size=5000, common=5000)
        self.internal_comparisons_test(test_file)

    def test_larger_all_common_comparisons(self):
        test_file = self.get_filename(size=5000, common=5000)
        self.comparisons_test(test_file)


class LargestTests(BaseTestCommonGenes):

    def test_largest_none_common(self):
        test_file = self.get_filename(size=10000, common=0)
        self.common_genes_test(test_file)

    def test_largest_none_common_internal_comparisons(self):
        test_file = self.get_filename(size=10000, common=0)
        self.internal_comparisons_test(test_file)

    def test_largest_none_common_comparisons(self):
        test_file = self.get_filename(size=10000, common=0)
        self.comparisons_test(test_file)

    def test_largest_some_common(self):
        test_file = self.get_filename(size=10000, common=5000)
        self.common_genes_test(test_file)

    def test_largest_some_common_internal_comparisons(self):
        test_file = self.get_filename(size=10000, common=5000)
        self.internal_comparisons_test(test_file)

    def test_largest_some_common_comparisons(self):
        test_file = self.get_filename(size=10000, common=5000)
        self.comparisons_test(test_file)

    def test_largest_all_common(self):
        test_file = self.get_filename(size=10000, common=10000)
        self.common_genes_test(test_file)

    def test_largest_all_common_internal_comparisons(self):
        test_file = self.get_filename(size=10000, common=10000)
        self.internal_comparisons_test(test_file)

    def test_largest_all_common_comparisons(self):
        test_file = self.get_filename(size=10000, common=10000)
        self.comparisons_test(test_file)


class HugeTests(BaseTestCommonGenes):

    def test_huge_none_common(self):
        test_file = self.get_filename(size=100000, common=0)
        self.common_genes_test(test_file)

    def test_huge_none_common_internal_comparisons(self):
        test_file = self.get_filename(size=100000, common=0)
        self.internal_comparisons_test(test_file)

    def test_huge_none_common_comparisons(self):
        test_file = self.get_filename(size=100000, common=0)
        self.comparisons_test(test_file)

    def test_huge_some_common(self):
        test_file = self.get_filename(size=100000, common=50000)
        self.common_genes_test(test_file)

    def test_huge_some_common_internal_comparisons(self):
        test_file = self.get_filename(size=100000, common=50000)
        self.internal_comparisons_test(test_file)

    def test_huge_some_common_comparisons(self):
        test_file = self.get_filename(size=100000, common=50000)
        self.comparisons_test(test_file)

    def test_huge_all_common(self):
        test_file = self.get_filename(size=100000, common=100000)
        self.common_genes_test(test_file)

    def test_huge_all_common_internal_comparisons(self):
        test_file = self.get_filename(size=100000, common=100000)
        self.internal_comparisons_test(test_file)

    def test_huge_all_common_comparisons(self):
        test_file = self.get_filename(size=100000, common=100000)
        self.comparisons_test(test_file)




class SequentialExact(BaseTestCommonGenes):

    # Here we do some extra tests with known values

    def test_tiny_comparisons_exact(self):
        test_file = self.get_filename(size=2, common=1)
        self.comparisons_test(test_file, 4)

    def test_small_none_common_comparisons_exact(self):
        test_file = self.get_filename(size=10, common=0)
        self.comparisons_test(test_file, 100)

    def test_small_some_common_comparisons_exact(self):
        test_file = self.get_filename(size=10, common=3)
        self.comparisons_test(test_file, 85)

    def test_small_all_common_comparisons_exact(self):
        test_file = self.get_filename(size=10, common=10)
        self.comparisons_test(test_file, 55)

    def test_large_none_common_comparisons_exact(self):
        test_file = self.get_filename(size=1000, common=0)
        self.comparisons_test(test_file, 1000000)

    def test_large_some_common_comparisons_exact(self):
        test_file = self.get_filename(size=1000, common=250)
        self.comparisons_test(test_file, 872420)

    def test_large_all_common_comparisons_exact(self):
        test_file = self.get_filename(size=1000, common=1000)
        self.comparisons_test(test_file, 500500)


# All the sequential tests
class TinyTestsSequential(TestCommonGenesSequential, TinyTests):
    pass


class SmallTestsSequential(TestCommonGenesSequential, SmallTests):
    pass


class LargeTestsSequential(TestCommonGenesSequential, LargeTests):
    pass


class LargerTestsSequential(TestCommonGenesSequential, LargerTests):
    pass


class LargestTestsSequential(TestCommonGenesSequential, LargestTests):
    pass


class HugeTestsSequential(TestCommonGenesSequential, HugeTests):
    pass


class ExactTestsSequential(TestCommonGenesSequential, SequentialExact):
    pass


# All the binary tests
class TinyTestsBinary(TestCommonGenesBinary, TinyTests):
    pass


class SmallTestsBinary(TestCommonGenesBinary, SmallTests):
    pass


class LargeTestsBinary(TestCommonGenesBinary, LargeTests):
    pass


class LargerTestsBinary(TestCommonGenesBinary, LargerTests):
    pass


class LargestTestsBinary(TestCommonGenesBinary, LargestTests):
    pass


class HugeTestsBinary(TestCommonGenesBinary, HugeTests):
    pass




def all_tests_suite():
    """ Combines test cases from various classes to make a
    big suite of tests to run.
    You can comment out tests you don't want to run and uncomment
    tests that you do want to run :)
    """
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase

    suite.addTest(test_loader(TinyTestsSequential))
    suite.addTest(test_loader(SmallTestsSequential))
    suite.addTest(test_loader(LargeTestsSequential))
    suite.addTest(test_loader(LargerTestsSequential))
    # suite.addTest(test_loader(LargestTestsSequential)) # Based on the shorter tests time,
    # suite.addTest(test_loader(HugeTestsSequential))    # how long will these tests take?
    suite.addTest(test_loader(ExactTestsSequential))

    # uncomment the next line when ready for binary testing
    # suite.addTest(test_loader(TinyTestsBinary))
    # suite.addTest(test_loader(SmallTestsBinary))
    # suite.addTest(test_loader(LargeTestsBinary))
    # suite.addTest(test_loader(LargerTestsBinary))
    # suite.addTest(test_loader(LargestTestsBinary))
    # suite.addTest(test_loader(HugeTestsBinary))
    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)



if __name__ == '__main__':
    main()
