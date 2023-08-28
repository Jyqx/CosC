"""
Python program to add and remove timers for tasks
"""

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = SECONDS_PER_MINUTE * 60

def to_seconds(time_string):
    """
    Take time string of form 'hh:mm:ss' and 
    return number of seconds elapsed since start of day.
    """
    split = time_string.split(":")
    hours = int(split[0]) * SECONDS_PER_HOUR
    minutes = int(split[1]) * SECONDS_PER_MINUTE
    seconds = int(split[2])
    return hours + minutes + seconds

def new_task(task_id, start_string):
    """
    Takes a list of strings and a start 
    time and returns it in a tuple
    """
    return (task_id, [to_seconds(start_string)])

def start_task(tasks, task_id):
    """
    Takes a task list and a task id then 
    appends the new task to the tasks list
    """
    if len(tasks) == 0 or len(tasks[-1][1]) == (2 or 0):
        time = input("Please enter a time (hh:mm:ss): ")
        tasks.append(new_task(task_id, time))
    else:
        print ("Can't start a timer, one is already running")

def end_active_task(tasks):
    """
    Ends the current running task from list
    """
    if tasks and len(tasks[-1]) >= 2 and len(tasks[-1][1]) == 1:
        end_time = input("Please enter a time (hh:mm:ss): ")
        tasks[-1][1].append(to_seconds(end_time))
    else:
        print("No timer is currently running")

def read_list(prompt):
    """
    Asks the user for a list of 
    values seperated by comma
    """
    input_str = input(prompt)
    input_list = input_str.split(",")
    output_list = [value.strip() for value in input_list]
    return output_list

def remove_last_task(tasks):
    """
    Removes the last task entry from the list of tasks
    """
    if not tasks:
        print("Can't remove task when none exist")
        return
    tasks.pop()

def print_report(tasks):
    """
    Prints a report of all completed tasks
    """
    print("Report:")
    for task in tasks:
        task_ids = task[0]
        time_intervals = task[1]
        if len(time_intervals) == 2:
            start_time = time_intervals[0]
            end_time = time_intervals[1]
            print(f"    ({','.join(task_ids)}) {start_time}:{end_time}")

def commands():
    """
    Main function that runs the timer program
    """
    command_lists = (
    '    [s] start',
    '    [e] end active timer',
    '    [d] delete',
    '    [r] report', 
    '    [q] quit',
    " "
    )
    print("Commands:")
    for i in command_lists:
        print(i)
    tasks = []
    while True:
        command = input("Select command: ").lower()
        if command == "s":
            task_ids = read_list("Enter task IDs: ")
            start_task(tasks, task_ids)
        elif command == "e":
            end_active_task(tasks)
        elif command == "d":
            remove_last_task(tasks)
        elif command == "r":
            print_report(tasks)
        elif command == "q":
            break
        else:
            print("Command is not valid")

commands()