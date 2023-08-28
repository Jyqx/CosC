def guess_a_number(target, low, high, max_tries):
    '''Asks the user to guess the target number between high and low.
       max_tries is the maximum allowed guesses.
    '''
    print("I'm thinking of a number between {} and {}.".format(low, high))
    num_tries = 1
    num = int(input("What do you think it is? "))
    while num_tries < max_tries and num != target:
        print("That's not my number. Try again.")
        num = int(input("What do you think it is? "))
        num_tries += 1
    if num == target:
        print("Congratulations! You guessed my number!")
    else:
        print("Sorry, too many failed guesses.")

guess_a_number(2, 1, 5, 3)