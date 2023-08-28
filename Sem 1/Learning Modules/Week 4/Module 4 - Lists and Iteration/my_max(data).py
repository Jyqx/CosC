def my_max(data):
    """Checks for biggest number in list"""
    max_length = data[0]
    for num in data:
        if num > max_length:
            max_length = num
    return max_length

print(my_max([11, 99, 3, -6]))