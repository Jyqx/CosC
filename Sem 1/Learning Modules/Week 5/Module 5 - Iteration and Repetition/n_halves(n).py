def n_halves(n):
    """Halves N until under 1"""
    count = 0
    while n > 1:
        n /= 2
        count += 1
    return count


print(n_halves(17))