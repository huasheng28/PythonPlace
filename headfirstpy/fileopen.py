import os
if os.path.exists('sketch.txt'):
    data = open('sketch.txt')
    for each_line in data:
        if each_line.find(':') != -1:
            (role, line_spoken) = each_line.split(':', 1)
            print(role, end='')
            print(' said:', end='')
            print(line_spoken, end='')
        else:
            print(each_line, end='')
    # for each_line in data:
    #     try:
    #         (role,line_spoken)=each_line.split(':',1)
    #         print(role,end='')
    #         print(' said:',end='')
    #         print(line_spoken,end='')
    #     except:
    #         pass
    data.close()
else:
    print("The data is not found!")
