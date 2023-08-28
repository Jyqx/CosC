def whatsit(x):
    y = []
    for i in range(len(x)):
        if i % 2 == 0:
            y.append(x[i] + i)
        else:
            y.append(x[i] - i)
    print(y)

whatsit([7, 12, -4, 7]      )