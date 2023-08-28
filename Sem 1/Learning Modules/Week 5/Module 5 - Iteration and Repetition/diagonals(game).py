# Uses list comprehension to shorten for loop into 1 line
def diagonals(game):
    "Returns a list that shows the diagonals of a tictacetoe board"
    diagonal1 = [game[i][i] for i in range(3)]
    diagonal2 = [game[i] [2-i] for i in range(3)]  
    return (diagonal1, diagonal2)

board = [['O', 'O', 'O'],
         ['X', 'X', ' '],
         [' ', 'O', 'X']]
diags = diagonals(board)
print(diags)