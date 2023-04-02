def thing(x, y):
    z = 0
    k = 0
    for i in range(len(x)):
        if x[i] == -y[i]:
            z += x[i]
            k += 1
    print("k =", k, "z =", z)

x = [10,10,10,10]         
y = [-10,-10,-10,-10]     
thing(x, y)