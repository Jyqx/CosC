def  max_num_in_file(filename):
    """Returns the largest integer found in the file"""
    with open(filename, "r") as infile:
        max_num = float('-inf')
        for line in infile:
            number = int(line.strip())
            if max_num < number:
                max_num = number
    return max_num


answer = max_num_in_file('max_num_in_file_test_01.txt')
print(answer)