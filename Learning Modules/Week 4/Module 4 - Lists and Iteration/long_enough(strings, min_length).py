def long_enough(strings, min_length):
    """Long strings"""
    long_string = []
    for n in strings:
        if len(n) >= min_length:
            long_string.append(n)
    return long_string