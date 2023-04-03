def generate_daily_totals(input_filename, output_filename):
    """Writes daily totals into new file"""
    path = "lab6_data/"
    with open(path + input_filename, "r") as infile:
        with open(path + output_filename, "w") as outfile:
            for line in infile:
                parts = line.strip().split(",")
                date = parts[0]
                values = [float(v) for v in parts[1:]]
                daily_total = sum(values)
                outfile.write(f"{date} = {daily_total:.2f}\n")

generate_daily_totals('data60.txt', 'totals60.txt')
checker = open('lab6_data/totals60.txt')
print(checker.read())
checker.close()