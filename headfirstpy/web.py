import pickle


def santize(time_string):
    if '-' in time_string:
        splitter = "-"
    elif ":" in time_string:
        splitter = ':'
    else:
        return time_string
    (mins, secs) = time_string.split(splitter)
    return (mins + '.' + secs)


class Athlete:
    def __init__(self, a_name, a_dob=None, a_times=[]):
        list.__init__([])
        self.name = a_name
        self.dob = a_dob
        self.extend(a_times)

    def top3(self):
        return sorted(set([santize(t) for t in self]))[0:3]


def get_data(filename):
    try:
        with open(filename) as f:
            data = f.readline()
        temp = data.strip().split(',')
        return Athlete(temp.pop(0), temp.pop(0), temp)
    except IOError as ioerr:
        print('File Error: ' + str(ioerr))
        return None


def put_to_store(files_list):
    all_athlete = {}
    for each_file in files_list:
        ath = get_data(each_file)
        all_athlete[ath.name] = ath
    try:
        with open('athletes.pickle', 'wb') as athf:
            pickle.dump(all_athlete, athf)
    except IOError as ioerr:
        print('File error (put and store):' + str(ioerr))
    return all_athlete


def get_from_store():
    all_athletes = {}
    try:
        with open('athlete.pickle', 'rb') as athf:
            all_athletes = pickle.load(athf)
    except IOError as ioerr:
        print('File error(get and store):' + str(ioerr))
    return all_athletes
