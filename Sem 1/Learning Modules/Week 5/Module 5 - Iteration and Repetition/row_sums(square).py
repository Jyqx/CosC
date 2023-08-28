def row_sums(square):
    """Sums each row"""
    added = []
    for i in range(len(square)):
        add = 0
        for j in range(len(square[i])):
            add += square[i][j]
        added.append(add)
    return added

magic_square = [
    [2, 7, 6],
    [9, 5, 1],
    [4, 3, 8]
]
print(row_sums(magic_square))