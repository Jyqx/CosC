# def dangerous(a):
#     z = 500
#     x = z + a
#     print(x)
#     return a // x

# print(dangerous(-500))

def trouble(a, b):
    z = 1000
    x = z - a
    y = z - b
    x = x + 500
    print(x, y, a, z, b)
    (x, y) = (y, x)
    if x >= y:
        z = x - y
    else:
        z = x // y
    z = z * y
    return z

print(trouble(-1000, -1000))