def column_sums(square):
    """sum columns"""
    sums = []
    for row in range(len(square)):
        add = 0
        for col in range(len(square)):
            add += square[col][row]
        sums.append(add)
    return sums

ascending_square = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]
print(column_sums(ascending_square))