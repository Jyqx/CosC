def x_at_either_end(string):
    """Checks if string ends or starts with x"""
    return string.startswith("x") or string.endswith("x")

print(x_at_either_end('pax'))