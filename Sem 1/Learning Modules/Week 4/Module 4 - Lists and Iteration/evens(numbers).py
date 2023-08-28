def evens(numbers):
    """Takes even numbers and puts it in a new list"""
    even = []
    for n in numbers:
        if n % 2 == 0: 
            even.append(n)
    return even
