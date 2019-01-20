from selenium.webdriver import Chrome, ChromeOptions
from os.path import dirname, abspath, join
import string
from string import ascii_letters, printable
import json

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

def get_sobrenomes():
    driver = init_chrome_driver(False, False, "http://www.tiltedlogic.org/Familia/surnames-all.php?tree=")
    sobrenomes = {}
    tds = driver.find_elements_by_class_name("sncol")
    for td in tds:
        children = td.get_property("children")
        index = 1
        snomes = []
        for element in children:
            if element.get_property("tagName") == "A":
                # print("{0}, {1}".format(element.get_property("innerText"), element.get_attribute("innerText")))
                txt = element.get_property("innerText")
                # print("({1})txt = {0}".format(txt, type(txt)))
                snomes.append(txt)
        sobrenomes["sobrenomes{0}".format(index)] = snomes
        index+=1
    driver.quit()
    sobrenome_json = json.dumps(sobrenomes)
    print(sobrenome_json)


def check_word(word):
    if type(word) == str:
        for letter in word:
            if ascii_letters.find(letter) == -1:
                return False
                break
        return True
    else:
        raise TypeError("Must be an string type.")


if __name__ == "__main__":
    get_sobrenomes()
    print(ascii_letters)
    print(printable)