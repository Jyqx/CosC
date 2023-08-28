def duplicate_last(data):
    """Duplicate last element of list"""
    n = data
    newdata = n[-1:]
    return data + newdata

# Uc Solution
# def duplicate_last(data):
#     """Returns the list of data with the last item duplicated"""
#     return data + [data[-1]]

original = [1,2,3]
result = duplicate_last(original)
print(result)