def file_size(filename):
    """Return length of data file"""
    with open(filename, "r") as infile:
        data = infile.read()
        infile.close()
        return(len(data))
print(file_size('data.txt'))
