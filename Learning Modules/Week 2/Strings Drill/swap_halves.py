def swap_halves(s):
    """Swap halves"""
    mid = len(s) // 2
    first = s[:mid]
    last = s[mid:]
    return last + first