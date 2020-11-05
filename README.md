# Staking Report Creator

[Nash Exchange](https://nash.io) - Staking Report Creator

This is a Python script to export staking reports for tracking the dividends on external websites, e.g. on [CoinTracking](https://cointracking.info).

For now this script only works for the Chrome Browser and you might have to [download](https://chromedriver.storage.googleapis.com/index.html) a suitable Selenium driver if the available drivers do not work for you.

If you don't have a Nash account yet, feel free to sign up [here](https://app.nash.io/create-account?code=2TnCEZ).

## Getting Started

### Prerequisites
- Python 3.7 or higher

### Install Requirements
Use a package manager of your choice and run the following command
````
pip install -r requirements.txt
````
### Run Tracker

Parameters:
1. ``start_time``: From which date to start to export the reports, e.g. 2019-09-01

````
python staking_report --start_time=2019-09-01
````
