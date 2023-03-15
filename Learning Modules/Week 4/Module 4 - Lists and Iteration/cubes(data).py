def cubes(data):
    """Cubes shit"""
    result = []
    for n in data:
        result.append(n * n * n)
    return result

cubes_list = cubes([1, 2, 4])
print(cubes_list)