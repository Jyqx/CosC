def num_words(string):
    """Splits the strings into a list and counts number of items in list"""
    split = len(string.split())
    return split

word_count = num_words("Welcome to lists!")
print(word_count)
