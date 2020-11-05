# Staking Report Creator

[Nash Exchange](https://nash.io) - Staking Report Creator

This is a Python script to export staking reports for tracking the dividends on external websites, e.g. on [CoinTracking](https://cointracking.info).

For now this script only works for the Chrome Browser and you might have to [download](https://chromedriver.storage.googleapis.com/index.html) a suitable Selenium driver if the available drivers do not work for you.

If you don't have a Nash account yet, feel free to sign up [here](https://app.nash.io/create-account?code=2TnCEZ).

## Getting Started

### Prerequisites
- Python 3.7 or higher

### Install Python
There are different possibilities for this depending on your operating system. For example, you can download a current version directly from the [Python](https://www.python.org/downloads) website, or you can use a package manager like [Conda](https://docs.conda.io/en/latest/miniconda.html). 

### Install Requirements
Use a package manager of your choice and run the following command
````
pip install -r requirements.txt
````
### Run Report Creator

Parameters:
1. ``start_time``: From which date to start to export the reports, e.g. 2019-09-01

````
python staking_report.py --start_time=2019-09-01
````
### Login
There are two ways to log in:
1. Type into the terminal when prompted
2. Or create a credentials.txt file with two lines each for email and password

After logging in you will also be asked to enter your 2FA code.