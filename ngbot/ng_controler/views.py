from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from os.path import dirname, abspath, join

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


def create_account(request, email, full_name, username, password):

    driver = init_chrome_driver(False)
    driver.get("https://www.instagram.com/")

    email = driver.find_element_by_name("emailOrPhone")
    email.send_keys(email)

    real_name = driver.find_element_by_name("fullName")

    user_name = driver.find_element_by_name("username")

    driver.find_element_by_name()

