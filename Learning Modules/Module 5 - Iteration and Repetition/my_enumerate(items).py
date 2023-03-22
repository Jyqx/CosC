def my_enumerate(items):
    """Cringe stuff"""
    enum_items = []
    for n in range(len(items)):
        enum_items.append((n, items[n]))
    return enum_items

ans = my_enumerate(['dog', 'pig', 'cow'])
print(ans)