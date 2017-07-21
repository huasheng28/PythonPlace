def get_data(filename):
    try:
        with open(filename) as f:
            data=f.readline()
        temp=data.strip().split(",")
        return ({
            'name':temp.pop(0),
            'dob':temp.pop(0),
            'times':str(sorted(set([santize(t) for t in temp]))[0:3])
        })
    except IOError as ioerr:
        print("file error" + str(ioerr))
        return None

def santize(time_string):
    if '-' in time_string:
        splitter = "-"
    elif ":" in time_string:
        splitter= ':'
    else:
        return time_string
    (mins ,secs) = time_string.split(splitter)
    return (mins + '.' + secs)

sarah=get_data('sarah2.txt')
# (sarah_name, sarah_dob) = (sarah.pop(0), sarah.pop(0))
# print(sarah_name + "'s fastert time are : " + str(sorted(set([santize(t) for t in sarah]))[0:3]))


print(sarah['name'] + "'s fatest times are : " + sarah['times'])