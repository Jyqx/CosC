"""
tests.py
A module of unit tests to verify your answers to the
genetic similarity functions.
"""

import signal
import time
import unittest
import math

from classes3 import Priority, Patient
from utilities import read_test_data, run_tests, DATA_DIR
from stats import StatCounter, COMPARISONS, IS_MARKING_MODE


from patient_queue import PatientQueueHeap


TEST_FILE_FORMAT = DATA_DIR + "test_data-{imports}-{enqueues}-{dequeues}.txt"
real_count = StatCounter.get_count



class HeapAssertions:
    def assertHeap(self, heap, bad_op, index=0):
        """AssertHeap is an O(n) check that the heap is valid."""
        child_indices = heap._child_indices(index)
        valid_child_indices = [i for i in child_indices if i < len(heap.data)]
        if not valid_child_indices:
            return  # No children, no worries!
        parent_value = heap.data[index]
        for i in valid_child_indices:
            child_value = heap.data[i]
            if child_value.priority > parent_value.priority:
                raise AssertionError(
                    "Bad heap invariant after '{}':"
                    "\n\tparent: {}\n\tchild: {}".format(
                        bad_op, parent_value, child_value
                    )
                )
            self.assertHeap(heap, bad_op, index=i)

    def assertIndices(self, heap):
        """AssertIndices checks that the index dictionary is correct!"""
        for name, index in heap.indices.items():
            if heap.data[index].name != name:
                raise AssertionError(
                    "Index is not pointing to the right place:"
                    "\n\tExpected {} at index {}, but found {}."
                    "".format(name, index, heap.data[index].name)
                )


class BaseTestPatientQueue(unittest.TestCase, HeapAssertions):
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


    def get_bounds(self, import_size, instructions, fast):
        lower_bound = 0
        upper_bound = 0
        if fast:
            lower_bound += import_size - 1
            upper_bound += 2 * import_size + 1
        else:
            # set O(n log n) importing bounds
            lower_bound += import_size - 1
            upper_bound += int(import_size * \
                               (math.log2(import_size + 1))) // 2 + 1
        if import_size < 2:
            lower_bound = 0
            upper_bound = 0
        queue_size = import_size
        op_deltas = {"enqueue": 1, "dequeue": -1, "remove": -1}
        op_factors = {"enqueue": 1, "dequeue": 1.2, "remove": 1.75}
        for operation, _ in instructions:
            # Update the bounds for an O(log n) operation
            should_count_comps = (operation == "enqueue" and queue_size > 0) or (
                operation == "dequeue" and queue_size > 1
            )
            if should_count_comps:
                lower_bound += int(math.log2(queue_size) / 4)
                upper_bound += (
                    int(op_factors[operation] * \
                        (math.log2(queue_size + 1))) + 1
                )

            queue_size += op_deltas[operation]
        return lower_bound, upper_bound

    def run_test_file_instructions(self, filename, priority_queue, fast):
        """Using the test data in the file described by 'filename', run tests on the
        'priority_queue' class given.
        """
        import_data, instructions = read_test_data(filename)
        queue = priority_queue(import_data, fast)
        StatCounter.lock()
        self.assertHeap(queue, ("fast-" if fast else "") + "heapify")
        StatCounter.unlock()
        for mode, data in instructions:
            if mode == "enqueue":
                queue.enqueue(data)
                StatCounter.lock()
                self.assertIn(
                    data,
                    queue.data,
                    msg=f"After enqueueing {data}, {data} was not found in your heap!",
                )
                StatCounter.unlock()
            elif mode == "dequeue":
                result = queue.dequeue()
                self.assertEqual(
                    data,
                    result.name,
                    msg=f"After dequeuing {data} was not returned, instead your function returned {result.name}!",
                )
            elif mode == "remove":
                queue.remove(data)
                StatCounter.lock()
                self.assertNotIn(data, queue.data)
                StatCounter.unlock()
            StatCounter.lock()
            self.assertHeap(queue, mode)
            StatCounter.unlock()
        return queue

    def heap_test(self, test_file_name):
        """Test that the heap correctly follows the instructions given in the test file."""
        self.run_test_file_instructions(test_file_name)

    def internal_comparisons_test(self, test_file_name):
        """Test that the student has correctly counted the code against what
        we have counted. This does not mean that the count is correct, just
        that it was correctly counted.
        """
        queue = self.run_test_file_instructions(test_file_name)
        student_comparisons = queue.comparisons
        true_comparisons = real_count(COMPARISONS)
        message_if_wrong = (
            f"Your code reported using {student_comparisons} Priority {COMPARISONS} "
        )
        message_if_wrong += f"but it actually used {true_comparisons}. "
        message_if_wrong += (
            f"This means you are miscounting Priority {COMPARISONS}, eg, "
        )
        message_if_wrong += (
            f"not counting Priority {COMPARISONS} when they are made or "
        )
        message_if_wrong += f"counting Priority {COMPARISONS} that weren't made."
        self.assertEqual(student_comparisons,
                         true_comparisons, msg=message_if_wrong)


    def comparisons_test(self, test_file_name):
        """Test that the number of comparisons that the student made is
        within the expected bounds (provided by self.get_bounds)
        """
        lower_bound, upper_bound = self.get_bounds(
            *read_test_data(test_file_name))
        queue = self.run_test_file_instructions(test_file_name)
        student_comparisons = queue.comparisons
        # self.assertIn(queue.comparisons, valid_count_range)
        message_if_wrong = (
            f"Your code reported using {student_comparisons} Priority comparisons "
        )
        message_if_wrong += (
            f"but it should use {lower_bound} <= comparisons <= {upper_bound}."
        )

        self.assertTrue(
            lower_bound <= student_comparisons <= upper_bound, msg=message_if_wrong
        )

    def both_comparisons_test(self, test_file_name):
        """Test that the number of comparisons that the student made is
        within the expected bounds (provided by self.get_bounds) AND that they counted
        their comparisons correctly.
        """
        lower_bound, upper_bound = self.get_bounds(
            *read_test_data(test_file_name))
        queue = self.run_test_file_instructions(test_file_name)
        student_comparisons = queue.comparisons
        # self.assertIn(queue.comparisons, valid_count_range)
        message_if_wrong = (
            f"Your code reported using {student_comparisons} Priority comparisons "
        )
        message_if_wrong += (
            f"but it should use {lower_bound} <= comparisons <= {upper_bound}."
        )

        self.assertTrue(
            lower_bound <= student_comparisons <= upper_bound, msg=message_if_wrong
        )

        true_comparisons = real_count(COMPARISONS)
        message_if_wrong = (
            f"Your code reported using {student_comparisons} Priority {COMPARISONS} "
        )
        message_if_wrong += f"but it actually used {true_comparisons}. "
        message_if_wrong += (
            f"This means you are miscounting Priority {COMPARISONS}, eg, "
        )
        message_if_wrong += (
            f"not counting Priority {COMPARISONS} when they are made or "
        )
        message_if_wrong += f"counting Priority {COMPARISONS} that weren't made."
        self.assertEqual(student_comparisons,
                         true_comparisons, msg=message_if_wrong)

    def all_test(self, test_file_name):
        """Test that the number of comparisons that the student made is
        within the expected bounds (provided by self.get_bounds) AND that they counted
        their comparisons correctly AND result is correct.
        """
        self.both_comparisons_test(test_file_name)


class TestPatientQueueEnqueueTiny(BaseTestPatientQueue):
    """Unit tests for enqueueing (which tests sift_up)"""

    def test_tiny_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=1, dequeues=0)
        self.heap_test(test_file)

    def test_tiny_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=1, dequeues=0)
        self.internal_comparisons_test(test_file)

    def test_tiny_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=1, dequeues=0)
        self.comparisons_test(test_file)


class TestPatientQueueEnqueueSmall(BaseTestPatientQueue):
    """Unit tests for enqueueing (which tests sift_up)"""

    def test_small_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=5, dequeues=0)
        self.heap_test(test_file)

    def test_small_enqueue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=5, dequeues=0)
        self.internal_comparisons_test(test_file)

    def test_small_enqueue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=5, dequeues=0)
        self.comparisons_test(test_file)


class TestPatientQueueEnqueue(BaseTestPatientQueue):
    """Unit tests for enqueueing (which tests sift_up)"""

    def test_medium_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=75, dequeues=0)
        self.heap_test(test_file)

    def test_medium_enqueue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=0, enqueues=75, dequeues=0)
        self.both_comparisons_test(test_file)

    def test_medium_enqueue_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0)
        self.heap_test(test_file)

    def test_medium_enqueue_both_comparisons_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=0)
        self.both_comparisons_test(test_file)

    def test_large_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=100, dequeues=0)
        self.heap_test(test_file)

    def test_large_enqueue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=100, dequeues=0)
        self.both_comparisons_test(test_file)

    def test_large_enqueue_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0)
        self.heap_test(test_file)

    def test_large_enqueue_both_comparisons_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=0)
        self.both_comparisons_test(test_file)

    def test_larger_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=250, dequeues=0)
        self.heap_test(test_file)

    def test_larger_enqueue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=0, enqueues=250, dequeues=0)
        self.both_comparisons_test(test_file)

    def test_larger_enqueue_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=250, enqueues=250, dequeues=0)
        self.heap_test(test_file)

    def test_larger_enqueue_both_comparisons_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=250, enqueues=250, dequeues=0)
        self.both_comparisons_test(test_file)


class TestPatientQueueEnqueueHuge(BaseTestPatientQueue):
    """Unit tests for enqueueing (which tests sift_up)"""

    def test_huge_enqueue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0)
        self.heap_test(test_file)

    def test_huge_enqueue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=0)
        self.both_comparisons_test(test_file)


class TestPatientQueueDequeueTiny(BaseTestPatientQueue):
    """Unit tests for dequeueing (which tests sift_down)
    This dataset actually tests both up and down, because you need
    to be able to enqueue to have stuff to dequeue!
    """

    def test_tiny_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(imports=1, enqueues=0, dequeues=1)
        self.heap_test(test_file)

    def test_tiny_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=1, enqueues=0, dequeues=1)
        self.internal_comparisons_test(test_file)

    def test_tiny_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(imports=1, enqueues=0, dequeues=1)
        self.comparisons_test(test_file)


class TestPatientQueueDequeueSmall(BaseTestPatientQueue):
    """Unit tests for dequeueing (which tests sift_down)
    This dataset actually tests both up and down, because you need
    to be able to enqueue to have stuff to dequeue!
    """

    def test_small_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20)
        self.heap_test(test_file)

    def test_small_dequeue_internal_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20)
        self.internal_comparisons_test(test_file)

    def test_small_dequeue_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=10, enqueues=10, dequeues=20)
        self.comparisons_test(test_file)


class TestPatientQueueDequeue(BaseTestPatientQueue):
    """Unit tests for dequeueing (which tests sift_down)
    This dataset actually tests both up and down, because you need
    to be able to enqueue to have stuff to dequeue!
    """

    def test_medium_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75)
        self.heap_test(test_file)

    def test_medium_dequeue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=25, dequeues=75)
        self.both_comparisons_test(test_file)

    def test_medium_dequeue_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=50, dequeues=100)
        self.heap_test(test_file)

    def test_medium_dequeue_both_comparisons_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=50, enqueues=50, dequeues=100)
        self.both_comparisons_test(test_file)

    def test_large_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150)
        self.heap_test(test_file)

    def test_large_dequeue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=150)
        self.both_comparisons_test(test_file)

    def test_large_dequeue_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=200)
        self.heap_test(test_file)

    def test_large_dequeue_both_comparisons_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=100, enqueues=100, dequeues=200)
        self.both_comparisons_test(test_file)

    def test_larger_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=500, enqueues=0, dequeues=10)
        self.heap_test(test_file)

    def test_larger_dequeue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=500, enqueues=0, dequeues=10)
        self.both_comparisons_test(test_file)


class TestPatientQueueDequeueHuge(BaseTestPatientQueue):
    """Unit tests for dequeueing (which tests sift_down)
    This dataset actually tests both up and down, because you need
    to be able to enqueue to have stuff to dequeue!
    """

    def test_huge_dequeue(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500)
        self.heap_test(test_file)

    def test_huge_dequeue_both_comparisons(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=1000, dequeues=1500)
        self.both_comparisons_test(test_file)


class TestPatientQueueFastHeapify(BaseTestPatientQueue):
    """Unit tests for _fast_heapify. These check the comparisons more tightly, that
    the comparisons were correctly counted, and that the result is correct.
    """

    def test_medium_fast_heapify_all(self):
        test_file = TEST_FILE_FORMAT.format(imports=50, enqueues=0, dequeues=0)
        self.all_test(test_file)

    def test_medium_fast_heapify_all_2(self):
        test_file = TEST_FILE_FORMAT.format(imports=50, enqueues=0, dequeues=0)
        self.all_test(test_file)

    def test_large_fast_heapify_all(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=250, enqueues=0, dequeues=0)
        self.all_test(test_file)

    def test_larger_fast_heapify_all_2(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=500, enqueues=0, dequeues=0)
        self.all_test(test_file)

    def test_huge_fast_heapify_all(self):
        test_file = TEST_FILE_FORMAT.format(
            imports=1000, enqueues=0, dequeues=0)
        self.all_test(test_file)




class TestTaskOne(
    TestPatientQueueEnqueueTiny,
    TestPatientQueueEnqueueSmall,
    TestPatientQueueEnqueue,
    TestPatientQueueEnqueueHuge,
):
    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=False)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(
            filename, PatientQueueHeap, fast=False
        )


class TestTaskTwo(
    TestPatientQueueDequeueTiny,
    TestPatientQueueDequeueSmall,
    TestPatientQueueDequeue,
    TestPatientQueueDequeueHuge,
):
    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=False)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(
            filename, PatientQueueHeap, fast=False
        )


class TestTaskThree(
    TestPatientQueueDequeueTiny,
    TestPatientQueueFastHeapify,
):
    """Uses Dequeue test files with fast heap building."""

    def get_bounds(self, imports, instructions):
        return super().get_bounds(len(imports), instructions, fast=True)

    def run_test_file_instructions(self, filename):
        return super().run_test_file_instructions(filename, PatientQueueHeap, fast=True)




def all_tests_suite():
    """Combines test cases from various classes to make a
    big suite of tests to run.
    You can comment out tests you don't want to run and uncomment
    tests that you do want to run :)
    """
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase

    suite.addTest(test_loader(TestTaskOne))

    # uncomment the following lines when ready to test further tasks
    # suite.addTest(test_loader(TestTaskTwo))
    # suite.addTest(test_loader(TestTaskThree))
    return suite




def main():
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()


    test_runner.run(all_tests)


if __name__ == "__main__":
    main()
