def fast_heapify(heap_list):
    # Calculate the last parent index to start the process.
    n = len(heap_list) - 1
    last_parent = n // 2

    # Start from the last parent and move up the list.
    for i in range(last_parent, 0, -1):
        _sift_down_min_2_heap(heap_list, i)

def _sift_down_min_2_heap(heap_list, index):
    """
    Sifts down the element at the given index to its proper position in a min-2-heap.
    """
    n = len(heap_list) - 1
    while index * 2 <= n:
        left_child = index * 2
        right_child = left_child + 1
        min_child = left_child

        # Find the minimum of the two children (if the right child exists and is smaller).
        if right_child <= n and heap_list[right_child] < heap_list[left_child]:
            min_child = right_child

        # Swap the element with the minimum child if necessary.
        if heap_list[index] > heap_list[min_child]:
            heap_list[index], heap_list[min_child] = heap_list[min_child], heap_list[index]
            index = min_child
        else:
            break

# Example usage:
heap_list = [46, 90, 6, 20, 58, 36, 72]
fast_heapify(heap_list)
print(heap_list[1:])