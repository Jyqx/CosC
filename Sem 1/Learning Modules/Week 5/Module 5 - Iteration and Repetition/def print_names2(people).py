# Fix this code
# def print_names2(people):
#     """Print a list of people's names, which each person's name
#        is itself a list of names (first name, second name etc)
#     """
#     for person in people:
#         to_print = ""
#         for name in person:
#             to_print += name + " "
#         print(to_print)

def print_names2(people):
    """Print a list of people's names, which each person's name
    is itself a list of names (first name, second name etc)
    """
    i = 0
    output =""
    while i < len(people):
        j = 0
        while j < len(people[i]):
            output_name = (people[i][j])
            output += (output_name + " ")
            j += 1
        output += "\n"
        i +=1
    print(output)

print_names2([['Bilbo', 'Baggins'], ['Gollum'], ['Tom', 'Bombadil'], ['Aragorn']])