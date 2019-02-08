# ====== Global Variables ==========
from os.path import dirname, abspath, join

_directory_ = dirname(abspath(__file__))
# ==================================

# ====== Sys Path Configuration =====
import sys

sys.path.append(join(dirname(_directory_), 'utilities'))
# =================================

# ====== Imports ====================
from django.http import JsonResponse, HttpResponse
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


def models_test(request):
    if request.method == "GET":
        from email_sign_up.models import Person
        no_ng_people = list(Person.objects.filter(ngCreated=None))
        no_ng_people.extend(list(Person.objects.filter(ngCreated=False)))
        if len(no_ng_people) > 0:
            person = random.choice(no_ng_people)
            tries = request.GET.get("tries")
            # print("tries: {0}".format(tries))
            if tries is not None:
                result = Instagram.create_account(person=person, tries=int(tries))
            else:
                result = Instagram.create_account(person=person)
            if result:
                person.ngCreated = True
                person.save()
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
        else:
            return JsonResponse(
                {
                    'message': "There is no person without instagram",
                })


def reset_all_instagram_accounts(request, pwd=None):
    if request.method == "GET":
        if pwd is not None and pwd == 'R$&ngreset95':
            from email_sign_up.models import Person
            for person in Person.objects.all():
                person.ngCreated = False
                person.username = ''
                person.save()
            return JsonResponse({'result': True})
    return JsonResponse({'result': False})


def request_show(request):
    response = show_obj(request.GET, None, True)
    if type(response) == str:
        return HttpResponse(response)
    return JsonResponse(response)


def show_obj(obj, dictionary={}, html=True):
    html_txt = ''
    if obj is not None:
        for prop in dir(obj):
            prop_type = eval("type(obj.{0})".format(prop))
            txt = "( {0} ) {1}".format(prop_type, prop).replace("<class '", '').replace("'>", '')
            if html is True:
                html_txt += "<p>{0}</p>".format(txt)
            elif dictionary is None:
                print(txt)
            else:
                dictionary[prop] = txt
    if html is True:
        return html_txt
    return dictionary
