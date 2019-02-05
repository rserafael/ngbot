import time
import sys
import random
from os.path import dirname, join, abspath

_directory_ = dirname(abspath(__file__))
sys.path.append(_directory_)
from tools import init_chrome_driver
from selenium.webdriver.common.action_chains import ActionChains


class Instagram(object):
    def __init__(self):
        raise NotImplementedError("This is a static class. Should not be instantiated.")

    def create_username(person):
        dates = [person.day, person.year, person.month]
        username = "{0}{1}{2}".format(person.lastname.replace(" ", ''), person.firstname.replace(" ", ''),
                                       random.choice(dates))
        return username.lower()

    def try_refresh(error_input):
        # from selenium.webdriver.remote.webelement import WebElement
        # w = WebElement()
        parent = error_input.get_property("parentElement")
        if parent:
            print("parent: {0}".format(parent))
            children = parent.get_property("children")
            if children:
                print("children: {0}".format(children))
                for element in children:
                    if element != error_input:
                        element.click()
                        element.click()

    def check_correctness(driver):
        error_inputs = driver.find_elements_by_class_name("coreSpriteInputError")
        print("Erros: {0}".format(len(error_inputs)))
        accepted_elements = driver.find_elements_by_class_name("coreSpriteInputAccepted")
        print("Accepted: {0}".format(len(accepted_elements)))
        if len(accepted_elements) == 4 and len(error_inputs) == 0:
            return True, None
        else:
            return False, error_inputs

    def refresh_factor(error_inputs):
        if len(error_inputs) > 0:
            for element in error_inputs:
                Instagram.try_refresh(element)

    def sign_up(driver):
        from selenium.webdriver import Chrome
        driver = Chrome
        buttons = driver.find_elements_by_tag_name("button")
        btn = None
        for button in buttons:
            if button.get_property("innerText").find("Sign up") != -1:
                btn = button
                break
        if btn != None:
            btn.click()
            return True
        else:
            return False

    def click_out(driver):
        elements = driver.find_elements_by_tag_name("h1")
        for el in elements:
            el.click()

    def account_creation(email, full_name, username, password):
        try:
            writing_time = 1

            driver = init_chrome_driver(True, True, "https://www.instagram.com/")
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

            root = driver.find_element_by_id("react-root")
            # ActionChains(driver).move_to_element(root).click().perform()
            Instagram.click_out(driver)
            time.sleep(3)

            tries = 1
            while True:
                result, prob_err = Instagram.check_correctness(driver)
                if result:
                    # result = Instagram.sign_up(driver)
                    if result:
                        driver.quit()
                        return True
                    else:
                        return False
                else:
                    if tries > 3:
                        return False
                    else:
                        Instagram.refresh_factor(prob_err)
                        Instagram.click_out(driver)
                        # ActionChains(driver).move_to_element(root).click().perform()
                        time.sleep(1)
                    print("Tries: {0}".format(tries))
                    tries += 1
        except Exception as err:
            print("Instagram.account_creation: {0}".format(type(err)))
            print(err)
            print("===============================")
            return False

    def create_account(person, verbose=False):
        person.username = Instagram.create_username(person)
        if verbose:
            print("username ({0}) created.".format(person.username))
        result = Instagram.account_creation(person.email, "{0} {1}".format(person.firstname, person.lastname),
                                            person.username, person.password)
        return result
