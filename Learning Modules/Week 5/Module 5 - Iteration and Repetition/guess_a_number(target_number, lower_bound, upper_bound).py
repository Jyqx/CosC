def guess_a_number(target_number, lower_bound, upper_bound):
    """
    Word guessing game with input.
    """
    i = False
    print(f"I'm thinking of a number between {lower_bound} and {upper_bound}.")
    while i == False:
        guess = int(input("Make a guess: "))
        if guess == target_number:
            print("Congratulations! That was my number!")
            i = True
        else:
            print("That is not my number. Enter another.")




guess_a_number(2, 1, 5)