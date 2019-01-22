import json
import os
import random

br_male_names = None
br_female_names = None
br_lastnames = None
us_male_names = None
us_female_names = None
us_lastnames = None


def get_all_names():
    global br_male_names, br_female_names, br_lastnames, us_male_names, us_female_names, us_lastnames

    br_male_names = json.load(open('br_male_names.json', 'r'), )
    br_female_names = json.load(open('br_female_names.json', 'r'))
    br_lastnames = json.load(open('br_lastnames.json', 'r'))
    us_male_names = json.load(open('us_male_names.json', 'r'))
    us_female_names = json.load(open('us_female_names.json', 'r'))
    us_lastnames = json.load(open('us_lastnames.json', 'r'))


class Person(object):

    def __init__(self, name, lastname, country, sex, day, month, year):
        self.name = name
        self.lastname = lastname
        self.country = country
        self.sex = sex
        self.day = day
        self.month = month
        self.year = year


def random_date():
    day = random.choice(range(1, 28))
    month = random.choice(range(1, 13))
    year = random.choice(range(1980, 2001))
    return day, month, year


def set_br_persons():
    global br_male_names, br_female_names, br_lastnames

    br_males = {}
    count = 1

    for n in br_male_names:
        name = br_male_names[n]
        for ln in br_lastnames:
            lastname = br_lastnames[ln]
            day, month, year = random_date()
            br_males['person{0}'.format(count)] = Person(name, lastname, 'BR', "M", day, month, year).__dict__
            count += 1

    br_females = {}
    count = 1
    for n in br_female_names:
        name = br_female_names[n]
        for ln in br_lastnames:
            lastname = br_lastnames[ln]
            day, month, year = random_date()
            br_females['person{0}'.format(count)] = Person(name, lastname, 'BR', "F", day, month, year).__dict__
            count += 1
    return br_males, br_females


def set_us_persons():
    global br_male_names, br_female_names, br_lastnames, us_male_names, us_female_names, us_lastnames

    us_males = {}
    count = 1
    for n in us_male_names:
        name = us_male_names[n]
        for ln in us_lastnames:
            lastname = us_lastnames[ln]
            day, month, year = random_date()
            us_males['person{0}'.format(count)] = Person(name, lastname, 'US', "M", day, month, year).__dict__
            count += 1

    us_females = {}
    count = 1
    for n in us_female_names:
        name = us_female_names[n]
        for ln in us_lastnames:
            lastname = us_lastnames[ln]
            day, month, year = random_date()
            us_females['person{0}'.format(count)] = Person(name, lastname, 'US', "F", day, month, year).__dict__
            count += 1
    return us_males, us_females


def write_json(file_name, person_dict, file_format="json"):
    index = 0
    i = ''
    full_file_name = "{0}{1}.{2}".format(file_name, i, file_format)
    while os.path.exists(full_file_name):
        index += 1
        i = index
        full_file_name = "{0}{1}.{2}".format(file_name, i, file_format)
    file = open(full_file_name, 'w')
    file.writelines(json.dumps(person_dict, skipkeys=True, ensure_ascii=False, indent=2))
    file.close()


def write_person_json():
    get_all_names()
    br_males, br_females = set_br_persons()
    us_males, us_females = set_us_persons()
    write_json("br_males", br_males)
    write_json("br_females", br_females)
    write_json("us_males", us_males)
    write_json("us_females", us_females)


if __name__ == "__main__":
    write_person_json()
