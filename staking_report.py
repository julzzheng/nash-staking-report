import sys
import os
import argparse
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from selenium import webdriver
from helper import log_into_nash, get_staking_dividends

TODAY = datetime.utcnow().date()
current_path = os.path.dirname(os.path.abspath(__file__))
EXPORT_PATH = os.path.join(current_path, 'export')
COLUMNS = ['Type', 'Buy', 'BuyCur', 'Sell', 'SellCur', 'Fee', 'FeeCur', 'Exchange', 'Group', 'Comment', 'Date']


def run(driver, start_time):
    """

    :param driver:
    :return:
    """
    time = date_parser.parse(start_time)
    log_into_nash(driver)

    df = pd.DataFrame(columns=COLUMNS)

    while True:
        try:
            year, month, day = str(time.date()).split('-')
            url = f'https://app.nash.io/staking/statements/{year}/{month}/{day}'
        except TimeoutError:
            pass

        dividends = get_staking_dividends(driver, url, time)
        df = df.append(dividends, ignore_index=True)

        time += timedelta(days=1)

        if time.date() > TODAY:
            break

    df.to_csv(EXPORT_PATH + f'/{str(TODAY)}.csv', index=False)
    driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_time', type=str, default='2019-09-01')
    args = parser.parse_args()

    if sys.platform == "darwin":
        executable_path = "./bin/chromedriver_mac"
    elif "linux" in sys.platform:
        executable_path = "./bin/chromedriver_linux"
    elif "win32" in sys.platform:
        executable_path = "./bin/chromedriver_win32.exe"
    else:
        raise Exception('Driver for os not found.')

    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(executable_path=executable_path, options=options)
    driver.maximize_window()

    run(driver=driver, start_time=args.start_time)