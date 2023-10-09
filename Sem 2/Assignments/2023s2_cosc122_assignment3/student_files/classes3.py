"""
classes.py
COSC122 Assignment 3

This module provides classes that are to be used to complete the COSC122
Assignment 3. These have many careful restrictions placed on them, but do
provide a sufficient interface to solve the problems given.
"""


from stats import StatCounter, COMPARISONS, HASHES
from abc import ABC, abstractmethod


class Priority:
    """A simple int wrapper so that we can count comparisons.
    You can use all the usual comparison operators on these.
    """

    def __init__(self, priority):
        """IMPORTANT!
        You should never access _priority directly!
        That is, you shouldn't be doing things like the following
            patient.priority._priority < something.  # NO!
        This would cause trouble with the internal comparison counting!
        You should simply do things like the following
            patient.priority < something   # YES
        The underscore (_) indicates that this is an internal variable
        and should only be used by the Priority methods themselves.
        """
        self._priority = priority  # don't access _priority directly!

    def __repr__(self):
        return repr(self._priority)

    def __str__(self):
        return str(self._priority)

    def __eq__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(
                "Priority objects can only be compared to other Priority objects"
            )
        StatCounter.increment(COMPARISONS)
        return self._priority == other._priority

    def __le__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(
                "Priority objects can only be compared to other Priority objects"
            )
        StatCounter.increment(COMPARISONS)
        return self._priority <= other._priority

    def __ne__(self, other):
        if other is None:
            StatCounter.increment(COMPARISONS)
            return False
        if not isinstance(other, Priority):
            raise ValueError(
                "Priority objects can only be compared to other Priority objects"
            )
        StatCounter.increment(COMPARISONS)
        return self._priority != other._priority

    def __lt__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(
                "Priority objects can only be compared to other Priority objects"
            )
        StatCounter.increment(COMPARISONS)
        return self._priority < other._priority

    def __gt__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(
                "Priority objects can only be compared to other Priority objects"
            )
        StatCounter.increment(COMPARISONS)
        return self._priority > other._priority

    def __ge__(self, other):
        if not isinstance(other, Priority):
            raise ValueError(
                "Priority objects can only be compared to other Priority objects"
            )
        StatCounter.increment(COMPARISONS)
        return self._priority >= other._priority

    def __hash__(self):
        StatCounter.increment(HASHES)
        return hash(self._priority)


class Patient:
    """A patient object to hold all the information needed to
    store them in a patient queue.
    """

    def __init__(self, name, disease_severity, days_since_diagnosis):
        self.name = name
        self.disease_severity = disease_severity
        self.days_since_diagnosis = days_since_diagnosis
        self.priority = Priority(self._calc_priority())

    def _calc_priority(self):
        return self.disease_severity**2 + self.days_since_diagnosis * 100

    def __repr__(self):
        return "Patient('{}', {})".format(self.name, self.priority)


class PriorityQueue(ABC):
    """An Abstract base class for priority queues.
    All priority queues must have an enqueue and dequeue method.
    This also provides a __str__ method so you can visualize your queue.
    """

    @abstractmethod
    def enqueue(self, patient):
        pass

    @abstractmethod
    def dequeue(self):
        pass

    def __str__(self):
        return "PQ[{}]".format(", ".join(str(p) for p in self.data))
