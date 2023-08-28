def make_out_word(out, word):
    """Even more cringe"""
    mid = len(out) // 2
    first = out[:mid]
    last = out[mid:]
    return first + word + last