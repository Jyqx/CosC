def print_daily_totals(rainfalls):
    """Print daily rainfall on newlines"""
    for i in range(len(rainfalls)):
        add_row = 0
        for j in range(len(rainfalls[i])):
            add_row += rainfalls[i][j]
        print(f"Day {i} total: {add_row}")

daily_rain = [ 
      [0, 9, 3, 7],
      [11, 9, 0, 0],
      [0, 10, 12, 20],
      [0, 0, 0, 0],
      [1, 3, 4, 1],
      [2, 8, 10, 0],
      [0, 0, 0, 0]
]
print_daily_totals(daily_rain)