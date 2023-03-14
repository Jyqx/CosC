def extra_end(s):
    """
    Takes last 2 letters in string and print it 3 times.
    """
    last_two = s[-2:]
    return last_two * 3

print(extra_end('Hello'))