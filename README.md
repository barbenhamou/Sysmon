# Sysmon

## Welcome to MY SYSMON


## From Git to Run
1. Download the project files from my github repo 'https://github.com/barbenhamou/Sysmon.git'.
2. Make sure u have python (> 3.9, preferred above 3.12). And python venv.
3. Create a new venv.
4. Install the requirements - 'pip install -e .[test] '.
5. Run commands:
    1. run_sysmon - default, interval == 1 and log path == "./log.json".
    2. run_sysmon --log <LOG_PATH> --interval <INTERVAL> -  enter your own path and interval, make sure the file is of json type, and interval is greater than 0.

## Run Example
![Demo](docs/assets/Demo.gif)