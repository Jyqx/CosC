def bad_combine(list_1, list_2):
    """
    Combine two lists with list 1 last element removed and and
    list 2 first element removed.
    """
    bad_list = []
    bad_list = (list_1[:-1] + list_2[1:])
    return bad_list
ans = bad_combine([10, 20, 30], [100, 200, 300])
print(ans)