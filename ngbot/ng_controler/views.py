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
from instagramutils import Instagram
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


def modelstest(request):
    from email_sign_up.models import Person
    people = Person.objects.all()
    person = random.choice(people)
    while person.ngCreated:
        person = random.choice(people)
    result = Instagram.create_account(person)
    if result:
        person.ngCreated = True
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
