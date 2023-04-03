def write_reversed_file(input_filename, output_filename):
    """Writes lines in reverse order"""
    with open(input_filename, "r") as infile:
        with open(output_filename, "w") as outfile:
            lines = infile.readlines()
            for line in reversed(lines):
                outfile.write(f'{line.strip()}\n')

import os.path
write_reversed_file('data.txt', 'reversed1.txt')
if not os.path.exists('reversed1.txt'):
    print("You don't seem to have created the required output file!")
else:
    print(open('reversed1.txt').read())
