from selenium import webdriver
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys

def create_driver(headless=False, incognito=True, random_user=True) -> None:
    user = {
        'User-Agent': UserAgent().random,
    }

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    #chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument('--disable-gpu')

    chrome_options.add_argument('--log-level=3')
    if incognito: chrome_options.add_argument('--incognito')
    if headless: chrome_options.add_argument('--headless')
    if random_user: chrome_options.add_argument(f'user-agent={user}')

    driver = uc.Chrome(options=chrome_options, use_subprocess=True)

    return driver

def delete_driver(driver) -> None:
    driver.close()
    driver.quit()
