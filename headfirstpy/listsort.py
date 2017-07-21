# coding=utf-8
# 生成列表
# with open("james.txt")as jaf:
#     data=jaf.readline()
# james=data.strip().split(',')


def get_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
        return data.strip().split(",")
    except IOError as ioerr:
        print("file error" + str(ioerr))
        return None


james = get_data('james.txt')
# 将分秒分隔符统一


def santize(time_string):
    if '-' in time_string:
        splitter = "-"
    elif ":" in time_string:
        splitter = ':'
    else:
        return time_string
    (mins, secs) = time_string.split(splitter)
    return (mins + '.' + secs)
# 遍历生成排序新列表
# clean_james=[]
# for each in james:
#     clean_james.append(santize(each))

# clean_james=sorted([float(santize(each)) for each in james])

# 取最快的记录且不能重复
# unique_james=[]
# for each in clean_james:
#     if each not in unique_james:
#         unique_james.append(each)

# 工厂模式去重复set()
# unique_james=sorted(set(clean_james))


print(sorted(set(santize(each) for each in james))[0:3])
