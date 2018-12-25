import os
import time
from django.shortcuts import render
from django.http import HttpResponse
from os.path import dirname as name_of_directory
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#Global Variables
chrome_relative_path = "chromedriver_linux64/chromedriver"
password = 'R$&fakeemail95'
f_name = "Anonymous"
l_name ="Fakeson"
#end of global variables


def init_chrome_driver():

    global chrome_relative_path
    chrome_driver_path = name_of_directory(name_of_directory(name_of_directory(__file__)))

    print("chrome_driver_path  = {0}".format(chrome_driver_path))
    chrome_driver_path = os.path.join(chrome_driver_path, chrome_relative_path)
    print("chrome_driver_path  = {0}".format(chrome_driver_path))
    driver = webdriver.Chrome(chrome_driver_path)
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

if __name__ == "__main__":
    print("it is working")
    create_outlook_email(None)
