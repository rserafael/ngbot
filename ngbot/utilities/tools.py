from os.path import abspath,join, dirname

_directory_ = dirname(abspath(__file__))
chromedriver_path = join(_directory_,  'chromedriver')


def init_chrome_driver(headless=False, incognito=False, url="", verbose=False):

    from selenium.webdriver import Chrome, ChromeOptions
    global chromedriver_path

    if verbose:
        print("file: {0}".format(abspath(__file__)))
        print("chromedriver_path  = {0}".format(chromedriver_path))
    chrome_options = ChromeOptions()

    if headless:
        chrome_options.add_argument("---headless")

    if incognito:
        chrome_options.add_argument("--incognito")

    driver = Chrome(executable_path=chromedriver_path, options=chrome_options)

    if url != "" and url != None and type(url) == str:
        driver.get(url)

    if verbose:
        print("Chrome Driver has started.")

    return driver


def showObj(obj, name):
    print("---------{0}---------".format(name))
    for prop in dir(obj):
        value = eval("obj.{0}".format(prop))
        prop_type = str(type(value)).replace("class ", "").replace('<', '').replace(">", '')
        print("({0}) {1}".format(prop_type, prop))
    print("---------{0}---------".format(name))