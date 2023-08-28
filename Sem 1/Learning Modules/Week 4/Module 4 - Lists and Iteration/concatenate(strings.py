def concatenate(strings):
    """Concatenates strings together"""
    fullstring = ""
    for n in strings:
        fullstring += n
    return fullstring  

print(concatenate(["x", "yy", "zzz"]))