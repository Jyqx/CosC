""" Used to help you check your comparisons count matches the actual number
of comparisons done

IMPORTANT - You shouldn't refer to __n_comparisons__ or get_comparisons in
the answer you submit to the quiz server. They won't be available!
"""


# Set marking mode to False for testing
# NOTE: it will be set to True on the quiz server!
IS_MARKING_MODE = False
ERROR = "You can't use the stats in marking mode!"

ACCESSES = "accesses"
COMPARISONS = "comparisons"
HASHES = "hashes"


class StatCounter:
    """Used to help you check your comparison count
    You shouldn't use this in your answer code as it won't work!
    """

    if not IS_MARKING_MODE:
        _stats = {COMPARISONS: 0, ACCESSES: 0, HASHES: 0}
    else:
        _stats = {COMPARISONS: ERROR, ACCESSES: ERROR, HASHES: ERROR}
    _lock = False

    def __init__(self, *args, **kwargs):
        raise TypeError("The StatCounter class should never be initialized!")

    @classmethod
    def increment(cls, counter):
        if cls._lock:
            return
        if not IS_MARKING_MODE:
            cls._stats[counter] += 1
        else:
            cls._stats[counter] = ERROR

    @classmethod
    def lock(cls):
        cls._lock = True

    @classmethod
    def unlock(cls):
        cls._lock = False

    @classmethod
    def get_count(cls, counter):
        if not IS_MARKING_MODE:
            return cls._stats[counter]
        else:
            # you shouldn't be using this in your final code!
            raise ValueError(ERROR)

    @classmethod
    def reset_counts(cls):
        if not IS_MARKING_MODE:
            cls._stats = {COMPARISONS: 0, ACCESSES: 0, HASHES: 0}
        else:
            cls._stats = {COMPARISONS: ERROR, ACCESSES: ERROR, HASHES: ERROR}

    @classmethod
    def set_count(cls, counter, count):
        """Resets the count for just the given counter"""
        if not IS_MARKING_MODE:
            cls._stats[counter] = count
        else:
            # you shouldn't be using this in your final code!
            cls._stats[counter] = ERROR

