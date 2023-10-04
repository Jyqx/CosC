import random

def generate_items():
    # Input the file name and values
    file_name = (input("Enter the file name: ") + ".txt")
    num_items = int(input("Enter the number of items: "))
    min_value = input("Enter the minimum value: ")
    max_value = input("Enter the maximum value: ")

    # Check if the user provided min_value and max_value
    if min_value == "":
        min_value = 1  # Default minimum value
    else:
        min_value = int(min_value)

    if max_value == "":
        max_value = num_items  # Default maximum value
    else:
        max_value = int(max_value)

    # Generate a list of unique random integers
    unique_items = random.sample(range(min_value, max_value + 1), num_items)

    # Write the unique items to the file
    with open(file_name, 'w') as file:
        for item in unique_items:
            file.write(str(item) + '\n')

    print(f"File '{file_name}' with {num_items} unique items has been generated.")

def generate_reverse():
    # Create a file with 10,000 items in reverse order
    with open("file17.txt", "w") as file:
        for i in range(10000, 0, -1):
            file.write(str(i) + "\n")

generate_reverse()