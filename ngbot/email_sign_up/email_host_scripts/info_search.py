from selenium.webdriver import Chrome, ChromeOptions
from os.path import dirname, abspath, join
import string
from string import ascii_letters, printable
import json

base_dir_path = dirname(dirname(dirname(dirname(abspath(__file__)))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")


not_ascii = {'Á': 'A', 'í': 'i', 'ç': 'c', 'ã': 'a', 'õ': 'o', '’': '', 'ó': 'o', 'á': 'a', 'ê': 'e', 'ü': 'u', '-': ''}

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
        print(json.dumps(sobrenomes["sobrenomes{0}".format(index)]))
        index+=1
    driver.quit()
    sobrenome_json = json.dumps(sobrenomes)
    print(sobrenome_json)

def get_sobrenomes2():
    driver = init_chrome_driver(False, False, "https://nomestop.com/sobrenomes-brasileiros/")
    paragraphs = driver.find_elements_by_tag_name("p")
    sobrenomes = []
    for p in paragraphs:
        text = p.get_property("innerText")
        if text.count(" ") <= 1 and text != "":
            sobrenomes.append(text)
    print("quantidade: {0}".format(len(sobrenomes)))
    print(sobrenomes)
    not_ascii = []
    for sb in sobrenomes:
        if not is_ascii(sb):
            not_ascii.append(sb)
    print("quantidade: {0}".format(len(not_ascii)))
    print(not_ascii)
    return sobrenomes, not_ascii


def is_ascii(word):
    if type(word) == str:
        for letter in word:
            if ascii_letters.find(letter) == -1 and letter != " ":
                return False
                break
        return True
    else:
        raise TypeError("Must be an string type.")


def not_ascii_dict(word, dictionary):
    if type(word) == str and type(dictionary) == dict:
        for letter in word:
            if ascii_letters.find(letter) == -1 and letter != " ":
                dictionary[letter] = "placeholder"
    else:
        raise TypeError("Must be an string type.")

def make_not_ascii_dict(word_list):
    not_ascii = {}
    for word in word_list:
        not_ascii_dict(word, not_ascii)
    print(not_ascii)

def make_word_ascii(word):
    if type(word) == str:
        not_ascii = {'Á': 'A',
                     'í': 'i',
                     'ç': 'c',
                     'ã': 'a',
                     'õ': 'o',
                     '’': '_',
                     'ó': 'o',
                     'á': 'a',
                     'ê': 'e',
                     'ü': 'u',
                     '-': '_'}
        for index in range(len(word)):
            letter = word[index]
            check = is_ascii(letter)
            if not check:
                if letter in not_ascii.keys():
                    word = word[0:index] + not_ascii[letter] + word[index+1:len(word)]
                else:
                    word = word[0:index] + '_' + word[index + 1:len(word)]





if __name__ == "__main__":
    # get_sobrenomes()
    # print(ascii_letters)
    # print(printable)
    sobrenomes, not_ascii = get_sobrenomes2()
