import os
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
        print(man, file=man_txt)
        print(other, file=other_txt)
except IOError as err:
    print("file error:", + str(err))
# finally:
#     if man_txt in locals():
#         man_txt.close()
#     if other_txt in locals():
#         other_txt.close()
