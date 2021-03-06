from selenium.webdriver import Chrome, ChromeOptions
from os.path import dirname, abspath, join
import string
from string import ascii_letters, printable
import json
import os
import bcrypt

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
    # print("chromedriver_path = {0}".format(chromedriver_path))
    driver = Chrome(executable_path=chromedriver_path, options=chrome_options)
    if url != "" and url != None and type(url) == str:
        driver.get(url)
    print("Chrome driver inicializado.")
    return driver


# def get_sobrenomes():
#     driver = init_chrome_driver(False, False, "http://www.tiltedlogic.org/Familia/surnames-all.php?tree=")
#     sobrenomes = {}
#     tds = driver.find_elements_by_class_name("sncol")
#     for td in tds:
#         children = td.get_property("children")
#         index = 1
#         snomes = []
#         for element in children:
#             if element.get_property("tagName") == "A":
#                 # print("{0}, {1}".format(element.get_property("innerText"), element.get_attribute("innerText")))
#                 txt = element.get_property("innerText")
#                 # print("({1})txt = {0}".format(txt, type(txt)))
#                 snomes.append(txt)
#         sobrenomes["sobrenomes{0}".format(index)] = snomes
#         print(json.dumps(sobrenomes["sobrenomes{0}".format(index)]))
#         index+=1
#     driver.quit()
#     sobrenome_json = json.dumps(sobrenomes)
#     print(sobrenome_json)

def encode_number(number):
    number_dict = {
        0: 'o',
        1: 'i',
        2: 'z',
        3: 'e',
        4: 'a',
        5: 's',
        6: 'c',
        7: 't',
        8: 'b',
        9: 'g',
    }
    old_str = str(number)
    new_str = ''
    if type(number) == int:
        for n in old_str:
            new_str += str(number_dict[int(n)])
        return new_str


def is_ascii(word):
    if type(word) == str:
        for letter in word:
            if ascii_letters.find(letter) == -1 and letter != " ":
                return False
                break
        return True
    else:
        raise TypeError("Must be an string type.")


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
                    word = word[0:index] + not_ascii[letter] + word[index + 1:len(word)]
                else:
                    word = word[0:index] + '_' + word[index + 1:len(word)]
        qnt = word.count("_")
        for i in range(qnt):
            word = word.replace("_", "")
        return word


def get_sobrenomes():
    driver = init_chrome_driver(True, True, "https://nomestop.com/sobrenomes-brasileiros/")
    paragraphs = driver.find_elements_by_tag_name("p")
    sobrenomes = []
    for p in paragraphs:
        text = p.get_property("innerText")
        if text.count(" ") <= 1 and text != "":
            sobrenomes.append(text)
    # not_ascii = []
    # for sb in sobrenomes:
    #     if not is_ascii(sb):
    #         not_ascii.append(sb)
    # print("quantidade: {0}".format(len(not_ascii)))
    # print(not_ascii)
    return sobrenomes


def get_americans_lastnames():
    driver = init_chrome_driver(True, True, "https://www.rong-chang.com/namesdict/100_last_names.htm")
    links = driver.find_elements_by_tag_name("a")
    lastnames = []
    for link in links:
        if link.get_attribute("href").find("dictionary") != -1:
            lastnames.append(link.get_property("innerText").title())
    return lastnames


def get_br_male_names():
    driver = init_chrome_driver(True, True, "http://nomesportugueses.blogspot.com/p/nomes-masculinos-z_28.html")
    itens = driver.find_elements_by_tag_name('li')
    names = []
    for item in itens:
        if item.get_property("innerText").count(" ") == 0:
            names.append(item.get_property("innerText").title())
    return names


def get_br_female_names():
    driver = init_chrome_driver(True, True, "http://nomesportugueses.blogspot.com/p/nomes-brasileiros-de-z.html")
    itens = driver.find_elements_by_tag_name('li')
    names = []
    for item in itens:
        if item.get_property("innerText").count(" ") == 0:
            names.append(item.get_property("innerText").title())
    return names


def get_us_male_names():
    driver = init_chrome_driver(True, True, "https://names.mongabay.com/male_names.htm")
    links = driver.find_elements_by_tag_name("a")
    names = []
    for link in links:
        if link.get_attribute("href").find("names") != -1:
            content = link.get_property("innerText")
            if is_ascii(content):
                names.append(content.title())
    return names


def get_us_female_names():
    driver = init_chrome_driver(True, True, "https://names.mongabay.com/baby_names/girls250.html")
    links = driver.find_elements_by_tag_name("td")
    names = []
    for link in links:
        content = link.get_property("innerText")
        if is_ascii(content) and content != " ":
            names.append(content.title())
    return names


def write_json_file(name_list, file_name, file_format='json'):
    if type(file_name) == str and type(name_list) == list:
        index = 0
        file = None
        while True:
            i = index
            if index == 0:
                i = ''
            file_fullname = './{0}{1}.{2}'.format(file_name, i, file_format)
            if os.path.exists(file_fullname):
                index += 1
            else:
                print(file_fullname)
                file = open(file_fullname, 'w')
                break
        if file != None:
            index = 1
            name_dict = {}
            for name in name_list:
                # str_number = encode_number(index)
                # code = bcrypt.hashpw(str_number.encode(), bcrypt.gensalt()).__str__()
                name_dict['name_{0}_arch'.format(index)] = name
                index += 1
            content = json.dumps(obj=name_dict, ensure_ascii=False)
            file.writelines(content)
            file.close()
            return True
        else:
            return False

    else:
        raise TypeError("Pass a str and a list object.")


def get_and_write(func, filename, file_format):
    function_type = type(lambda x: x + 1)
    if type(func) == function_type:
        names_list = func()
        result = write_json_file(names_list, filename, file_format)
        if result:
            print("success")
        else:
            print("failure")
    else:
        raise TypeError("Must pass a function.")


if __name__ == "__main__":
    get_and_write(get_sobrenomes, 'br_lastnames', 'json')
    get_and_write(get_americans_lastnames, 'us_lastnames', 'json')
    get_and_write(get_br_male_names, 'br_male_names', 'json')
    get_and_write(get_br_female_names, 'br_female_names', 'json')
    get_and_write(get_us_male_names, 'us_male_names', 'json')
    get_and_write(get_us_female_names, 'us_female_names', 'json')
