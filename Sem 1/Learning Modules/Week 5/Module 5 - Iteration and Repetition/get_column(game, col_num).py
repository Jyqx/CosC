def get_column(game, col_num):
    """Returns a column in a tic-tac-toe game"""
    col = []
    for row in range(3):
        col.append(game[row][col_num])
    return col

board = [['O', 'X', 'O'],
         ['X', ' ', ' '],
         ['X', ' ', ' ']]
column1 = get_column(board, 0)
print(column1)