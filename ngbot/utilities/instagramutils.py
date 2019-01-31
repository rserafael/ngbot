import time
import sys
from os.path import dirname, join, abspath

_directory_ = dirname(abspath(__file__))
sys.path.append(_directory_)
from toots import init_chrome_driver

class Instagram(object):
    def __init__(self):
        raise NotImplementedError("This is a static class. Should not be instantiated.")

    def create_username(person):
        dates = [person.day, person.year, person.month]
        username = "{0}{1}{2}".format(person.lastname, person.firstname, random.choice(dates))
        return username.lower()

    def account_creation(email, full_name, username, password):
        try:
            writing_time = 0.8

            driver = init_chrome_driver(False, False, "https://www.instagram.com/")
            time.sleep(2)

            email_element = driver.find_element_by_name("emailOrPhone")
            email_element.send_keys(email)
            time.sleep(writing_time)

            fname = driver.find_element_by_name("fullName")
            fname.send_keys(full_name)
            time.sleep(writing_time)

            uname = driver.find_element_by_name("username")
            uname.send_keys(username)
            time.sleep(writing_time)

            pwd = driver.find_element_by_name("password")
            pwd.send_keys(password)
            time.sleep(writing_time)

            time.sleep(2)

            return True
        except Exception as err:
            print("Instagram.account_creation: {0}".format(type(err)))
            print(err)
            print("===============================")
            return False

    def create_account(person, verbose=False):
        person.username = Instagram.create_username(person)
        if verbose:
            print("username ({0}) created.".format(person.username))
        result = Instagram.account_creation(person.email, "{0} {1}".format(person.firstname, person.lastname),
                                            person.username, person.password)
        return result
