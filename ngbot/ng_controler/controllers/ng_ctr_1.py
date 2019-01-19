from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from os.path import dirname, abspath, join
import time

#Global Variables
base_dir_path = dirname(dirname(dirname(dirname(abspath(__file__)))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")
email = "justafakemembername@outlook.com"
password = 'R$&fakeinstagram95'
username = "maria.antonieta17"
start_point_url = "https://www.instagram.com/accounts/login/?source=auth_switcher"
writing_time = 0.7
#end of global variables

def init_chrome_driver(headless=False):

    global chromedriver_path
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("---headless")
    driver = Chrome(executable_path=chromedriver_path,options=chrome_options)
    return driver

def log_in(request, email, password ):
    driver = init_chrome_driver(False)
    driver.get(start_point_url)
    time.sleep(2)

    username_input = driver.find_element_by_name("username")
    username_input.send_keys(email)
    time.sleep(writing_time)

    pwd_input = driver.find_element_by_name("password")
    pwd_input.send_keys(password)
    time.sleep(writing_time)

    btns = driver.find_elements_by_tag_name("button")
    log_in_btn = None
    for btn in btns:
        if btn.get_property("innerText").find("Log in") != -1:
            log_in_btn = btn
            break
    if log_in_btn != None:
        log_in_btn.click()
    else:
        print("Não encontramos o log in button.")

    time.sleep(10000)

if __name__ == "__main__":
    email = "justafakemembername@outlook.com"
    password = 'R$&fakeinstagram95'
    log_in(None, email, password)