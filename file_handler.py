import sys

def open_file(filename, extension = "txt", priviledges = "w"):
    file = open(f"{filename}.{extension}", priviledges)
    sys.stdout = file
    return file

def close_file(file):
    file.close()
    sys.stdout = sys.__stdout__