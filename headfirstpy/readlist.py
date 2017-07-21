movies = [0, 1, [2, [3, 4, 5, 6], 7], 8]
# for each_item in movies:
#     if isinstance(each_item,list):
#         for one in each_item:
#             if isinstance(one,list):
#                 for two in one:
#                     print(two)
#             else:
#                 print(one)
#     else:
#         print(each_item)


def print_lol(the_list, indent=False, level=0):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='')
            print(each_item)


print_lol(movies, True)
