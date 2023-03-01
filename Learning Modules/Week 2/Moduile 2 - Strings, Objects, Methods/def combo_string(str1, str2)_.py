def combo_string(str1, str2):
    """
    Calculate string lengths and create a shortlongshort
    """
    if len(str1) < len(str2):
        low = str1
        high = str2
    else:
        high = str1
        low = str2
    return low+high+low

print(combo_string("hi","hello"))