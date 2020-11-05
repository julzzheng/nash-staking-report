import os
import getpass
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

current_path = os.path.dirname(os.path.abspath(__file__))
EXPORT_PATH = os.path.join(current_path, 'export')
CREDENTIALS_FILE = os.path.join(current_path, 'credentials.txt')
LOGIN_URL = 'https://app.nash.io/auth/sign-in'
COLUMNS = ['Type', 'Buy', 'BuyCur', 'Exchange', 'Comment', 'Date']


def get_credentials():
    """
    Get user credentials either by the credentials file or by user input.
    :return: credentials
    :raises:
    """

    def get_by_file():
        with open(CREDENTIALS_FILE, 'r') as f:
            content = f.readlines()
            if len(content) != 2:
                return None
            else:
                return {
                    'username': content[0].strip(),
                    'password': content[1].strip()
                }

    def get_by_user_input():
        username = input('Nash Username: ')
        password = getpass.getpass('Nash Password: ')
        return {
            'username': username.strip(),
            'password': password.strip()
        }

    for strategy_fn in [get_by_file, get_by_user_input]:
        try:
            credentials = strategy_fn()
            if credentials:
                return credentials
        except:
            pass

    raise Exception('Could not retrieve username or password.')


def log_into_nash(driver):
    credentials = get_credentials()
    login(driver, credentials['username'], credentials['password'])


def login(driver, username, password):
    try:
        driver.get(LOGIN_URL)
    except TimeoutException:
        pass

    wait_until_visible(driver=driver, xpath='//input[@id="email"]')
    email_input = driver.find_element_by_xpath('//input[@id="email"]')
    email_input.clear()
    email_input.send_keys(username)
    password_input = driver.find_element_by_xpath('//input[@id="password"]')
    password_input.clear()
    password_input.send_keys(password)

    wait_until_visible(driver=driver, xpath='//button[@data-testid="submit-button" and not(@disabled)]')
    driver.find_element_by_xpath('//button[@data-testid="submit-button"]').click()

    wait_until_visible(driver=driver, xpath='//input[@data-testid="two-fa-code"]')
    auth_code = input('2FA Code: ')
    auth_input = driver.find_element_by_xpath('//input[@data-testid="two-fa-code"]')
    auth_input.clear()
    auth_input.send_keys(auth_code)

    wait_until_redirected(driver=driver, url=LOGIN_URL)


def get_staking_dividends(driver, url, time):
    print(time)
    try:
        driver.get(url)
    except TimeoutException:
        pass

    wait_until_visible(driver=driver, xpath='//table[@role="table"]')
    html_page = driver.page_source
    soup = BeautifulSoup(html_page, 'lxml')

    dividends = []

    for row in soup.find('table').tbody.findAll('tr'):
        dividends.append(tuple(row.findAll('td')[2].text.split()))

    return list(map(lambda div: pd.Series(
        ['Interest Income', div[0], div[1], 'Nash Exchange', 'Staking dividend', str(time)], index=COLUMNS), dividends))


def wait_until_visible(driver, xpath, timeout=30, frequency=0.5):
    return WebDriverWait(driver, timeout, frequency).until(EC.visibility_of_element_located((By.XPATH, xpath)))


def wait_until_redirected(driver, url, timeout=30, frequency=0.5):
    return WebDriverWait(driver, timeout, frequency).until(lambda driver: driver.current_url != url)
