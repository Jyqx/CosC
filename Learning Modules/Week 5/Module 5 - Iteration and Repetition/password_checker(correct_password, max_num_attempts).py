def password_checker(correct_password, max_num_attempts):
    """ Asks the user for a password and checks if it is correct.
        The user can try at most max_num_attempts times.
    """

    num_attempts = 0
    password_found = False

    while num_attempts < max_num_attempts and password_found == False:
        password = input("What's the password: ")
        num_attempts += 1
        if password == correct_password:
            password_found = True
        else:
            print("Incorrect password.")

    if password == correct_password:
        print("You may enter.")
    else:
        print("Max number of attempts exceeded.")

password_checker("CaputDraconis123", 3)