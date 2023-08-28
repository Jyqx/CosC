def print_numbered_lines(filename):
    """Print each line iin numbered order"""
    with open(filename, "r") as infile:
        num = 1
        for line in infile:
            number = str(line.strip())
            print(f"{num}: {number}")
            num +=1

print_numbered_lines('marks2.txt')
