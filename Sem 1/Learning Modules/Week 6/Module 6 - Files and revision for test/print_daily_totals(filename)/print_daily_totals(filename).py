def print_daily_totals(filename):
    """Prints daily totals"""
    path = "lab6_data/"
    with open(path + filename, "r") as infile:
        for line in infile:
            parts = line.strip().split(",")
            date = parts[0]
            values = [float(v) for v in parts[1:]]
            daily_total = sum(values)
            print(f"{date} = {daily_total:.2f}")

print_daily_totals('data63.txt')