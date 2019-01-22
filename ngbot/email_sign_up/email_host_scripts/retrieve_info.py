import json
import os

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

    def __init__(self, name, lastname, country, sex):
        self.name = name
        self.lastname = lastname
        self.country = country
        self.sex = sex


def set_br_persons():
    global br_male_names, br_female_names, br_lastnames

    br_persons = {}
    count = 1
    try:
        for n in br_male_names.keys():
            try:
                name = br_male_names[n]
                for ln in br_lastnames:
                    lastname = br_lastnames[ln]
                    br_persons['person{0}'.format(count)] = Person(name, lastname, 'BR', "M").__dict__
                    count += 1
            except Exception as err:
                print("an error")
                print(err)

        for n in br_female_names:
            name = br_male_names[n]
            for ln in br_lastnames:
                lastname = br_lastnames[ln]
                br_persons['person{0}'.format(count)] = Person(name, lastname, 'BR', "F").__dict__
                count += 1
        return br_persons
    except Exception as error:
        print("an error")
        print(error)


def set_us_persons():
    global br_male_names, br_female_names, br_lastnames, us_male_names, us_female_names, us_lastnames

    us_persons = {}
    count = 1
    for n in us_male_names:
        name = us_male_names[n]
        for ln in us_lastnames:
            lastname = us_lastnames[ln]
            us_persons['person{0}'.format(count)] = Person(name, lastname, 'US', "M").__dict__
            count += 1

    for n in us_female_names:
        name = us_male_names[n]
        for ln in us_lastnames:
            lastname = us_lastnames[ln]
            us_persons['person{0}'.format(count)] = Person(name, lastname, 'US', "F").__dict__
            count += 1
    return us_persons


def write_json(file_name, person_dict, file_format="json"):
    index = 1
    full_file_name = "{0}{1}.{2}".format(file_name, index, file_format)
    while os.path.exists(full_file_name):
        index += 1
        full_file_name = "{0}{1}.{2}".format(file_name, index, file_format)
    file = open(full_file_name, 'w')
    file.writelines(json.dumps(person_dict))
    file.close()


def write_person_json():
    get_all_names()
    br_persons = set_br_persons()
    us_persons = set_us_persons()
    write_json("br_persons", br_persons)
    write_json("us_persons", us_persons)


if __name__ == "__main__":
    write_person_json()
