def first_two(s):
    """First two halfs"""
    if len(s) < 2:
        return s
    else:
        return s[:2]

print(first_two('Hello'))
