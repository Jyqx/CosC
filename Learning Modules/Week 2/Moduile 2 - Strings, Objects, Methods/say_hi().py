def say_hi():
    """ Function that takes name input then capitilize and prints "Hi 'name' """
    name = str(input("What is your name? "))
    print(f"Hi  {name.capitalize()}")

say_hi()