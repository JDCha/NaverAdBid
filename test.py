import sys
import os
import time
import datetime

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.

from datetime import datetime
from datetime import timedelta
import os, sys, time


start_hour = "22:00"
duration_hour = 10


start_time = datetime.strptime(start_hour, "%H:%M")
after_h = timedelta(hours=duration_hour)
end_hour = start_time + after_h

start_hour = start_hour
end_time = end_hour


print(start_time)
print(after_h)
print(end_hour)
print(start_hour)

print(end_time.hour)
print('now ' + str(datetime.now().hour))

