from os.path import dirname, abspath, join
from selenium.webdriver import Chrome, ChromeOptions
from file2 import greed
base_dir_path = dirname(dirname(dirname(abspath(__file__))))
chromedriver_path = join(base_dir_path, "chromedriver_linux64/chromedriver")

def init_chrome_driver(headless=False, incognito=False, url=""):
    global chromedriver_path
    chrome_options = ChromeOptions()
    if headless:
        chrome_options.add_argument("---headless")
    if incognito:
        chrome_options.add_argument("--incognito")
    driver = Chrome(executable_path=chromedriver_path,options=chrome_options)
    if url != "" and url != None and type(url) == str:
        driver.get(url)
    print("Chrome driver inicializado.")
    return driver

if __name__ == "__main__":
    print("Nice !!")
    greed()