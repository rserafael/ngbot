from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from os.path import dirname, abspath, join
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from http import client
import sys
import random
import threading
import os
import time

common_base = dirname(abspath(__file__))
script_base = join(common_base, 'email_host_scripts')
sys.path.append(script_base)


def create_proton_mail_account(request, username, password, verf_email):
    sign_up_link = "https://mail.protonmail.com/create/new?language=en"
    driver = init_chrome_driver(False)
    driver.get(sign_up_link)

    # Sending username
    username_element = driver.find_element_by_id("username")
    username_element.send_keys(username)

    password_element = driver.find_element_by_id("password")
    password_element.send_keys(password)

    passwordc_element = driver.find_element_by_id("passwordc")
    passwordc_element.send_keys(password)

    button = driver.find_element_by_class_name("signUpProcess-btn-create")
    button.click()
    time.sleep(1.1)

    try:
        confirm_button = driver.find_element_by_id("confirmModalBtn")
        confirm_button.click()
        time.sleep(1.1)

        verf_email_input = driver.find_element_by_class_name("codeVerificator-email-input")
        verf_email_input.send_keys(verf_email)
        verf_email_input.submit()

        # finish section
        finish_btn = driver.find_element_by_id("")

    except Exception as err:
        print("An error has occurred")
        print(err)
        time.sleep(100)
        driver.quit()
    time.sleep(100)
    # driver.quit()


def create_tutanota_email_account(request, username, password):
    driver = init_chrome_driver(False)
    driver.get("https://mail.tutanota.com/signup")

    # Achar o botão de Free Account
    elements = []
    t1 = datetime.now()
    div = None
    while len(elements) == 0 and (datetime.now() - t1).seconds < 120:
        elements = driver.find_elements_by_class_name("dialog-header")
        count = 0
        for elem in elements:
            count += 1
            if elem.get_attribute("innerText").find("Free") != -1:
                div = elem
    if div == None:
        raise Exception("Não foi possível achar o botão de free account.")
    else:
        try:
            file = open("./tutanota_script.js", "r")
            script = ""
            for line in file.readlines():
                script += "\n" + line
            # print("script: \n {0}".format(script))
            if script != "":
                time.sleep(2)
                driver.execute_script(script)
                if len(driver.find_elements_by_class_name("dialog-header")) <= 1:
                    inputs = driver.find_elements_by_tag_name("input")[0:5]
                    for index in range(len(inputs)):
                        if index == 0:
                            inputs[index].send_keys(username)
                        elif index == 1 or index == 2:
                            inputs[index].send_keys(password)
                        elif index == 3 or index == 4:
                            inputs[index].click()
                        else:
                            print("Index exceeds number of options")
                    btns = driver.find_elements_by_tag_name("button")
                    time.sleep(5)
                    for btn in btns:
                        if btn.get_property("title").find("Next") != -1:
                            btn.click()
                            break
                    time.sleep(5)
                    imgs = driver.find_elements_by_tag_name("img")
                    imgs_source = imgs[0].get_property("src")
                    print("image source: {0}".format(imgs_source))
                    if imgs_source != None:
                        conn = client.HTTPConnection("localhost", 8083)
                        conn.request("GET", imgs_source)
                        response = conn.getresponse()
                        print("response = {0}".format(response.read()))
                else:
                    print("length of 'dialog-header' elements = {0}".format(
                        len(driver.find_elements_by_class_name("dialog-header"))))
                    try:
                        driver.switch_to.alert.accept()
                        # driver.switch_to.
                    except Exception as err:
                        print("Erro aqui: ")
                        print(err)

        except Exception as err:
            print("Aconteceu um erro:")
            print(err)
            print("------------Fim do Erro-----------------")

    # driver.execute_script("window.alert('I think we found it')")
    # time.sleep(10)
    # driver.quit()
    time.sleep(10000)


def showObj(obj, name):
    print("---------{0}---------".format(name))
    for prop in dir(obj):
        value = eval("obj.{0}".format(prop))
        prop_type = str(type(value)).replace("class ", "").replace('<', '').replace(">", '')
        print("({0}) {1}".format(prop_type, prop))
    print("---------{0}---------".format(name))


def get_verification_image(request, img_url=None):
    if img_url == None:
        return HttpResponse('<div><h1>Erro: Image não encontrada!</h1></div>')
    else:
        print("img_url = {0}".format(img_url))
        return HttpResponse(
            "<div><img src={0} alt='verification image'/><input type='{1}' width=50/></div>".format(img_url, 'text'))


def start_driver_activity(session, img_key):
    try:
        from outlook import OutLook
        print("Importação bem sucedida.")
        var1, var2 = OutLook.create_rand_us_female_account()
        if var1 != False:
            img_url = var1
            driver = var2
            session[img_key] = img_url
            time.sleep(100)
            driver.quit()
        else:
            print("deu merda...")
    except RuntimeError as rerror:
        print("at RuntimeError: {0}".format(type(rerror)))
        print(rerror)
        print("--------------------------------")
    except BaseException as error:
        print("at BaseException: {0}".format(type(error)))
        print(error)
        print("--------------------------------")


def create_outlook_email(request):
    if request.method == "GET":
        img_key = 'driver123'
        a = threading.Thread(target=start_driver_activity, name="Driver_Thread", daemon=True,
                             kwargs={'session': request.session,
                                     'img_key': 'driver123'})
        a.start()
        time.sleep(20)
        return redirect(
            "http://localhost:8000/createemail/getverificationimage/{0}".format(img_key))
    else:
        return HttpResponse("Method Tried = {0}.\nMethod Allowed = GET".format(request.method))
