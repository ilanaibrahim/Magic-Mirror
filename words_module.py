from random import choice

filename = r"C:\Mirror\quotes.txt"

def random_line():
    with open(filename, "r") as fp:
        lines = fp.readlines()
    return(choice(lines))
