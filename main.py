import requests
from datetime import datetime as dt
import time
import os
import sys
import subprocess


def convert_dt_epoch(text):
    dt_object = dt.strptime(text, "%m/%d/%Y")
    epoch = int(time.mktime(dt_object.timetuple()))
    return epoch


def file_name(text):
    result = f"{text}.csv"
    return result


def open_file(file):
    if sys.platform == "win32":
        os.startfile(file)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, file])


ticker_symbol = input("Enter a ticker symbol: ").upper()
start_date = input("Enter starting date (mm/dd/yyyy format): ")
end_date = input("Enter ending date (mm/dd/yyyy format): ")


url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker_symbol}?period1={convert_dt_epoch(start_date)}\
&period2={convert_dt_epoch(end_date)}&interval=1d" \
      "&events=history&includeAdjustedClose=true"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 "
                         "Safari/537.36"}

# Finance site does not allow scripts to download from them. To circumvent this, a headers parameter
# is added to the requests.get method that spoof a user-agent.


content = requests.get(url, headers=headers).content    # Content returns in byte format

with open(file_name(ticker_symbol), "wb") as f:
    f.write(content)

open_file(file_name(ticker_symbol))
