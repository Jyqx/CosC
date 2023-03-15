def abs_values(numbers):
    """Changes to abs values in a list"""
    result = []
    for n in numbers:
        result.append(abs(n))
    return result

print(abs_values([2, -3, -7]))