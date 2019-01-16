from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from os.path import dirname, abspath, join
import time

#Global Variables
base_dir_path = dirname(dirname(dirname(abspath(__file__))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")
email = "justafakemembername@outlook.com"
password = 'R$&fakeinstagram95'
full_name = "Maria Antonieta"
username = "maria.antonieta17"
#end of global variables

relative_chromedriver_path = "./../../chromedriver_linux64/chromedriver"


def init_chrome_driver(headless=False):

    global chromedriver_path
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("---headless")
    driver = Chrome(executable_path=chromedriver_path,options=chrome_options)
    return driver


def create_account(request, email, full_name, username, password):

    driver = init_chrome_driver(False)
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    email_element = driver.find_element_by_name("emailOrPhone")
    email_element.send_keys(email)

    fname = driver.find_element_by_name("fullName")
    fname.send_keys(full_name)

    uname = driver.find_element_by_name("username")
    uname.send_keys(username)

    pwd = driver.find_element_by_name("password")
    pwd.send_keys(password)

    # Achando o erro:

    erro = driver.find_elements_by_class_name("coreSpriteInputError")
    refresh = driver.find_elements_by_class_name("coreSpriteInputRefresh")

    if erro != None:
        print("Erro no Input")
        if len(erro) == 1:
            if refresh != None:
                if len(refresh) == 1:
                    refresh[0].get_property("parentElement").click()
                    time.sleep(0.5)
                    print("username = {0}".format(uname.get_property("value")))



    time.sleep(1000)

    btns = driver.find_elements_by_tag_name("button")
    sign_up_btn = None
    if len(btns) > 0:
        for btn in btns:
            if btn.get_property("innerText").find("Sign up") != -1:
                sign_up_btn = btn
                break
        if sign_up_btn != None:
            sign_up_btn.click()
        else:
            print("Não achamos o signup button")
    else:
        print("Não achamos nenhum button element")



if __name__ == "__main__":
    # global email, full_name, username, password

    create_account(None, email, full_name, username, password)
