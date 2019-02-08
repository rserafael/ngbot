import time
from os.path import dirname, abspath, join
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import json
import random
import sys

_directory_ = dirname(abspath(__file__))
_maindir_ = dirname(_directory_)

sys.path.append(_directory_)
from tools import init_chrome_driver

br_males_json_path = join(_directory_, 'names_collection/br_males.json')
br_females_json_path = join(_directory_, 'names_collection/br_females.json')
us_males_json_path = join(_directory_, 'names_collection/us_males.json')
us_females_json_path = join(_directory_, 'names_collection/us_females.json')


class OutLook(object):

    def __init__(self, email_address, first_name, last_name, password):
        raise Exception("")

    def create_email(first_name, last_name, permutation=1, additional="ng", number=10):
        first_name = first_name.lower().replace(" ", '')
        last_name = last_name.lower().replace(" ", '')
        additional = additional.lower().replace(" ", '')
        email_address = None
        if permutation == 1:
            email_address = "{0}.{1}.{2}{3}".format(first_name, last_name, additional, number)
        elif permutation == 2:
            email_address = "{0}.{1}.{2}{3}".format(first_name, additional, last_name, number)
        elif permutation == 3:
            email_address = "{0}.{1}.{2}{3}".format(last_name, first_name, additional, number)
        elif permutation == 4:
            email_address = "{0}.{1}.{2}{3}".format(last_name, additional, first_name, number)
        elif permutation == 5:
            email_address = "{0}.{1}.{2}{3}".format(additional, first_name, last_name, number)
        elif permutation == 6:
            email_address = "{0}.{1}.{2}{3}".format(additional, last_name, first_name, number)
        else:
            return OutLook.create_email(first_name, last_name, permutation=1, additional="ng", number=171)
        return email_address

    def click_next_button(driver, sleep_interval):
        try:
            next_button = driver.find_element_by_id("iSignupAction")
            next_button.click()
            time.sleep(sleep_interval)
            return True
        except NoSuchElementException as NoElement:
            print("Não encontramos Next Button.")
            return False

    def insert_address(driver, email_address, sleep_interval, permutation=2):
        try:
            page_title = driver.find_element_by_id("CredentialsPageTitle")
            if page_title.get_property("innerText").find("Create account") != -1:
                address_input = driver.find_element_by_id("MemberName")
                address_input.send_keys(email_address)
                time.sleep(sleep_interval)
                if OutLook.click_next_button(driver, 2):
                    return True
                else:
                    try:
                        alert_msg = driver.find_element_by_id("MemberNameError")
                        print("insert_address: alert_msg = {0}".format(alert_msg.get_property("innerText")))
                        return OutLook.click_next_button(driver, sleep_interval)
                    except NoSuchElementException as NoElement:
                        return OutLook.click_next_button(driver, sleep_interval)
                    except Exception as error:
                        raise error
            else:
                print("You are not at address insertion step.")
                return False

        except Exception as error:
            print("insert_address: Type: {0}".format(type(error)))
            print(error)
            print("-------------------------")
            return False

    def insert_password(driver, password, sleep_interval):
        try:
            page_title = driver.find_element_by_id("PasswordTitle")
            if page_title.get_property("innerText").find("Create a password") != -1:
                pwd_input = driver.find_element_by_id("PasswordInput")
                pwd_input.send_keys(password)
                time.sleep(sleep_interval)

                check_box_input = driver.find_element_by_id("iOptinEmail")
                if not check_box_input.get_property("checked"):
                    check_box_input.click()
                    time.sleep(sleep_interval)

                if OutLook.click_next_button(driver, sleep_interval):
                    return True
                else:
                    try:
                        pwd_error = driver.find_element_by_id("PasswordError")
                        print("Password Error Alert: {0}".format(pwd_error.get_property("innerText")))
                        return False
                    except NoSuchElementException as NoElement:
                        return OutLook.click_next_button(driver)
                    except Exception as error:
                        raise error
        except Exception as error:
            print("insert_password: Type: {0}".format(type(error)))
            print(error)
            print("--------------------------")
            return False

    def insert_personal_info(driver, first_name, last_name, sleep_interval):
        try:
            page_title = driver.find_element_by_id("iPageTitle")
            if page_title.get_property("innerText").find("Create account") != -1:
                first_name_input = driver.find_element_by_id("FirstName")
                first_name_input.send_keys(first_name)
                time.sleep(sleep_interval)

                last_name_input = driver.find_element_by_id("LastName")
                last_name_input.send_keys(last_name)
                time.sleep(sleep_interval)

                if OutLook.click_next_button(driver, 2):
                    return True
                else:
                    try:
                        alert_error = driver.find_elements_by_class_name("alert-error")
                        count = 0
                        for error in alert_error:
                            count += 1
                            print("{0} - erro: {1}".format(count, error.get_property("innerText")))
                        return False
                    except Exception as error:
                        raise error

        except Exception as error:
            print("insert_personal_info: Type: {0}".format(type(error)))
            print(error)
            print("-----------------")
            return False

    def select_month(driver, month_input, month):
        try:
            actions = ActionChains(driver)
            actions.move_to_element(month_input)
            actions.perform()
            time.sleep(0.1)
            actions.click(month_input)
            actions.perform()
            time.sleep(0.1)
            for i in range(month):
                actions.key_down(Keys.ARROW_DOWN, month_input)
            actions.perform()
            time.sleep(1.5)
            return True
        except Exception as error:
            print("select_month: Type: {0}".format(type(error)))
            print(error)
            print("-----------------")
            return False

    def insert_more_personal_info(driver, country="Brazil", month=4, day=1, year=2001, sleep_interval=0.7):
        try:
            page_title = driver.find_element_by_id("iPageTitle")
            if page_title.get_property("innerText").find("Add details") != -1:
                country_input = driver.find_element_by_id("Country")
                country_input.send_keys(country)
                time.sleep(sleep_interval)

                month_input = driver.find_element_by_id("BirthMonth")
                if OutLook.select_month(driver, month_input, month):
                    day_input = driver.find_element_by_id("BirthDay")
                    day_input.send_keys(day)
                    time.sleep(sleep_interval)

                    year_input = driver.find_element_by_id("BirthYear")
                    year_input.send_keys(year)
                    time.sleep(sleep_interval)

                    return OutLook.click_next_button(driver, 1)
                else:
                    return False

        except Exception as error:
            print("insert_more_personal_info: Type: {0}".format(type(error)))
            print(error)
            print("-----------------")
            return False

    def image_processing(driver):
        try:
            start_time = datetime.now()
            imgs = driver.find_elements_by_tag_name("img")
            while True:
                for img in imgs:
                    if img.get_attribute("alt").find("Visual Challenge") != -1:
                        return True, img.get_attribute("src")
                        break
                    else:
                        time.sleep(0.5)
                        imgs = driver.find_elements_by_tag_name("img")
                delta_time = datetime.now() - start_time
                if delta_time.total_seconds() > 100:
                    return False, None
        except Exception as error:
            print("image_processing: Type: {0}".format(type(error)))
            print(error)
            print("-----------------")
            return False

    def create_new_account(driver, email_address, password, first_name, last_name, country, day, month, year):
        start_time = datetime.now()
        sleep_interval = 0.2
        if OutLook.insert_address(driver, email_address, sleep_interval=1):
            if OutLook.insert_password(driver, password, sleep_interval=1):
                if OutLook.insert_personal_info(driver, first_name, last_name, sleep_interval=1):
                    if OutLook.insert_more_personal_info(driver, country=country, month=month, day=day, year=year,
                                                         sleep_interval=0.7):
                        time.sleep(5)
                        result, img_url = OutLook.image_processing(driver)
                        if result:
                            print("time spent = {0}".format(datetime.now() - start_time))
                            return True, img_url, driver
                        else:
                            print("time spent = {0}".format(datetime.now() - start_time))
                            return False, "Erro no image_processing", None
                    else:
                        print("time spent = {0}".format(datetime.now() - start_time))
                        return False, "Erro no insert_more_personal_info", None
                else:
                    print("time spent = {0}".format(datetime.now() - start_time))
                    return False, "Erro no insert_personal_info", None
            else:
                print("time spent = {0}".format(datetime.now() - start_time))
                return False, "Erro no insert_password", None
        else:
            print("time spent = {0}".format(datetime.now() - start_time))
            return False, "Erro no insert_address", None

    def insert_verification_text(driver, verf_text=''):
        inputs = driver.find_elements_by_tag_name("input")
        print("numbers of inputs: {0}".format(len(inputs)))
        for input in inputs:
            id = input.get_attribute("id")
            if id.find("Solution"):
                print("we found it")
                input.send_keys(verf_text)
                OutLook.click_next_button(driver, 2)
                time.sleep(5)
                finalization = OutLook.finilize_account_creation(driver)
                return finalization
            else:
                print("OutLook: insert_verification_text: id not found: {0}".format(id))
                return False
        return False

    def next_btn_after_creation(driver):
        try:
            next_btns = driver.find_elements_by_class_name("nextButton")
            if next_btns is None or len(next_btns) < 1:
                return False
            if len(next_btns) == 1:
                next_btns[0].click()
                time.sleep(3)
                return True
            else:
                for btn in next_btns:
                    if btn.get_property("tagName").find("BUTTON") != -1:
                        btn.click()
                time.sleep(3)
                return True
        except Exception as err:
            print("Outlook: next_btn_after_creation: error type: {0}".format(type(err)))
            return False

    def click_get_started_btn(driver):
        btns = driver.find_elements_by_class_name("primaryButton")
        if btns is None or len(btns) < 1:
            print("OutLook: get_started_btn: btns is None or empty")
            return False
        if len(btns) == 1:
            primary_btn = btns[0]
            primary_btn.click()
            return True
        else:
            for btn in btns:
                if btn.get_property("innerText").find("Get Started") != -1:
                    btn.click()
                    return True
        print("OutLook: get_started_btn: primary button not found")
        return False

    def finilize_account_creation(driver):
        count = 0
        while count < 4:
            count += 1
            ended = OutLook.click_get_started_btn(driver)
            if ended:
                return True
            nxt_btn = OutLook.next_btn_after_creation(driver)
            if not nxt_btn:
                return False
        print("Outlook: finilize_account_creation: count exceeded: {0}".format(count))
        return False

    def create_random_person(sex='', country='', password='R$&contafalsa95'):
        driver = init_chrome_driver(False, True, "https://outlook.live.com/owa/?nlp=1&signup=1")
        names_json_path = Account.get_person_json(sex, country)
        names_json = json.load(open(names_json_path, "r"))
        rand_key = Account.get_a_random_key(list(names_json.keys()))
        person = names_json[rand_key]
        print("person: ")
        print(person)
        email = OutLook.create_email(person['name'], person['lastname'],
                                     number=random.choice([person['day'], person['month'], person['year']]))
        result, img_url, driver = OutLook.create_new_account(driver, email, password, person['name'],
                                                             person['lastname'], person['country'], person['day'],
                                                             person['month'], person['year'])
        if result:
            person['email'] = email
            person['password'] = password + "@outlook.com"
            return result, img_url, driver, person
        else:
            print("create_random_person: ")
            print(img_url)
            return result, None, None, None


class Account(object):
    def __init__(self):
        raise NotImplementedError("This Class is an static class.")

    def get_a_random_key(keys):
        key = random.choice(keys)
        return key

    def get_person_json(sex="", country=''):

        global us_females_json_path, us_males_json_path, br_females_json_path, br_males_json_path
        json_paths = [us_females_json_path, us_males_json_path, br_females_json_path, br_males_json_path]
        if sex == 'F':
            if country == "BR":
                return br_females_json_path
            elif country == "US":
                return us_females_json_path
            else:
                return random.choice(json_paths)
        elif sex == 'M':
            if country == "BR":
                return br_males_json_path
            elif country == "US":
                return us_males_json_path
            else:
                return random.choice(json_paths)
        else:
            return random.choice(json_paths)
