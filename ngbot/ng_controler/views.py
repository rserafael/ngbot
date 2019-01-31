# ====== Global Variables ==========
from os.path import dirname, abspath, join

_directory_ = dirname(abspath(__file__))
# ==================================

# ====== Sys Path Configuration =====
import sys

sys.path.append(join(dirname(_directory_), 'utilities'))
# =================================

# ====== Imports ====================
from django.http import JsonResponse
import time
from tools import init_chrome_driver
import random


# ====================================


def retry_sign_up(driver, sign_up_btn, uname):
    sign_up_btn.click()
    time.sleep(1)
    error_alert = driver.find_element_by_id("ssfErrorAlert")
    if (error_alert != None):
        print("error_alert = {0}".format(error_alert.get_property("innerText")))
        input_error = driver.find_elements_by_class_name("coreSpriteInputError")
        input_refresh = driver.find_elements_by_class_name("coreSpriteInputRefresh")
        if input_error != None:
            print("Erro no Input")
            if len(input_error) >= 1:
                if input_refresh != None:
                    print("Existe algum input refresher")
                    print("len(input_refresh = {0}".format(len(input_refresh)))
                    if len(input_refresh) >= 1:
                        input_refresh[0].get_property("parentElement").click()
                        time.sleep(0.5)
                        print("username = {0}".format(uname.get_property("value")))
                        time.sleep(3)
                        print("retrying...")
                        retry_sign_up(driver, sign_up_btn, uname)
    else:
        return True


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


def modelstest(request):
    from email_sign_up.models import Person
    people = Person.objects.all()
    person = random.choice(people)
    result = Instagram.create_account(person)
    if result:
        return JsonResponse(
            {
                'firstname': person.firstname,
                'lastname': person.lastname,
                'username': person.username
            })
    else:
        return JsonResponse(
            {
                'message': 'Failed!'
            })
