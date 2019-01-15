import os
import time
from django.http import HttpResponse
from os.path import dirname, abspath, join
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime

#Global Variables
base_dir_path = dirname(dirname(dirname(abspath(__file__))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")
password = 'R$&fakeemail95'
f_name = "Anonymous"
l_name ="Fakeson"
#end of global variables

relative_chromedriver_path = "./../../chromedriver_linux64/chromedriver"


def init_chrome_driver(headless=False):

    global chromedriver_path
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("---headless")
    driver = Chrome(executable_path=chromedriver_path,options=chrome_options)
    return driver


def create_outlook_email(request):

    global password
    global f_name
    global l_name
    driver = init_chrome_driver()
    driver.get("https://outlook.live.com/owa/?nlp=1&signup=1")

    #start login
    login_name_input = driver.find_element_by_id("MemberName")
    login_name_input.send_keys("justafakemembername")
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(3)
    #end login

    #start password
    pwd_input = driver.find_element_by_id("PasswordInput")
    pwd_input.send_keys(password)
    check_box_input = driver.find_element_by_id("iOptinEmail")
    check_box_input.click()
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(1)
    #end password

    #user's information
    first_name = driver.find_element_by_id("FirstName")
    first_name.send_keys(f_name)
    last_name = driver.find_element_by_id("LastName")
    last_name.send_keys(l_name)
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(1)
    #end of user's information

    #start add details
    country_input = driver.find_element_by_id("Country")
    country_options = country_input.get_property("options")
    country_input.send_keys("US")
    month_input = driver.find_element_by_id("BirthMonth")
    print("before::month_input.value = {0}".format(month_input.get_property("value")))
    month_input.send_keys("5")
    print("after::month_input.value = {0}".format(month_input.get_property("value")))
    print("after::month_input.value = {0}".format(month_input.get_attribute("value")))
    actions = ActionChains(driver)
    actions.move_to_element(month_input)
    actions.perform()
    time.sleep(3)
    actions.click(month_input)
    actions.perform()
    time.sleep(1)
    actions.key_down(Keys.ARROW_DOWN, month_input)
    actions.perform()
    time.sleep(1)
    actions.key_down(Keys.ARROW_DOWN, month_input)
    actions.perform()
    print("done 1 ")
    time.sleep(3)
    actions.context_click(month_input)
    print("done 2 ")
    time.sleep(3)
    actions.double_click(month_input)
    print("done 3 ")
    time.sleep(3)

    print("2 - after::month_input.value = {0}".format(month_input.get_property("value")))
    print("2 - after::month_input.value = {0}".format(month_input.get_attribute("value")))
    day_input = driver.find_element_by_id("BirthDay")
    day_input.send_keys("17")
    year_input = driver.find_element_by_id("BirthYear")
    year_input.send_keys("1999")
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(3)
    #end add details

    #start the image processing
    elems = driver.find_elements_by_class_name("text-body")
    print(len(elems))
    img = None
    time.sleep(10)
    for elem in elems:
        print(elem)
        print(elem.get_property("tagName"))
        if elem.get_property("tagName") == "IMG":
            img = elem
    if img != None:
        print("we found it: ")
        print(img.get_property("src"))
    else:
        print("there is no img... :(")
    time.sleep(10)
    #end the image processing
    time.sleep(1)
    driver.quit()

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

        #finish section
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
            count+=1
            if elem.get_attribute("innerText").find("Free") != -1:
                div = elem
    if div == None:
        raise Exception("Não foi possível achar o botão de free account.")
    else:
        try:
            file = open("./tutanota_script.js","r")
            script = ""
            for line in file.readlines():
                script+="\n"+line
            print("script: \n {0}".format(script))
            if script != "":
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
        except Exception as err:
            print("Aconteceu um erro:")
            print(err)
            print("------------Fim do Erro-----------------")

    # driver.execute_script("window.alert('I think we found it')")
    time.sleep(10)
    driver.quit()


if __name__ == "__main__":
    # print("Just a Test")
    # proton_username = "mariasilvarse"
    # password = "rsefakeemail95"
    # verf_email = "rafael.eusebio95@gmail.com"
    # create_proton_mail_account(None, proton_username, password, verf_email)
    create_tutanota_email_account(None, "mariasilvarse", "rsefakeemail95")
