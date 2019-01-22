import time
from os.path import dirname, abspath, join
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

base_dir_path = dirname(dirname(dirname(dirname(abspath(__file__)))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")


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
                        driver = Chrome()
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
            imgs = driver.find_elements_by_tag_name("img")
            src_list = []
            for img in imgs:
                src_list.append(img.get_attribute("src"))
            print(src_list)
            return True
            # if len(imgs) == 2:
            #     img = imgs[1]
            #     print("src = {0}".format(img.get_attribute("src")))
            #     return True
            # else:
            #     print("quantidade de elementos img = {0}".format(len(imgs)))
            #     return False
        except Exception as error:
            print("image_processing: Type: {0}".format(type(error)))
            print(error)
            print("-----------------")
            return False


    def create_new_account(driver, email_address, password, first_name, last_name):
        start_time = datetime.now()
        sleep_interval = 0.2
        if OutLook.insert_address(driver, email_address, sleep_interval=1):
            if OutLook.insert_password(driver, password, sleep_interval=1):
                if OutLook.insert_personal_info(driver, first_name, last_name, sleep_interval):
                    if OutLook.insert_more_personal_info(driver, country="Brazil", month=4, day=1, year=2001,
                                                         sleep_interval=0.7):
                        if OutLook.image_processing(driver):
                            print("Success")
                            print("time spent = {0}".format(datetime.now() - start_time))
                            return True
        print("Failure")
        print("time spent = {0}".format(datetime.now() - start_time))
        return False


def create_outlook_email(request, f_name, l_name, password):
    sleep_time = 3
    # global password
    # global f_name
    # global l_name
    driver = init_chrome_driver()
    driver.get("https://outlook.live.com/owa/?nlp=1&signup=1")

    # start login
    login_name_input = driver.find_element_by_id("MemberName")
    login_name_input.send_keys("justafakemembername")
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(sleep_time)
    # end login

    # start password
    pwd_input = driver.find_element_by_id("PasswordInput")
    pwd_input.send_keys(password)
    check_box_input = driver.find_element_by_id("iOptinEmail")
    check_box_input.click()
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(sleep_time)
    # end password

    # user's information
    first_name = driver.find_element_by_id("FirstName")
    first_name.send_keys(f_name)
    last_name = driver.find_element_by_id("LastName")
    last_name.send_keys(l_name)
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(sleep_time)
    # end of user's information

    # start add details
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
    time.sleep(0.1)
    actions.click(month_input)
    actions.perform()
    time.sleep(0.1)
    actions.key_down(Keys.ARROW_DOWN, month_input)
    actions.perform()
    time.sleep(0.1)
    actions.key_down(Keys.ARROW_DOWN, month_input)
    actions.perform()
    print("done 1 ")
    time.sleep(0.1)
    actions.context_click(month_input)
    print("done 2 ")
    time.sleep(0.1)
    actions.double_click(month_input)
    print("done 3 ")
    time.sleep(0.1)
    print("2 - after::month_input.value = {0}".format(month_input.get_property("value")))
    print("2 - after::month_input.value = {0}".format(month_input.get_attribute("value")))
    day_input = driver.find_element_by_id("BirthDay")
    day_input.send_keys("17")
    year_input = driver.find_element_by_id("BirthYear")
    year_input.send_keys("1999")
    next_button = driver.find_element_by_id("iSignupAction")
    next_button.click()
    time.sleep(sleep_time)
    # end add details

    # Manual Image Processing


if __name__ == "__main__":
    driver = init_chrome_driver(False, False, "https://outlook.live.com/owa/?nlp=1&signup=1")
    password = "R$&fakeemail95"
    first_name = 'Maria'
    last_name = "Rosario"
    country = "Brazil",
    month = 4
    day = 1
    year = '2001'
    email_address = OutLook.create_email(first_name, last_name, year)
    OutLook.create_new_account(driver, email_address, password, first_name, last_name)
