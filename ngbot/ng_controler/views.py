#====== Global Variables ==========
from os.path import dirname, abspath, join
_directory_ = dirname(abspath(__file__))
#==================================

#====== Sys Path Configuration =====
import sys
sys.path.append(join(dirname(_directory_), 'utilities'))
#=================================

#====== Imports ====================
from django.http import JsonResponse
import time
from tools import init_chrome_driver
import random
#====================================


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

        dates = [ person['day'], person['year'], person['month'] ]
        username = "{0}{1}{2}".format(person['lastname'], person['firstname'], random.choice(dates))
        return username


    def create_account(request, email, full_name, username, password):

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
        #find the sign up button

        # btns = driver.find_elements_by_tag_name("button")
        # sign_up_btn = None
        # for btn in btns:
        #     if btn.get_property("innerText").find("Sign up") != -1:
        #         sign_up_btn = btn
        #         break
        # if sign_up_btn != None:
        #     retry_sign_up(driver, sign_up_btn, uname)
        # else:
        #     print("Não encontramos o Sign Up Button")

def modelstest(request):
    from email_sign_up.models import Person
    people = Person.objects.all()
    person = random.choice(people)
    people =
    Instagram.create_account()
    return JsonResponse({person['firstname'], person['lastname']})

# if __name__ == "__main__":
    # global email, full_name, username, password
    # create_account(None, email, full_name, username, password)
    # import sys
    # print(sys.path)
    # sys.path.append(dirname(this_directory))
    # sys.path.append(dirname(join(this_directory, 'email_sign_up')))
    # from django.conf import settings
    # if not settings.configured:
    #     print("configuring settings")
    #     from ngbot import settings as ngbot_settings
    #     settings.configure(default_settings=ngbot_settings, DEBUG=True)
    #     time.sleep(5)
    # try:
    #
    #
    # except Exception as err:
    #     print("Type: {0}: ".format(type(err)))
    #     print(err)