import os
import sys
import pickle


def print_lol(the_list, indent=False, level=0, out=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, out)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=out)
            print(each_item, file=out)


man = []
other = []
try:
    data = open('sketch.txt')
    for each_line in data:
        try:
            (role, line_sopken) = each_line.split(':', 1)
            line_sopken = line_sopken.strip()
            if role == "Man":
                man.append(line_sopken)
            elif role == "Other Man":
                other.append(line_sopken)
        except ValueError:
            pass
    data.close()
except IOError:
    print("The file is missing!")
try:
    with open("man_data.txt", "w") as man_txt, open("other_data.txt", "w")as other_txt:
        print_lol(man, out=man_txt)
        print_lol(other, out=other_txt)
except IOError as err:
    print("file error:", + str(err))
