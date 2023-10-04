def zoom(n):
    if n > 2:
        print("Zooming -1")
        zoom(n-1)
        print("Zooming -2")
        zoom(n-2)
        print("Printing N")
        print(n)

zoom(6)