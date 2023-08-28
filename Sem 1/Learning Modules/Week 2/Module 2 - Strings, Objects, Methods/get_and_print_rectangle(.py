# Attempt 1
# def get_and_print_rectangle(): 
#     """Prints rectangle area using input"""
#     width_input = input("Rectangle width? ")
#     height_input = input("Rectangle height? ")
#     area = float(width_input) * float(height_input)
#     print("The area of the rectangle is: " + str(area))

# Attempt 2
def get_and_print_rectangle(): 
    """Prints rectangle area using input"""
    width_input = float(input("Rectangle width? "))
    height_input = float(input("Rectangle height? "))
    area = width_input* height_input
    print("The area of the rectangle is: " + str(area))

get_and_print_rectangle()