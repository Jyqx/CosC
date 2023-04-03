def print_reversed(filename):
    """Returns lines in reverse order"""
    with open(filename, "r") as infile:
        lines = infile.readlines()
        for line in reversed(lines):
            print(line.strip())
    

print_reversed('data.txt')
