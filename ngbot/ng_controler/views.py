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

def create_account(request, email, full_name, username, password):

    writing_time = 0.8

    driver = init_chrome_driver(False)
    driver.get("https://www.instagram.com/")
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

    btns = driver.find_elements_by_tag_name("button")
    sign_up_btn = None
    for btn in btns:
        if btn.get_property("innerText").find("Sign up") != -1:
            sign_up_btn = btn
            break
    if sign_up_btn != None:
        retry_sign_up(driver, sign_up_btn, uname)
    else:
        print("Não encontramos o Sign Up Button")



if __name__ == "__main__":
    # global email, full_name, username, password

    create_account(None, email, full_name, username, password)
