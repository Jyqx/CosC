# Fix this code
# def print_cumulative_values(values):
#     """Prints the first value on a line by itself, then on 
#        the next line the first two values separated by a space, etc
#        until all values in the list are printed on a single
#        line separated by spaces."""
#     output = ""
#     for value in values:
#         output += value + " "
#         print(output)

def print_cumulative_values(values):
    """Prints value onto new list"""
    i = 0
    while i < len(values):
        print(values[i] + " ")
        i += 1

print_cumulative_values(['John', 'Mary', 'Donald'])