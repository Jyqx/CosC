"""
utilities.py
A collection of useful structures to complete this assignment.
"""


DATA_DIR = "./test_data/"


def read_test_data(filename):
    """Read in the test data from the file given by filename.
    This function accepts the name of a file: filename.
    It returns a list of Patient objects for import alongside
    a list of instructions (enqeueue/dequeue) for your heap to complete.
    Example usage:
    >>> from classes3 import Patient
    >>> from utilities import verify_heapness, read_test_data
    >>> patients, instructions = read_test_data("test_data/test_data-5-5-0.txt")
    """
    import_data = []
    instructions = []
    with open(filename, encoding="utf8") as f:
        n_imports = int(_get_next_line(f))
        for _ in range(n_imports):
            line = _get_next_line(f)
            import_data.append(_create_patient(line))

        first_instruction = _get_next_line(f)
        lines = [first_instruction] if first_instruction else []
        lines += f.readlines()
        for line in lines:
            instruction, information = line.split(maxsplit=1)
            if instruction == "enqueue":  # Enqueue the patient
                instructions.append(("enqueue", _create_patient(information)))
            elif (
                instruction == "dequeue"
            ):  # Dequeue a patient, should assert match with given name
                instructions.append(("dequeue", information.strip()))
            elif instruction == "remove":  # Remove the named patient
                # information is just a name, not a patient
                instructions.append(("remove", information.strip()))
            else:
                raise NameError(
                    "Priority Queue instruction not understood:\n" + f"{line}"
                )
    return import_data, instructions


def verify_heapness(heap, index=0):
    """Make sure that the heap invariant is maintained.
    Example usage:
    >>> from classes3 import Patient
    >>> from utilities import verify_heapness, read_test_data
    >>> patients, _ = read_test_data("test_data/test_data-5-5-0.txt")
    >>> my_heap = PatientQueueHeap(start_data=patients, fast=True)
    >>> verify_heapness(my_heap)
    """
    child_indices = heap._child_indices(index)
    valid_child_indices = [i for i in child_indices if i < len(heap.data)]
    if not valid_child_indices:
        return True  # No children, no worries!
    parent_value = heap.data[index]
    for i in valid_child_indices:
        child_value = heap.data[i]
        if child_value.priority > parent_value.priority:
            return False
        verify_heapness(heap, index=i)
    return True


def run_tests(filename, priority_queue, fast=False, verbose=True):
    """Using the test data in the file described by 'filename', run tests on the
    'priority_queue' class given.
    Example usage:
    >>> run_tests('TestData/test_data-0-1-0.txt', PatientHeapQueue)
    """
    import_data, instructions = read_test_data(filename)
    queue = priority_queue(import_data, fast)
    for mode, data in instructions:
        if mode == "enqueue":
            if verbose:
                print("Enqueueing {}".format(data))
            queue.enqueue(data)
        elif mode == "dequeue":
            result = queue.dequeue()
            if verbose:
                print(
                    "Dequeued {}, which is {}".format(
                        result, "right" if result.name == data else "wrong"
                    )
                )
        elif mode == "remove":
            if verbose:
                print("Removing {}".format(data))
            queue.remove(data)
        if not verify_heapness(queue):
            raise AssertionError("Heap invariant violated!")
    return queue


def _create_patient(information):
    """Create a patient from a line of information."""
    from classes3 import Patient

    name, disease_severity, days_since_diagnosis = information.strip().split(",")
    return Patient(name, int(disease_severity), int(days_since_diagnosis))


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
