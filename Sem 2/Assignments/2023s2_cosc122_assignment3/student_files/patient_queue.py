"""
File = patient_queue.py
Author = Luke Donaldson-Scott

Maintain a patient queue that sorts patients based on the diseases
they have been diagnosed with, and the time since the diagnosis.
"""

from classes3 import PriorityQueue, Patient


class PatientQueueHeap(PriorityQueue):
    """Implement a queue structure using a 0-indexed Heap.
    This particular type of queue is designed to hold patient information.
    """

    def __init__(self, start_data=None, fast=False):
        """Creates the patient queue."""
        if start_data is None:
            start_data = []
        self.comparisons = 0
        self.data = []
        if fast:
            self._fast_heapify(start_data)
        else:
            self._heapify(start_data)

    def _swap(self, i, j):
        """Swap the patients at positions i and j."""
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _parent_index(self, index):
        """Determine the parent index of the current index.
        For a binary heap that is zero-indexed, this is
        p = (i - 1) // 2
        """
        return (index - 1) // 2

    def _child_indices(self, index):
        """Calculate the child indices for the current index.
        For a binary heap that is zero-indexed, this is
        c1 = 2*i + 1
        c2 = 2*i + 2
        """
        return [2 * index + delta for delta in range(1, 2 + 1)]

    def _max_child_priority_index(self, child_indices):
        """Find the child among the given indices that has the highest priority.
        If an index is not valid, do not consider it. If none are valid, then
        return None. Assumes the child_indices are in order.
        """
        max_index = None
        for index in child_indices:
            if index >= len(self.data):
                break  # No more valid children
            if max_index is None:  # This is the first child, it's valid, so use it
                max_index = index
            else:
                self.comparisons += 1  # Don't worry, we do the comparison counting here
                if self.data[index].priority > self.data[max_index].priority:
                    max_index = index
        return max_index

    def _sift_up(self, index):
        """Move the patient at the given index into the correct location
        further up in the heap by swapping with its parents if appropriate.
        """
        # ---start student section---
        while index > 0:
            parent_index = self._parent_index(index)
            if self.data[index].priority > self.data[parent_index].priority:
                self._swap(index, parent_index)
                index = parent_index
                self.comparisons += 1  # Increment comparisons for the comparison made
            else:
                break
        # ===end student section===

    def _sift_down(self, index):
        """Move the patient at the given index into the correct location
        further down in the heap by swapping with its children if appropriate.
        """
        # ---start student section---
        while True:
            child_indices = self._child_indices(index)
            max_child_index = self._max_child_priority_index(child_indices)

            if max_child_index is None:
                break

            if self.data[index].priority < self.data[max_child_index].priority:
                self._swap(index, max_child_index)
                index = max_child_index
                self.comparisons += 1  # Increment comparisons for the comparison made
            else:
                break
        # ===end student section===

    def _heapify(self, data):
        """Turn the existing data into a heap in O(n log n) time."""
        for patient in data:
            self.enqueue(patient)

    def _fast_heapify(self, data):
        """Turn the existing data into a heap in O(n) time.
        """
        # ---start student section---
        last_non_leaf = len(data) // 2 - 1
        self.data = data

        for i in range(last_non_leaf, -1, -1):
            self._sift_down(i)
        # ===end student section===

    def enqueue(self, patient):
        """Add a patient to the queue.
        """
        # We first make sure that we're only including Patients
        assert isinstance(patient, Patient)
        # ---start student section---
        self.data.append(patient)  # Add the patient to the end of the list
        self._sift_up(len(self.data) - 1)  # Sift the newly added patient up to its correct position
        # ===end student section===

    def dequeue(self):
        """Take a patient off the queue and return the Patient object.
        """
        # ---start student section---
        if not self.data:
            return None  # Return None if the queue is empty
        elif len(self.data) == 1:
            return self.data.pop()  # Return the only patient if there's only one

        # Swap the first and last elements (highest priority with last)
        self._swap(0, len(self.data) - 1)
        # Remove and return the last patient (the one with the highest priority)
        patient = self.data.pop()
        # Sift down the new root to maintain the heap property
        self._sift_down(0)
        
        return patient
        # ===end student section===




if __name__ == "__main__":
    # put your own simple tests here
    # you don't need to submit this code
    print("Add some tests here...")
