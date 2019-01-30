import time
from os.path import dirname, abspath, join
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import json
import random

base_dir_path = dirname(dirname(dirname(dirname(abspath(__file__)))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")
common_path = dirname(dirname(abspath(__file__)))
names_collection_path = join(common_path, "names_collection")


def init_chrome_driver(headless=False, incognito=False, url=""):
    global chromedriver_path
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("---headless")
    if incognito:
        chrome_options.add_argument("--incognito")
    print("chromedriver_path = {0}".format(chromedriver_path))
    driver = Chrome(executable_path=chromedriver_path, options=chrome_options)
    if url != "" and url != None and type(url) == str:
        driver.get(url)
    print("Chrome driver inicializado.")
    return driver


class OutLook(object):

    def __init__(self, email_address, first_name, last_name, password):
        raise Exception("")

    def create_email(first_name, last_name, permutation=1, additional="ng", number=10):
        first_name = first_name.lower()
        last_name = last_name.lower()
        additional = additional.lower()
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
                if delta_time.total_seconds() > 30:
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
                            return False, "Erro no image_processing"
                    else:
                        print("time spent = {0}".format(datetime.now() - start_time))
                        return False, "Erro no insert_more_personal_info"
                else:
                    print("time spent = {0}".format(datetime.now() - start_time))
                    return False, "Erro no insert_personal_info"
            else:
                print("time spent = {0}".format(datetime.now() - start_time))
                return False, "Erro no insert_password"
        else:
            print("time spent = {0}".format(datetime.now() - start_time))
            return False, "Erro no insert_address"

    def create_rand_us_female_account(self=None):
        # Talvez deva ser uma nova classe:
        password = "R$&fakeemail95"
        us_female_json = join(dirname(dirname(abspath(__file__))), 'names_collection/us_females.json')
        print(us_female_json)
        us_females = json.load(open(us_female_json, "r"))
        keys = []
        for n in us_females.keys():
            keys.append(n)
        choice = random.choice(keys)
        female = us_females[choice]
        # Uma classe estática que se chama Persons
        print(female)
        driver = init_chrome_driver(False, False, "https://outlook.live.com/owa/?nlp=1&signup=1")
        result, var1, var2 = OutLook.create_new_account(driver,
                                            OutLook.create_email(
                                                female['name'],
                                                female['lastname'],
                                                number=random.choice(
                                                    [female['day'], female['month'], female['year']])),
                                            password,
                                            female['name'],
                                            female['lastname'],
                                            female['country'], female['day'],
                                            female['month'], female['year'])
        if result:
            return var1, var2
        else:
            return False, var1

    def insert_verification_text(driver, verf_text=''):
        inputs = driver.find_elements_by_tag_name("input")
        print("numbers of inputs: {0}".format(len(inputs)))
        for input in inputs:
            id = input.get_attribute("id")
            if id.find("Solution"):
                print("we found it")
                input.send_keys(verf_text)
                OutLook.click_next_button(driver, 2)
                return True
            else:
                print("not yet: {0}".format(id))
                return False
        return False

if __name__ == "__main__":
    img_url, current_url = OutLook.create_rand_us_female_account()
    if img_url != False:
        print("Success")
        print(img_url)
    else:
        print("Failure")
