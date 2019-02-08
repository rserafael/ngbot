# ===== Global Variable =======
from os.path import dirname, abspath, join

_directory_ = dirname(abspath(__file__))
# ===============================

# ============== Imports =============
from django.http import HttpResponse, JsonResponse
import sys

# ===================================

# ============ Sys Path Appendments ============
_maindir_ = dirname(_directory_)
sys.path.append(join(_maindir_, 'utilities'))


# ==============================================

class Eternal(object):
    def __init__(self):
        self.kwargs = {}


ETERNAL = Eternal()
print("\n\nETERNAL HAS BEEN CREATED\n\n")


def set_verification_text(request, verification_text=None):
    if verification_text == None:
        return JsonResponse({'erro': True})
    else:
        ETERNAL.kwargs['verftext'] = verification_text
        try:
            from emailutils import OutLook
            result = OutLook.insert_verification_text(ETERNAL.kwargs['driver'], verification_text)
            if result:
                from .models import Person
                person = ETERNAL.kwargs['person']
                p = Person(firstname=person['name'],
                           lastname=person['lastname'],
                           country=person['country_symbol'],
                           sex=person['sex'],
                           email=person['email'] + "@outlook.com",
                           password=person['password'],
                           day=person['day'],
                           month=person['month'],
                           year=person['year'],
                           emailCreated=True,
                           ngCreated=False,
                           username="")
                p.save()
                print("\n--> Person created.\n")
                return JsonResponse({'erro': False})
            else:
                return JsonResponse({'erro': True})
        except Exception as err:
            print("ERRO: {0}".format(type(err)))
            print(err)
        return JsonResponse({'erro': True, })


def get_verification_text(request):
    if ETERNAL.kwargs.get("verftext") is not None:
        return JsonResponse({'ready': True, 'text': ETERNAL.kwargs['verftext']})
    else:
        return JsonResponse({"ready": False, 'reason': "ETERNAL.kwargs.get('verftext') is empty right now"})


def get_verification_image(request):
    if ETERNAL.kwargs.get("img_url") is None:
        return JsonResponse({'erro': True})
    else:
        return JsonResponse({'erro': False, 'src': ETERNAL.kwargs['img_url']})


def start_driver_activity(sex='', country=''):
    method_name = 'start_driver_activity'
    try:
        from emailutils import OutLook

        result, img_url, driver, person = OutLook.create_random_person(sex, country)
        if result != False:
            ETERNAL.kwargs['driver'] = driver
            ETERNAL.kwargs['img_url'] = img_url
            ETERNAL.kwargs['person'] = person
            return True
        else:
            print("{0}: deu merda...".format(method_name))
            return False
    except RuntimeError as rerror:
        print("{0}: at RuntimeError: {1}".format(method_name, type(rerror)))
        print(rerror)
        print("--------------------------------")
        return False
    except BaseException as error:
        print("{0}: at BaseException: {1}".format(method_name, type(error)))
        print(error)
        print("--------------------------------")
        return False


def create_outlook_email(request):
    method_name = "create_outlook_email"
    if request.method == "GET":
        result = start_driver_activity(sex=request.GET.get("sex"), country=request.GET.get('country'))
        if result:
            f = open(join(_maindir_, 'utilities/verification_image.html'), 'r')
            html_page = ''
            for line in f.readlines():
                html_page += line
            return HttpResponse(html_page)
        else:
            return HttpResponse("Some thing wrong has happend")
    else:
        return HttpResponse("Method Tried = {0}.\nMethod Allowed = GET".format(request.method))

# def create_proton_mail_account(request, username, password, verf_email):
#     sign_up_link = "https://mail.protonmail.com/create/new?language=en"
#     driver = init_chrome_driver(False)
#     driver.get(sign_up_link)
#
#     # Sending username
#     username_element = driver.find_element_by_id("username")
#     username_element.send_keys(username)
#
#     password_element = driver.find_element_by_id("password")
#     password_element.send_keys(password)
#
#     passwordc_element = driver.find_element_by_id("passwordc")
#     passwordc_element.send_keys(password)
#
#     button = driver.find_element_by_class_name("signUpProcess-btn-create")
#     button.click()
#     time.sleep(1.1)
#
#     try:
#         confirm_button = driver.find_element_by_id("confirmModalBtn")
#         confirm_button.click()
#         time.sleep(1.1)
#
#         verf_email_input = driver.find_element_by_class_name("codeVerificator-email-input")
#         verf_email_input.send_keys(verf_email)
#         verf_email_input.submit()
#
#         # finish section
#         finish_btn = driver.find_element_by_id("")
#
#     except Exception as err:
#         print("An error has occurred")
#         print(err)
#         time.sleep(100)
#         driver.quit()
#     time.sleep(100)
#     # driver.quit()


# def create_tutanota_email_account(request, username, password):
#     driver = init_chrome_driver(False)
#     driver.get("https://mail.tutanota.com/signup")
#
#     # Achar o botão de Free Account
#     elements = []
#     t1 = datetime.now()
#     div = None
#     while len(elements) == 0 and (datetime.now() - t1).seconds < 120:
#         elements = driver.find_elements_by_class_name("dialog-header")
#         count = 0
#         for elem in elements:
#             count += 1
#             if elem.get_attribute("innerText").find("Free") != -1:
#                 div = elem
#     if div == None:
#         raise Exception("Não foi possível achar o botão de free account.")
#     else:
#         try:
#             file = open("./tutanota_script.js", "r")
#             script = ""
#             for line in file.readlines():
#                 script += "\n" + line
#             # print("script: \n {0}".format(script))
#             if script != "":
#                 time.sleep(2)
#                 driver.execute_script(script)
#                 if len(driver.find_elements_by_class_name("dialog-header")) <= 1:
#                     inputs = driver.find_elements_by_tag_name("input")[0:5]
#                     for index in range(len(inputs)):
#                         if index == 0:
#                             inputs[index].send_keys(username)
#                         elif index == 1 or index == 2:
#                             inputs[index].send_keys(password)
#                         elif index == 3 or index == 4:
#                             inputs[index].click()
#                         else:
#                             print("Index exceeds number of options")
#                     btns = driver.find_elements_by_tag_name("button")
#                     time.sleep(5)
#                     for btn in btns:
#                         if btn.get_property("title").find("Next") != -1:
#                             btn.click()
#                             break
#                     time.sleep(5)
#                     imgs = driver.find_elements_by_tag_name("img")
#                     imgs_source = imgs[0].get_property("src")
#                     print("image source: {0}".format(imgs_source))
#                     if imgs_source != None:
#                         conn = client.HTTPConnection("localhost", 8083)
#                         conn.request("GET", imgs_source)
#                         response = conn.getresponse()
#                         print("response = {0}".format(response.read()))
#                 else:
#                     print("length of 'dialog-header' elements = {0}".format(
#                         len(driver.find_elements_by_class_name("dialog-header"))))
#                     try:
#                         driver.switch_to.alert.accept()
#                         # driver.switch_to.
#                     except Exception as err:
#                         print("Erro aqui: ")
#                         print(err)
#
#         except Exception as err:
#             print("Aconteceu um erro:")
#             print(err)
#             print("------------Fim do Erro-----------------")
#
#     # driver.execute_script("window.alert('I think we found it')")
#     # time.sleep(10)
#     # driver.quit()
#     time.sleep(10000)
