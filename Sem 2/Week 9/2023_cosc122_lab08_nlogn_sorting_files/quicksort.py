import time
import random
import doctest

# funky styles
LEFT_PIVOT = 'left-pivot'
MO3_PIVOT = 'mo3-pivot'


def read_data(filename):
    """ Returns a list of integers read from the file """
    with open(filename) as infile:
        values = [int(line.strip()) for line in infile]
    return values


def quicksort(values, style=LEFT_PIVOT):
    """Starts the quicksort algorithm for sorting a list of values in-place.
    By default, uses the left most value as the first pivot value.
    >>> quicksort([1, 4, 10, 8, 2, 6, 7, 0, 5, 9, 3])
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """

    copy_of_list = list(values)

    if len(copy_of_list) == 1:
        # return the copy of the 1 item list
        return copy_of_list
    else:
        # Quicksort the copy of the list
        quicksort_helper(copy_of_list, 0, len(copy_of_list) - 1, style)
        return copy_of_list


def quicksort_helper(values, left, right, style):
    """
    Recursive quicksort helper.
    Sorts, in place, the portion of values between left and right.
    """

    # Stop when the left and right indices cross
    if left >= right:
        return
    # Partition the list
    split = partition(values, left, right, style)
    # Sort the left part
    quicksort_helper(values, left, split - 1, style)
    # Sort the right part
    quicksort_helper(values, split + 1, right, style)


def partition(values, left, right, style):
    """
    Partitions the values between left and right (inclusive).
    Returns the index of the split.
    if style='left-pivot' then left item used as pivot
    if sytle='mo3-pivot' then index of median of three
     used as pivot
    if sytle is unknown then left-pivot is used.

    """

    # Figure out which index to use as the pivot
    if style == LEFT_PIVOT:
        pivot_i = left
    elif style == MO3_PIVOT:
        pivot_i = pivot_index_mo3(values, left, right)
    else:
        print('I am unfamiliar with your funky styles.')
        print('Default left-pivot used...')
        pivot_i = left

    # Swap the pivot with the left item so we can keep the pivot
    # out of the way
    values[left], values[pivot_i] = values[pivot_i], values[left]

    # the pivot value is now the value in the left slot
    pivot = values[left]
    # move leftmark to first item after the pivot
    leftmark = left + 1
    rightmark = right
    # Move the left and right marks
    while True:
        # Find an item larger or equal to the pivot
        while leftmark <= rightmark and values[leftmark] < pivot:
            leftmark += 1
        # Find an item smaller than the pivot
        while leftmark <= rightmark and values[rightmark] >= pivot:
            rightmark -= 1

        # If the pointers cross, we're done
        if leftmark > rightmark:
            break
        else:
            # Otherwise... swap the items and keep going
            values[leftmark], values[rightmark] = values[
                rightmark], values[leftmark]

    # Put the pivot in its correct place
    if left != right:  # no point swapping with itself
        values[left], values[rightmark] = values[rightmark], values[left]

    # Return the location of the split
    # values to right of rightmark are >= pivot value
    # values to left of rightmark are < pivot value
    return rightmark


def quicksort_range(values, start, end, style='left-pivot'):
    """Starts a quicksort that only guarantees that values between
       the start and end index (inclusive) are sorted.
       start and end must valid non-negative inices into values
       end must be >= start
    >>> x = quicksort_range([2, 10, 5, 1, 0, 8, 3, 6, 9, 4, 7], 0, 1)
    >>> x[0]
    0
    >>> x[1]
    1
    >>> print(x)
    [0, 1, 2, 5, 10, 8, 3, 6, 9, 4, 7]
    >>> x = quicksort_range([5, 4, 10, 8, 2, 6, 7, 0, 1, 9, 3], 8, 10)
    >>> x[8:11]
    [8, 9, 10]
    >>> print(x)
    [0, 4, 3, 1, 2, 5, 6, 7, 8, 9, 10]
    >>> x = quicksort_range([2, 10, 5, 1, 0, 8, 3, 6, 9, 4, 7], 2, 3)
    >>> x[2]
    2
    >>> x[3]
    3
    >>> quicksort_range([2, 10, 5, 1, 0, 8, 3, 6, 9, 4, 7], 0, 10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    # check function has been called with sensible start and end
    if start < 0 or end < 0 or end >= len(values):
        raise IndexError(
            'start and end must be valid non-negative indices into values')
    if end < start:
        raise IndexError('The end should come after the start!')

    copy_of_list = list(values)
    if len(copy_of_list) == 1:
        # return the copy of the only item in list
        return copy_of_list
    else:
        # Quicksort the copy of the list
        quicksort_range_helper(copy_of_list,
                               0,
                               len(copy_of_list) - 1,
                               start,
                               end,
                               style)
        return copy_of_list


def quicksort_range_helper(values, left, right, start, end, style):
    """
    Recursive quicksort range helper.
    Sorts, in place, the portion of values between left and right (inclusive)
    but only if the left-right range has any overlap with the start-end range.
    """
    # ---start student section---
    if right < start or left > end:
        return  # No overlap, nothing to sort
    
    # Choose a pivot element (e.g., using the 'style' parameter)
    pivot_index = left  # For example, selecting the leftmost element as pivot

    # Partition the elements based on the pivot
    pivot = values[pivot_index]
    i = left
    j = right
    while i <= j:
        while values[i] < pivot:
            i += 1
        while values[j] > pivot:
            j -= 1
        if i <= j:
            values[i], values[j] = values[j], values[i]
            i += 1
            j -= 1

    # Recursively sort the left and right partitions if they overlap with start-end
    if left < j:
        quicksort_range_helper(values, left, j, start, end, style)
    if i < right:
        quicksort_range_helper(values, i, right, start, end, style)
    # ===end student section===


def pivot_index_mo3(values, left, right):
    """
    Returns the index of the item that is the median of the left, right and
    middle value in the list. The return value should normally be
    either left, right or middle.
    If there are only two items in the range, i.e. if right==left+1,
    then return the index of the first (left) item as there are only two items
    to find the median of, so we can't get a middle index...
    If there is only one item in the range then also simply
    return the left index, i.e. if left==right, then return left.
    If the left, middle and right values are all the same then return
    the middle index. It doesn't really matter which one but we specify
    middle for consistency - and it sorta feels nicer.

    >>> print(pivot_index_mo3([0,1,2],0,2))
    1
    >>> pivot_index_mo3([2,1,0],0,2)
    1
    >>> pivot_index_mo3([1,2,3],0,2)
    1
    >>> pivot_index_mo3([3,2,1],0,2)
    1
    >>> pivot_index_mo3([3,5,1],0,2)
    0
    >>> pivot_index_mo3([1,5,3],0,2)
    2
    >>> pivot_index_mo3([1,2],0,1)
    0
    >>> pivot_index_mo3([3,1],0,1)
    0
    >>> pivot_index_mo3([1,2],1,1)
    1
    >>> x = [1,1,3]
    >>> i = pivot_index_mo3(x,0,2)
    >>> x[i]
    1
    >>> y = [1,3,1]
    >>> i = pivot_index_mo3(y,0,2)
    >>> y[i]
    1
    >>> z = [3,1,1]
    >>> i = pivot_index_mo3(z,0,2)
    >>> z[i]
    1
    >>> xx = [1,3]
    >>> i = pivot_index_mo3(xx,0,1)
    >>> xx[i]
    1
    >>> pivot_index_mo3([1,2,2,5,2,8,10],0,6)
    3
    >>> pivot_index_mo3([1,6,0,5,9,8,10],0,4)
    0
    >>> pivot_index_mo3([9,6,9,5,9,8,10],0,4)
    2
    """
    # ---start student section---
    middle = (left + right) // 2

    # Retrieve values at left, middle, and right indices
    left_value = values[left]
    middle_value = values[middle]
    right_value = values[right]

    # Check if there is only one item in the range
    if left == right:
        return left

    # Check if there are only two items in the range
    if right == left + 1:
        return left

    # Check if the left, middle, and right values are all the same
    if left_value == middle_value == right_value:
        return middle  # Return the middle index

    # Determine the median index
    # Determine the median index without using the sort method
    if (left_value <= middle_value <= right_value) or (right_value <= middle_value <= left_value):
        return middle
    elif (middle_value <= left_value <= right_value) or (right_value <= left_value <= middle_value):
        return left
    else:
        return right
    # ===end student section===

if __name__ == "__main__":
    x = read_data("data/list1.txt")

    # Sort the data
    x.sort()

    # Calculate the number of items in the list
    num_items = len(x)

    # Find the median based on even or odd number of items
    if num_items % 2 == 1:
        # Odd number of items, median is the middle value
        median = x[num_items // 2]
    else:
        # Even number of items, median is the average of the two middle values
        middle1 = x[num_items // 2 - 1]
        middle2 = x[num_items // 2]
        median = (middle1 + middle2) / 2

    # Print the median
    print("The median is:", median)
    # i = pivot_index_mo3(xx, 0, len(xx)-1)
    # print(xx[i])
    # x = [34, 42, 87, 78, 94, 38, 16, 68, 69, 93]
    # print(pivot_index_mo3(x, 0, len(x)-1))