def print_squares_to_number(number):
    """print squares to range of numbers"""
    if number >= 1:
        for i in range(1, (number+1)):
            print(f"{i} * {i} = {i * i}")
    else:
        print("ERROR: number must be at least 1")

print_squares_to_number(5)