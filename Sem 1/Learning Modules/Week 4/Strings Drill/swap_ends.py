def swap_ends(s):
    """Swap ends"""
    first = s[0]
    last = s[-1:]
    word = last + s[1:-1] + first
