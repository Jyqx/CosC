def calculate_steps_to_one(n):
    steps = 0
    while n > 1:
        n = n // 2  # Integer division to halve the size of the problem
        steps += 1
    return steps

n = int(input("Please input number: "))
steps_needed = calculate_steps_to_one(n)
print(f"Number of steps needed to reduce {n} items to 1 item: {steps_needed}")
