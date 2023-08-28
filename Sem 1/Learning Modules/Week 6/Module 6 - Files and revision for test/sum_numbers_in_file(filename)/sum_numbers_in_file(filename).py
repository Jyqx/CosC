# def sum_numbers_in_file(filename):
#     """Sums file lines"""
#     with open(filename, "r") as infile:
#         lines = infile.readlines()
#         total = 0
#         for line in lines:
#             total += float(line.strip())
#     return total

def sum_numbers_in_file(filename):
    """Sums file lines"""
    with open(filename, "r") as infile:
        numbers = [int(line.strip()) for line in infile]
        return sum(numbers)
    
answer = sum_numbers_in_file('sum_nums_test_01.txt')
print(answer)
        
